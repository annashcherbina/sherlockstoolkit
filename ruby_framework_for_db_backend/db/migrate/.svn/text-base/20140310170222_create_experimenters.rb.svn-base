class CreateExperimenters < ActiveRecord::Migration
  def change
    create_table :experimenters do |t|
      t.references :experiment, index: true
      t.references :person, index: true
      t.string :role
      t.boolean :empcr
      t.boolean :uncertain_empcr
      t.boolean :seq
      t.boolean :uncertain_seq
    end
  end
end
