class CreateParameters < ActiveRecord::Migration
  def change
    create_table :parameters do |t|
      t.references  :user
      t.string      :group_name, limit: 40, index: true
      t.string      :category, :limit=>80, index: true
      t.string      :name, :limit => 80, index: true
      t.float       :value
      t.boolean     :is_visible
    end  # do
  end  # change
end  # class