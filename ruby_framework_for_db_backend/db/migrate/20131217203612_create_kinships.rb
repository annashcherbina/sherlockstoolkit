class CreateKinships < ActiveRecord::Migration
  def change
    create_table :kinships do |t|
      t.integer :relationship_id
      t.integer :common_minor_alleles
      t.integer :total_minor_alleles
    end  # do
  end  # change
  
  def self.up
    add_index :kinships, [:relationship_id], :name => :idx_kinships_relationship
  end  # up
end  # class
