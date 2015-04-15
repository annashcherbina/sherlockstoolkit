class CreateAttributes < ActiveRecord::Migration
  def change
    create_table :attributes do |t|
      t.string :name, :limit => 80
    end  # do
  end  # change
  
  def self.up
    add_index :attributes, [:name], :name => :idx_attributes_names
  end  # up
end  # class
