class CreateLociGroups < ActiveRecord::Migration
  def change
    create_table :loci_groups do |t|
      t.string :name, limit: 200
    end
  end
end