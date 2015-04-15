class CreateInstruments < ActiveRecord::Migration
  def change
    create_table :instruments do |t|
      t.string :name, :limit => 80
    end  # do
  end  # change
  
  def self.up
    add_index :instruments, [:name], :name => :idx_instruments_names
  end  # up
end  # class
