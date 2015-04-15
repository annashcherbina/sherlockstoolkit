class Locus < ActiveRecord::Base
  has_many :panel_loci
  has_many :panels, through: :panel_loci
  has_many :primers
  has_and_belongs_to_many :loci_groups

  private
  def self.make_snp_loader_hash
    hash = {}

    Locus.all.each do |locus|
      hash[locus.name] = locus
    end

    hash
  end
end
