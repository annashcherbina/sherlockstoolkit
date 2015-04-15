class CreateChoices < ActiveRecord::Migration
  def change
    create_table :choices do |t|
      t.integer :attribute_id
      t.string :name, :limit => 80
    end  # do
  end  # change
  
  def self.up
    add_index :choices, [:name], :name => :idx_choices_names
  end  # up
end  # class
