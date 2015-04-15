json.array!(@families) do |family|
  json.extract! family, :id, :name, :source
  json.url family_url(family, format: :json)
end
