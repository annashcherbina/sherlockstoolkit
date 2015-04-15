class CreateExperiments < ActiveRecord::Migration
  def change
    create_table :experiments do |t|
      t.integer     :instrument_id
      t.integer     :primer_panel_id
      t.references  :folder,  index: true
      t.references  :attachment
      t.string      :hash_name, :limit => 32
      t.string      :name, :limit => 80, index: true
      t.boolean     :is_mixture
      t.string      :call_url, :limit => 160
      t.integer     :final_lib_reads
      t.integer     :wells_with_isp
      t.integer     :live_isp
      t.integer     :filtered_polyclonal
      t.string      :pcr, limit: 45
      t.string      :amp_lig_quant, limit: 45
      t.date        :empcr_date
      t.string      :template_amount_loaded, :limit => 500
      t.string      :notes, :limit => 1000
      t.date        :run_date
    end  # do
  end  # change
end  # class
