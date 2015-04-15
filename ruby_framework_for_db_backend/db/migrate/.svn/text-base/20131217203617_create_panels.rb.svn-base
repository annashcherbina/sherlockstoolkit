class CreatePanels < ActiveRecord::Migration
  def change
    create_table :panels do |t|
      t.references :attachment
      t.string :name, :limit => 80
      t.string :panel_type, :limit => 40
      t.string :description, :limit => 80
      t.datetime :updated_at
    end  # do
  end  # change
  
  def self.up
    add_index :panels, [:name], :name => :idx_panels_names
  end  # up
end  # class
