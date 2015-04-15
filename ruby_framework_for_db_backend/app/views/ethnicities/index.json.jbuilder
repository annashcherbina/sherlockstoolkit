json.array!(@ethnicities) do |ethnicity|
  json.extract! ethnicity, :id, :name, :race
  json.url ethnicity_url(ethnicity, format: :json)
end
