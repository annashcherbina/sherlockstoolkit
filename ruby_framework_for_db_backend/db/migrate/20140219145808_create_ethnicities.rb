class CreateEthnicities < ActiveRecord::Migration
  def change
    create_table :ethnicities do |t|
      t.references :geographic
      t.string :name, limit: 80
      t.float :lat
      t.float :lng
    end
  end
end
