class CreateFamilies < ActiveRecord::Migration
  def change
    create_table :families do |t|
      t.string :name, :limit => 80
      t.string :source, :limit => 80
    end  # do
  end  # change
  
  def self.up
    add_index :families, [:name], :name => :idx_families_names
  end  # up
end  # class
