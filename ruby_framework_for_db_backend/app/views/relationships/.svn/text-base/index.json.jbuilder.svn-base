json.array!(@relationships) do |relationship|
  json.extract! relationship, :id, :family_id, :person_id, :person2_id, :relation
  json.url relationship_url(relationship, format: :json)
end
