class CreatePeople < ActiveRecord::Migration
  def change
    create_table :people do |t|
      t.integer :best_sample_id
      t.string :id_code, :limit => 80
      t.string :source, :limit => 80
      t.text :self_reported_ancestry
    end  # do
  end  # change
  
  def self.up
    add_index :people, [:id_code], :name => :idx_people_id_code
  end  # up
end  # class
