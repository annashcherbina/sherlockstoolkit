class CreateAncestries < ActiveRecord::Migration
  def change
    create_table :ancestries do |t|
      t.references :person_sample, index: true
      t.references :ethnicity, index: true
      t.references :geographic
      t.string     :source_description, limit: 100
      t.float :percent
      t.boolean :self_reported
    end
  end
end