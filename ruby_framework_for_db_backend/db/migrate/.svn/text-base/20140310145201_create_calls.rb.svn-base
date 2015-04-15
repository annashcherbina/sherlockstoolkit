class CreateCalls < ActiveRecord::Migration
  def change
    create_table :calls do |t|
      t.references :experiment, index: true
      t.references :locus, index: true
      t.references :sample, index: true
      t.integer :quality_thresh
      t.float :minor_allele_frequency
      t.integer :total_count
      t.integer :forward_count
    end
  end
end
