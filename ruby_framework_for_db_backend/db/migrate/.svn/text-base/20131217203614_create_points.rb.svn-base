class CreatePoints < ActiveRecord::Migration
  def change
    create_table :points do |t|
      t.integer :image_id
      t.string :type_of_point, :limit => 32
      t.float :qual
    end  # do
  end  # change
  
  def self.up
    add_index :points, [:image_id], :name => :idx_points_image
  end  # up
end  # class
