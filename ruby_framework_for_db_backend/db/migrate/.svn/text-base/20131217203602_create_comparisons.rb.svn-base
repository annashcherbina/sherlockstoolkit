class CreateComparisons < ActiveRecord::Migration
  def change
    create_table :comparisons do |t|
      t.integer :mixture_sample_id
      t.integer :reference_sample_id
      t.integer :tp_count
      t.integer :fp_count
      t.integer :fn_count
      t.integer :tn_count
      t.float :mixture_ma_threshold
      t.float :reference_ma_threshold
      t.float :rmne
      t.float :likelihood_ratio
    end  # do
  end  # change
  
  def self.up
    add_index :comparisons, [:barcode_id], :name => :idx_comparisons_barcode1
    add_index :comparisons, [:barcode2_id], :name => :idx_comparisons_barcode2
  end  # up
end  # class
