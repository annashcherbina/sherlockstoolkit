class CreateSTRs < ActiveRecord::Migration
  def change
    create_table :strs do |t|
      t.references  :experiment,        index: true
      t.references  :primer,            index: true
      t.references  :locus,             index: true
      t.references  :sample,            index: true
      t.string      :name,              limit:80, index: true
      t.boolean     :is_stutter
      t.boolean     :is_novel_allele
      t.boolean     :is_novel_flank
      t.string      :novel_flank_name,  limit: 80
      t.string      :flank5,            limit: 100
      t.string      :flank3,            limit: 100
      t.string      :str_call,          limit: 500
    end
  end
end
