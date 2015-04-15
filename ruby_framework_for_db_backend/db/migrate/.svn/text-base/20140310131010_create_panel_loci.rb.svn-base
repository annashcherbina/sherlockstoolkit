class CreatePanelLoci < ActiveRecord::Migration
  def change
    create_table :panel_loci do |t|
      t.references :panel, index: true
      t.references :locus, index: true
      t.integer :quality_thresh, index: true
      t.integer :ambiguous, default: 0
      t.integer :low, default: 0
      t.integer :strand_bias, default: 0
      t.integer :total_count, default: 0
    end
  end
end
