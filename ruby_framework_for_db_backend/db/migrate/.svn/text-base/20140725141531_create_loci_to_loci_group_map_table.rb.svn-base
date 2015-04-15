class CreateLociToLociGroupMapTable < ActiveRecord::Migration
  def change
    create_table :loci_loci_groups, id: false do |t|
      t.references :locus
      t.references :loci_group
    end
    add_index :loci_loci_groups, [:locus_id, :loci_group_id]
  end
end
