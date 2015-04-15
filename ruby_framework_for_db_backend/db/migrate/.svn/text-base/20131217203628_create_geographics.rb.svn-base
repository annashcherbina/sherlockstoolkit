class CreateGeographics < ActiveRecord::Migration
  def change
    create_table :geographics do |t|
      t.string :region_name, :limit => 80
    end  # do
  end  # change
  
  def self.up
    add_index :geographics, [:region_name], :name => :idx_geographics_names
  end  # up
end  # class
