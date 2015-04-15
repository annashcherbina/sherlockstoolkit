class Sample < ActiveRecord::Base
  belongs_to :experiment
  belongs_to :barcode
  has_many :calls
  has_many :person_samples
  has_many :people, through: :person_samples

  scope :is_mixture, lambda { where(is_mixture: true) }
  scope :reference, lambda { where(is_mixture: false) }
  scope :minor_calls_ordered, lambda { order("samples.minor_alleles_called DESC") }
  scope :total_reads_ordered, lambda { order("samples.total_reads DESC") }

  private
  #creates a hash of all Samples that are referenced by two keys, the experiment ID, followed by the barcode ID
  def self.make_snp_loader_hash
    hash = {}

    Sample.all.each do |sample|
      hash[sample.experiment_id] ||= {}
      hash[sample.experiment_id][sample.barcode_id] ||= {}
      hash[sample.experiment_id][sample.barcode_id][sample.quality_thresh] = sample
    end

    hash
  end


  #this hash is for the samples index view where all reference samples are arranged under the panel, and then subgrouped
  #by the source, and then further subgrouped by each person in descending order of total reads
  def self.make_samples_index_hash(experiments_hash)
    panels_hash = Hash[Panel.where(panel_type: "Primers").pluck(:id, :description)]
    sample_id_to_person_id_hash_nonmixture = Hash[PersonSample.pluck(:sample_id, :person_id)]
    people_hash = Tools::to_hash(Person.all)

    #initializes the return_hash
    return_hash = {}

    Sample.where(is_mixture: false).find_each do |sample|
      experiment = experiments_hash[sample.experiment_id]
      panel_name = panels_hash[experiment.primer_panel_id]

      person_id = sample_id_to_person_id_hash_nonmixture[sample.id]

      person = people_hash[person_id]
      person_source = person.source
      person_id_code = person.id_code

      return_hash[panel_name] ||=  {}
      return_hash[panel_name][person_source] ||= {}
      return_hash[panel_name][person_source][person_id_code] ||= []
      return_hash[panel_name][person_source][person_id_code] << sample
    end

    return_hash
  end

end
