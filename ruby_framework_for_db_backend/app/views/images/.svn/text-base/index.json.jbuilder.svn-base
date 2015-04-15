json.array!(@images) do |image|
  json.extract! image, :id, :folder_id, :name, :description, :image_type, :content_type, :picture_bytes, :created_at, :picture
  json.url image_url(image, format: :json)
end
