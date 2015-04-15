json.array!(@folders) do |folder|
  json.extract! folder, :id, :parent_id, :user_id, :name, :description, :updated_at
  json.url folder_url(folder, format: :json)
end
