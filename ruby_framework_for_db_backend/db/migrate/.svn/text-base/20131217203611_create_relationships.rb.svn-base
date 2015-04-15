class CreateRelationships < ActiveRecord::Migration
  def change
    create_table :relationships do |t|
      t.integer :family_id
      t.integer :person_id
      t.integer :person2_id
      t.string :relation, :limit => 64
      t.integer :degree
      t.float   :expected_shared_alleles
    end  # do
  end  # change
  
  def self.up
    add_index :relationships, [:person_id], :name => :idx_relationships_person1
    add_index :relationships, [:person2_id], :name => :idx_relationships_person2
  end  # up
end  # class
