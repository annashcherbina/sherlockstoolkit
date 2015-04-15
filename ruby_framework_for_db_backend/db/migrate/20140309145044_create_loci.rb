class CreateLoci < ActiveRecord::Migration
  def change
    create_table :loci do |t|
      t.string :name,         limit: 80,  index: true
      t.string :locus_type,   limit: 8
      t.string :chromosome,   limit: 2
      t.string :region,       limit: 45
      t.integer :position
      t.boolean :exclude
      t.string :str_unit,     limit: 40
      t.string :flank5,       limit: 500
      t.string :snp_iub,      limit: 1
      t.string :flank3,       limit: 500
      t.float  :fst
    end
  end
end
