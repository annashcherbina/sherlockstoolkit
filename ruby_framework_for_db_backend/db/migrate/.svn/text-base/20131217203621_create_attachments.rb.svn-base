class CreateAttachments < ActiveRecord::Migration
  def change
    create_table :attachments do |t|
      t.integer   :user_id
      t.integer   :folder_id
      t.string    :file_name,     limit: 1000
      t.integer   :internal_hash, limit: 8
      t.text      :description
      t.string    :file_type,     limit: 80
      t.string    :content_type,  limit: 80
      t.integer   :content_bytes
      t.binary    :contents, :limit => 32.megabyte
      t.boolean   :is_parsed
      t.float     :version
      t.float     :codebase_version
      t.datetime  :updated_at
    end  # do
  end  # change
  
  def self.up
    add_index :attachments, [:folder_id], :name => :idx_attachments_folder
    add_index :attachments, [:user_id], :name => :idx_attachments_user
  end  # up
end  # class
