json.array!(@people) do |person|
  json.extract! person, :id, :id_code, :source
  json.url person_url(person, format: :json)
end
