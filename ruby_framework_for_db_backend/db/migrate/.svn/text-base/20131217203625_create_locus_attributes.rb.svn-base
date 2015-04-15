class CreateLocusAttributes < ActiveRecord::Migration
  def change
    create_table :locus_attributes do |t|
      t.integer :locus_id
      t.string :attribute_name, :limit => 45
      t.string :attribute_choice, :limit => 45
    end  # do
  end  # change
  
  def self.up
    add_index :locus_attributes, [:attribute_name], :name => :idx_locus_attributes_names
  end  # up
end  # class
