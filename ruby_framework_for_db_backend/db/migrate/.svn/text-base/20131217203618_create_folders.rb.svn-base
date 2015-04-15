class CreateFolders < ActiveRecord::Migration
  def change
    create_table :folders do |t|
      t.integer :parent_id
      t.integer :user_id
      t.string :name, :limit => 80
      t.string :description, :limit => 160
      t.integer :level
      t.datetime :updated_at
    end  # do
  end  # change
  
  def self.up
    add_index :folders, [:user_id], :name => :idx_folders_user
    add_index :folders, [:name], :name => :idx_folders_names
  end  # up
end  # class
