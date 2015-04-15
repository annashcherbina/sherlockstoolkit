class CreateSamples < ActiveRecord::Migration
  def change
    create_table :samples do |t|
      t.references :experiment, index: true
      t.references :barcode, index: true
      t.integer :quality_thresh, index: true
      t.boolean :is_good
      t.boolean :is_mixture
      t.integer :minor_alleles_called, default: 0
      t.integer :total_reads, default: 0
    end
  end
end
