class CreateAlleleReferences < ActiveRecord::Migration
  def change
    create_table :allele_references do |t|
      t.integer :locus_id
      t.string :allele_name, :limit => 80
      t.string :regular_expression, :limit => 500
      t.string :allele_sequence, :limit => 500
    end  # do
  end  # change
  
  def self.up
    add_index :allele_references, [:allele_name], :name => :idx_allele_references_names
  end  # up
end  # class
