class CreatePrimers < ActiveRecord::Migration
  def change
    create_table :primers do |t|
      t.integer :panel_id
      t.integer :locus_id
      t.string :name, limit: 80
      t.boolean :is_forward
      t.string :sequence, limit: 500
      
    end
  end
end
