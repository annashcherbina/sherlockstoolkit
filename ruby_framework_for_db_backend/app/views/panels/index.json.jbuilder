json.array!(@panels) do |panel|
  json.extract! panel, :id, :name, :description, :updated_at
  json.url panel_url(panel, format: :json)
end
