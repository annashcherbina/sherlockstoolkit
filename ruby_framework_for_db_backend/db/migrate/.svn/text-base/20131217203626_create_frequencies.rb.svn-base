class CreateFrequencies < ActiveRecord::Migration
  def change
    create_table :frequencies do |t|
      t.integer :locus_id
      t.integer :ethnicity_id
      t.float :allele_frequency
      t.string :source, :limit => 64
    end  # do
  end  # change
  
  def self.up
    add_index :frequencies, [:locus_id], :name => :idx_frequencies_locus
  end  # up
end  # class
