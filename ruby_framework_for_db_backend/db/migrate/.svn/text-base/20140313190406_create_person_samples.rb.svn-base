class CreatePersonSamples < ActiveRecord::Migration
  def change
    create_table :person_samples do |t|
      t.references :sample, index: true
      t.references :person, index: true
      t.string :molarity, limit: 25
    end
  end
end
