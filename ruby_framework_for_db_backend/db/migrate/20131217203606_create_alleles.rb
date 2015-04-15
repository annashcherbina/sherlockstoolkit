class CreateAlleles < ActiveRecord::Migration
  def change
    create_table :alleles do |t|
      t.integer :experiment_id
      t.integer :primer_id
      t.integer :person_id
      t.integer :locus_id
      t.integer :barcode_person_id
      
      t.string :name, :limit => 80
      t.string :allele_base, :limit => 1
      t.integer :count
      t.integer :forward_count
      t.float :forward_qual
      t.float :reverse_qual
      
      t.boolean :is_minor
      t.boolean :is_stutter
      t.boolean :is_novel_allele
      t.boolean :is_novel_flank
      t.boolean :is_good

      t.string :novel_flank_name, :limit => 80
      t.string :flank5, :limit => 100
      t.string :flank3, :limit => 100
      t.string :str_call, :limit => 500
    end  # do
  end  # change
  
  def self.up
    add_index :alleles, [:experiment_id], :name => :idx_alleles_experiment
    add_index :alleles, [:person_id], :name => :idx_alleles_person
    add_index :alleles, [:name], :name => :idx_alleles_names
  end  # up
end  # class
