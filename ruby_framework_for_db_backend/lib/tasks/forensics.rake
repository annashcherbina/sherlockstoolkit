require 'activerecord-import'
require 'roo'
require "#{Rails.root}/app/helpers/snp_occurance"

namespace :forensics do
  FORENSICS_DATA_DIRECTORY = '/Volumes/ne24918/Bioinformatics_shared/Forensics/ForensicsData/csv/'
  FORENSICS_PANELS = %w(IAD1312 IAD1438 IAD1568 IAD28825 IAD30341 IAD39359)
  EXPERIMENTAL_QUALITY_LEVELS = [0, 20, 30, 40]

  desc "Uploads the summary file by creating Experiments and Subjects,"\
  " required parameter machine=$MACHINE, one of 'pgm', 'proton', or 'all'"
  task upload_summary: :environment do
    puts

    #checks that the machine environment var is set
    if ENV['machine'].nil?
      puts 'machine= not specified'
      next
    end

    root_xlsx_file_path = '/Users/ne24918/Downloads/data/july_summary_files/'
    proton_file = 'Proton_exp_summary09292014.xlsx'
    pgm_file = 'PGM_exp_summary20140721.xlsx'

    #gets the proper file path for the summary
    machine = ENV['machine'].downcase

    #parses the proper file depending on argument
    if machine == 'proton'
      parse_summary_file(root_xlsx_file_path + proton_file)
    elsif machine.to_s == 'pgm'
      parse_summary_file(root_xlsx_file_path + pgm_file)
    elsif machine == 'test'
      parse_summary_file(root_xlsx_file_path + test_file)
    elsif machine == 'both'
      parse_summary_file(root_xlsx_file_path + pgm_file)
      parse_summary_file(root_xlsx_file_path + proton_file)
    else
      puts 'Unknown Machine Specified'
      next
    end
  end

  #gets experimental folders for a particular given panel_path
  def get_experimental_folders(panel_path)
    delete_length = panel_path.length + 1
    folders = `find #{panel_path} -type d`.split("\n")

    #array of experimental folders with all 4 quality levels
    valid_folders = []

    folders.each do |folder|
      experiment_hash = folder[delete_length..-1]

      #ignores folders that do not have hashes
      next if experiment_hash.nil? || experiment_hash.empty?

      #valid_folder is true iff the folder named 'ABCDE' has a file with the name 'ABCDE_Q'* in it,
      #following naming conventions
      folder_path = "#{panel_path}/#{experiment_hash}"
      valid_folder = `if ls #{folder_path}/#{experiment_hash}_Q* &> /dev/null; then echo '1'; else echo '0'; fi`.to_i == 1

      valid_folders << folder if valid_folder
    end

    valid_folders
  end

  #gets all the hashes of the folders that match the requirements for get_experimental_folders for each panel
  def get_all_experimental_hashes
    all_experimental_folders = []
    FORENSICS_PANELS.each do |panel|
      all_experimental_folders << get_experimental_folders(FORENSICS_DATA_DIRECTORY + panel)
    end
    all_experimental_folders.flatten!
    all_experimental_folders.map{ |str| str.split('/').last }
  end

  def parse_summary_file(file_path)
    #creates an array of experimental hash names where the experimental csv data has already been processed
    experimental_hashes = get_all_experimental_hashes
    existing_panels_names = Panel.uniq.pluck(:description)

    puts
    puts file_path
    instrument_id = Instrument.find_by("lower(name) = ?", file_path.split('/').last.split('_').first).id

    #constants for what columns are for what
    col_hash_name = 1
    col_seq_panel = 2
    col_run_name = 3
    col_seq_run_date = 4
    col_subjects = 5
    col_barcode_prefix = 6
    col_barcode_mid = 7
    col_final_lib_reads = 8
    col_wells_w_isp = 9
    col_live_isp = 10
    col_filtered_polyclonal = 11
    col_pcr = 12
    col_amp_lig_quant = 13
    col_emp_pcr_date = 14
    col_who_empcr = 15
    col_who_empcr_uncert = 16
    col_who_seq = 17
    col_who_seq_uncert = 18
    col_template_amt_loaded = 19
    col_notes = 20
    col_molarity = 21

    puts "parsing summary file at #{file_path}"
    ss = Roo::Excelx.new(file_path)
    ss = ss.sheet(0)

    (2..ss.last_row).each do |i|
      begin
        #skips processing this line unless this line refers to an experiment where
        #the hash name is in the array of already processed files
        hash_name = ss.cell(i, col_hash_name).to_s.strip

        #ignore already processed experiments
        next if Experiment.exists?(hash_name: hash_name)


        seq_panel = ss.cell(i, col_seq_panel).to_s.strip
        #don't upload the samples for unknown panels yet
        unless existing_panels_names.include?(seq_panel)
          puts "Experiment hash #{hash_name} ignored due to primer field not matched"
          next
        end

        #ignore experiments without data
        unless experimental_hashes.include?(hash_name)
          puts "Experiment hash #{hash_name} on line #{i} ignored due to lack of processed experimental data"
          next
        end

        #parsing the information from the excel sheet
        exp_hash = {}
        exp_hash[:hash_name] = hash_name
        exp_hash[:instrument_id] = instrument_id
        exp_hash[:primer_panel_id] = Panel.find_by_description(seq_panel).id
        exp_hash[:name] = ss.cell(i, col_run_name).to_s.strip
        exp_hash[:final_lib_reads] = ss.cell(i, col_final_lib_reads).to_i
        exp_hash[:wells_with_isp] = ss.cell(i, col_wells_w_isp).to_i
        exp_hash[:live_isp] = ss.cell(i, col_live_isp).to_i
        exp_hash[:filtered_polyclonal] = ss.cell(i, col_filtered_polyclonal).to_i
        exp_hash[:pcr] = ss.cell(i, col_pcr).to_s.strip
        exp_hash[:amp_lig_quant] = ss.cell(i, col_amp_lig_quant).to_s.strip
        exp_hash[:empcr_date] = ss.cell(i, col_emp_pcr_date)
        exp_hash[:template_amount_loaded] = ss.cell(i, col_template_amt_loaded).to_s.strip
        exp_hash[:notes] = ss.cell(i, col_notes).to_s.strip
        exp_hash[:run_date] = ss.cell(i, col_seq_run_date)


        #if the experiment has samples associated with it go ahead and ignore the summary parsing for it
        subjects_array = to_array(ss.cell(i, col_subjects).to_s.strip)
        barcode_prefix = ss.cell(i, col_barcode_prefix).to_s.strip
        barcodes_array = to_array(ss.cell(i, col_barcode_mid).to_s.strip)
        molarity_array = to_array(ss.cell(i, col_molarity).to_s.strip)

        #ignores experiments that are not matched sizes or if one is empty
        if subjects_array.size != barcodes_array.size || subjects_array.empty?
          puts "Experiment hash #{hash_name} ignored due to mismatch or lack of subjects, barcode field"
          next
        end

        Experiment.transaction do
          experiment = Experiment.create(exp_hash)
          is_mixture = create_samples(experiment.id, subjects_array, barcode_prefix, barcodes_array, molarity_array)
          experiment.update(is_mixture: is_mixture)

          if experiment.samples.count == 0
            puts "Experiment #{hash_name} ignored, cannot make samples for it"
            raise ActiveRecord::Rollback
          end
        end

      rescue
        puts "rescue: #{file_path}: row #{i} is not parsed, experiment: #{hash_name}"
      end #begin/rescue
    end #for each row in csv summary loop
    puts
  end #parse_summary_file

  #returns boolean stating if the sample contains a mixture
  def create_samples(experiment_id, subjects_array, barcode_prefix, barcodes_array, molarity_array)
    is_mixture = nil

    Sample.transaction do
      begin
        EXPERIMENTAL_QUALITY_LEVELS.each do |quality|
          #molarity type = true if it is a titration, otherwise false
          molarity_type = (molarity_array == molarity_array.flatten)
          molarity_index = 0

          #iterate through both arrays at the same time
          subjects_array.each_with_index do |subject_group, index|
            barcode_name = barcode_prefix + '-' + '%02d' % barcodes_array[index].to_s
            target_barcode_id = Barcode.find_by(name: barcode_name).id

            #MIXTURE EXPERIMENT
            if subject_group.kind_of?(Array)
              #a sample is not uniquely id'd by its experiment and barcode,
              #since a single experiment may have the same barcode run multiple times
              sample = Sample.create(make_sample_hash(experiment_id, target_barcode_id, nil, true, 0, quality))
              has_molarity = false

              subject_group.each_with_index do |subject_id_code, subject_index|
                person_id = Person.find_by(id_code: subject_id_code).id

                if !molarity_type && !molarity_array[molarity_index].nil?
                  molarity = molarity_array[molarity_index][subject_index]
                  has_molarity = true
                else
                  molarity = nil
                end
                PersonSample.create(sample_id: sample.id, person_id: person_id, molarity: molarity)
              end #subjects_array

              molarity_index = molarity_index + 1 if has_molarity

              is_mixture = true
              #1 to 1
              #NOT A MIXTURE EXPERIMENT
            else
              #create new singular sample
              sample = Sample.create(make_sample_hash(experiment_id, target_barcode_id, nil, false, 0, quality))
              person_id = Person.find_by(id_code: subject_group).id

              if molarity_type && !molarity_array[molarity_index].nil?
                molarity = molarity_array[molarity_index]
                molarity_index = molarity_index + 1
              else
                molarity = nil
              end

              PersonSample.create(sample_id: sample.id, person_id: person_id, molarity: molarity)

              is_mixture ||= false
            end #if, elsif chain
          end #subjects array foreach
        end #qualities each

      rescue
        puts "Creating Samples failed for experiment hash_name: #{hash_name}, perhaps due to missing data, either in subjects, barcodes"
        is_mixture = nil
      end #begin statement
    end #Sample.transaction do
    is_mixture
  end #create_samples


  def make_sample_hash(experiment_id, barcode_id, is_good, is_mixture, minor_alleles_called, quality)
    sample_hash = {}
    sample_hash[:experiment_id] = experiment_id
    sample_hash[:barcode_id] = barcode_id
    sample_hash[:is_good] = is_good
    sample_hash[:is_mixture] = is_mixture
    sample_hash[:minor_alleles_called] = minor_alleles_called
    sample_hash[:total_reads] = 0
    sample_hash[:quality_thresh] = quality
    sample_hash
  end

  #converts strings such as
  #5,6,(24,22),12, (55, 61), 1, (80, 2)"
  #into an array in the form of
  #[5, 6, [24, 22], 12, [55, 61], 1, [80, 2]]
  def to_array(string)
    begin
      #making the string YAML loadable
      string.gsub!(/(,)(\S)/, '\\1 \\2')
      string.gsub!(/[()]/, '(' => '[', ')' => ']')
      string = '[' + string + ']'
      YAML::load(string)
    rescue
      puts "to_array failed for: #{string}"
    end
  end #to_array

  desc "Uploads Experimental Data CSV files into the Database"\
  " required parameter panels=$PANELS, a comma-separated string of panel names, or simply 'all'"
  task upload_snps: :environment do
    #figures out which panels to process
    if ENV['panels'].nil?
      puts 'missing panels arg'
      next
    end
    panels = ENV['panels'].upcase.split(',')
    if panels == ['ALL']
      panels = FORENSICS_PANELS
    else
      panels = FORENSICS_PANELS & panels
    end
    puts "WILL PROCESS PANELS #{panels.to_s}"

    start_time = Time.now
    puts "BEGIN TIME: #{start_time}"
    load_all_experiments(panels)
    end_time = Time.now
    puts "END TIME: #{end_time}"
    puts "TOTAL ELAPSED TIME: #{((end_time-start_time)/60).round(2)} MINUTES FOR PANELS #{panels.to_s}"
  end

  def load_all_experiments(panels)
    barcodes_hash = Barcode.make_snp_loader_hash
    samples_hash = Sample.make_snp_loader_hash
    loci_hash = Locus.make_snp_loader_hash
    panels_hash = Panel.make_snp_loader_hash
    panel_loci_hash = PanelLocus.make_snp_loader_hash

    panels.each do |panel|
      puts
      panel_start_time = Time.now
      puts "STARTED PANEL #{panel} AT #{panel_start_time}"
      folder_array = get_experimental_folders(FORENSICS_DATA_DIRECTORY + panel)

      folder_array.each do |folder|
        experiment_hash = folder.split('/').last

        experiment = Experiment.find_by_hash_name(experiment_hash)
        if experiment.nil?
          puts "No summary entry for experiment loaded for hash: #{experiment_hash} in folder: #{panel}"
          next
        end

        EXPERIMENTAL_QUALITY_LEVELS.each do |quality_num|
          quality_str = quality_num
          quality_str = 'DEF' if quality_num == 0

          #skip reprocessing this experiment
          #if at least one of the samples at a given quality level in the experiment have associated snps
          if experiment.samples.where(quality_thresh: quality_num).inject(false){|result, sample| result || !sample.calls.empty?}
            puts "#{experiment.hash_name} Experiment already processed at quality: #{quality_num}, skipping"
            next
          end

          file_path = `ls #{folder}/#{experiment_hash}_Q#{quality_str}*.csv`.chomp

          if $?.exitstatus != 0
            puts "Cannot find #{folder} at quality level: #{quality_str}"
            next
          end

          puts "loading #{experiment_hash} at quality level: #{quality_str} from file #{file_path}"
          Call.transaction do
            load_snp_file(file_path, experiment, quality_num, barcodes_hash, samples_hash, loci_hash, panels_hash, panel_loci_hash)
          end #Call.transaction

        end #for each quality level
      end #file each

      panel_end_time = Time.now
      puts "FINISHED PANEL #{panel} ELAPSED TIME: #{((panel_end_time-panel_start_time)/60).round(2)} MINUTES"
      puts
    end #each forensics_panel

  end #load all experiments

  def load_snp_file(file_path, experiment, quality_num, barcodes_hash, samples_hash, loci_hash, panels_hash, panel_loci_hash)
    file = File.open(file_path)

    experiment_panel = experiment.panel

    #otherwise, go ahead and insert snps for this experiment
    SNP.transaction do
      snps = []
      file.each_line do |line|
        #lose the first line if it is a header
        next if line.include?('Barcode')
        next if line.include?('barcode')
        line = line.strip
        process_line(line, experiment.id, quality_num, experiment_panel, barcodes_hash, samples_hash, loci_hash, panels_hash, panel_loci_hash, snps)
      end

      SNP.import snps, validate: false
    end
    file.close
  end #load_snp_file


  def process_line(line, experiment_id, quality_num, experiment_panel, barcodes_hash, samples_hash, loci_hash, panels_hash, panel_loci_hash, snps)
    begin
      tokens = line.split("\t")

      barcode                 = tokens[0]

      #ignore unnecessary lines
      return if %w(no_mid nomatch).include?(barcode)

      locus                   = tokens[1]
      snp                     = tokens[2]
      minor                   = tokens[3]

      total_count             = tokens[20].to_i
      forward_count           = tokens[21].to_i
      minor_allele_frequency  = tokens[22].to_f
      low                     = tokens[23].to_i
      ambiguous               = tokens[24].to_i
      strand_bias             = tokens[25].to_i

      barcode_id = barcodes_hash[barcode].id
      sample = samples_hash[experiment_id][barcode_id][quality_num]
      sample_id = sample.id
      locus_id = loci_hash[locus].id


      #increment total reads only if it is more than 0
      sample.increment!(:total_reads, total_count) if total_count > 0

      call_hash = {}
      call_hash[:experiment_id]           = experiment_id
      call_hash[:locus_id]                = locus_id
      call_hash[:sample_id]               = sample_id
      call_hash[:quality_thresh]          = quality_num
      call_hash[:total_count]             = total_count
      call_hash[:forward_count]           = forward_count
      call_hash[:minor_allele_frequency]  = minor_allele_frequency

      call = Call.create(call_hash)

      #4 times because there are 4 bases in each row to tally
      4.times do |counter|
        column = 4 * counter + 4

        allele = SNPOccurance.new(tokens[column], tokens[column + 1].to_i, tokens[column + 2].to_f, tokens[column + 3].to_f)

        next if !snp.include?(allele.base) || allele.counts == 0

        snp_hash = {}
        snp_hash[:call_id] = call.id
        snp_hash[:allele_base] = allele.base
        snp_hash[:count] = allele.counts
        snp_hash[:forward_qual] = allele.forward_qual
        snp_hash[:reverse_qual] = allele.reverse_qual
        snp_hash[:is_minor] = minor.include?(allele.base)

        snps << SNP.new(snp_hash)
      end # 4.each


      #updating the sample's number of minor alleles called
      if (sample.is_mixture && minor_allele_frequency > 0.01) || (!sample.is_mixture && minor_allele_frequency > 0.3)
        Sample.increment_counter(:minor_alleles_called, sample_id)
      end

      #updating the new Panel Locus if there is a 1 in low, ambiguous, or strand bias
      panel_that_created_locus = panels_hash[experiment_panel.description]
      panel_locus_id = panel_loci_hash[panel_that_created_locus.id][locus_id][quality_num]

      panel_locus = PanelLocus.find(panel_locus_id)

      unless sample.is_mixture
        update_hash = {}
        update_hash[:low] = panel_locus.low + 1 if low == 1
        update_hash[:ambiguous] = panel_locus.ambiguous + 1 if ambiguous == 1
        update_hash[:strand_bias] = panel_locus.strand_bias + 1 if strand_bias == 1
        update_hash[:total_count] = panel_locus.total_count + 1
        panel_locus.update(update_hash)
      end
    rescue
      puts "Unable to parse the experiment file for experiment_id-quality: #{experiment_id}-#{quality_num},"\
            "Error at line: #{line}, barcode or sample not found"
      puts "#{$!}"
      puts $@[0]
      puts
      #return
    end # begin rescue
  end # process_line
end #namespace
