class CreateUsers < ActiveRecord::Migration
  def change
    create_table :users do |t|
      t.integer :home_folder_id
      t.string :username, :limit => 10
      t.string :name, :limit => 80
      t.string :email, :limit => 80
      t.string :hashed_password, :limit => 64
      t.string :salt, :limit => 64
      t.boolean :is_admin
    end  # do
  end  # change
  
  def self.up
    add_index :users, [:name], :name => :idx_users_names
  end  # up
end  # class
