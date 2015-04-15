json.array!(@geographics) do |geographic|
  json.extract! geographic, :id, :region_name
  json.url geographic_url(geographic, format: :json)
end
