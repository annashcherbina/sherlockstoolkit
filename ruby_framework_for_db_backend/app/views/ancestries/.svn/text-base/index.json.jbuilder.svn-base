json.array!(@ancestries) do |ancestry|
  json.extract! ancestry, :id, :person_id, :ethnicity_id, :percent
  json.url ancestry_url(ancestry, format: :json)
end
