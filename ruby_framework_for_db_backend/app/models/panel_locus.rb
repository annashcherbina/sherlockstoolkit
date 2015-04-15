class PanelLocus < ActiveRecord::Base
  belongs_to :panel
  belongs_to :locus

  private
  #for snp_loader
  def self.make_snp_loader_hash
    hash = {}

    PanelLocus.find_each do |panel_locus|
      hash[panel_locus.panel_id] = {} if hash[panel_locus.panel_id].nil?
      hash[panel_locus.panel_id][panel_locus.locus_id] = {} if hash[panel_locus.panel_id][panel_locus.locus_id].nil?
      hash[panel_locus.panel_id][panel_locus.locus_id][panel_locus.quality_thresh] = panel_locus
    end

    hash
  end
end
