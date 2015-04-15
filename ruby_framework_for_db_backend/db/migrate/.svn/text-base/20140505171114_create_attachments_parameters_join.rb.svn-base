class CreateAttachmentsParametersJoin < ActiveRecord::Migration
  def change
    create_table :attachments_parameters, id: false do |t|
      t.references :attachment
      t.references :parameter
    end

    add_index :attachments_parameters, ["attachment_id", "parameter_id"]
  end
end
