class CreateBarcodes < ActiveRecord::Migration
  def change
    create_table :barcodes do |t|
      t.integer :panel_id
      t.string :name, :limit => 32
      t.string :barcode_seq, :limit => 32
      t.string :barcode_type, :limit => 32
    end  # do
    add_index :barcodes, [:panel_id], :name => :idx_barcodes_panel
    add_index :barcodes, [:barcode_seq], :name => :idx_barcodes_seqs
  end  # change
end  # class
