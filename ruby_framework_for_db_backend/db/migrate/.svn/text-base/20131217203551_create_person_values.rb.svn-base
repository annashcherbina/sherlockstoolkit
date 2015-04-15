class CreatePersonValues < ActiveRecord::Migration
  def change
    create_table :person_values do |t|
      t.integer :person_id
      t.integer :attribute_id
      t.integer :choice_id
      t.string :attribute_type, :limit => 16
      t.integer :attribute_int
      t.float :attribute_float
      t.string :attribute_string, :limit => 80
      t.boolean :attribute_bool
      t.string :source, :limit => 80
      t.boolean :is_truth
    end  # do
  end  # change
  
  def self.up
    add_index :person_values, [:person_id], :name => :idx_person_values_person_id
  end  # up
end  # class
