class Experiment < ActiveRecord::Base

  belongs_to :instrument
  belongs_to :attachment
  belongs_to :panel, foreign_key: "primer_panel_id"

  has_many :calls
  has_many :samples
  has_many :experimenters
  has_many :samples
  has_many :person_samples, through: :samples
  has_many :strs
  has_many :people, through: :samples

  validates :hash_name, :primer_panel_id, presence: true

  private
  def self.make_hash_by_name_and_hash_name
    hash = {}

    Experiment.all.each do |experiment|
      hash["#{experiment.name} - #{experiment.hash_name}"] = experiment
    end

    hash
  end
end # class