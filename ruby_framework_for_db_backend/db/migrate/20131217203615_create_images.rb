class CreateImages < ActiveRecord::Migration
  def change
    create_table :images do |t|
      t.references  :folder
      t.references  :user
      t.integer     :associated_image_id
      t.integer     :associated_attachment_id
      t.string      :file_name, :limit => 1000
      t.integer     :internal_hash, limit: 8
      t.text        :description
      t.string      :image_type, :limit => 80
      t.string      :content_type, :limit => 80
      t.integer     :picture_bytes
      t.binary      :picture, :limit => 15.megabyte
      t.float       :version
      t.float       :codebase_version
      t.datetime    :created_at
    end  # do
  end  # change
end  # class
