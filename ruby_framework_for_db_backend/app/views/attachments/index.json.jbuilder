json.array!(@attachments) do |attachment|
  json.extract! attachment, :id, :user_id, :folder_id, :file_name, :description, :file_type, :content_type, :updated_at, :contents_bytes, :contents
  json.url attachment_url(attachment, format: :json)
end
