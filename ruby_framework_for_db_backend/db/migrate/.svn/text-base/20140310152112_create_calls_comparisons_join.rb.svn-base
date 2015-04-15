class CreateCallsComparisonsJoin < ActiveRecord::Migration
  def change
    create_table :calls_comparisons, id: false  do |t|
      t.references :call,         index: true
      t.references :comparison,   index: true
    end
  end
end
