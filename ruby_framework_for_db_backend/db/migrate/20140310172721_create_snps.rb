class CreateSNPs < ActiveRecord::Migration
  def change
    create_table :snps do |t|
      t.references :call,     index: true
      t.string :allele_base,  limit: 1
      t.integer :count
      t.float :forward_qual
      t.float :reverse_qual
      t.boolean :is_minor
    end
  end
end
