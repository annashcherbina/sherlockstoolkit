require 'input_file.rb'

###############################################################################
class IdentitasLoader < InputFile
###############################################################################
  def initialize(name)
    super(name)
  end

  # method initalize

###############################################################################
  def skip_header
    for i in 1..11 do
      next_line
    end # for
  end

  # method skip_header

###############################################################################
  def load_snps
    puts 'load_snps: line = ' + line

    instrument = Instrument.create(name: 'Identitas custom SNP microarray')
    experiment = Experiment.create(instrument_id: instrument.id, hash_name: '12-17-2013_MIT-MP', name: 'December_17_2013_MIT-MP_FinalReport.txt', is_mixture: false, created_at: Time.now)

    sample_id = ''
    person = nil
    while  is_end_of_file? == false
      tokens = line.split("\t")

      # Set up the Locus.
      locus = Locus.find_by_name(tokens[0])
      if locus.nil?
        locus = Locus.create(name: tokens[0], locus_type: 'SNP', chromosome: tokens[8], position: tokens[7].to_i)
      end # if

      # Check for a new Sample ID
      if sample_id != tokens[1]
        sample_id = tokens[1]
        person = Person.create(id_code: sample_id, source: 'Identitas')
      end # if

      # Create each allele.
      if tokens[2] != '-'
        Allele.create(person_id: person.id, experiment_id: experiment.id, locus_id: locus.id, name: tokens[0], count: 1, is_good: true, allele_base: tokens[2])
      end # if

      if tokens[3] != '-'
        Allele.create(person_id: person.id, experiment_id: experiment.id, locus_id: locus.id, name: tokens[0], count: 1, is_good: true, allele_base: tokens[3])
      end # if

      next_line
    end # while
  end # method load_snps

###############################################################################
end # class

###############################################################################
def identitas_loader_main
  snp_file = IdentitasLoader.new('data/December_17_2013_MIT-MP_FinalReport.txt')
  snp_file.open_file
  snp_file.skip_header
  snp_file.load_snps
  snp_file.close_file
end

###############################################################################
# identitas_loader_main
