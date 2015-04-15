json.array!(@kinships) do |kinship|
  json.extract! kinship, :id, :relationship_id, :common_minor_alleles, :total_minor_alleles
  json.url kinship_url(kinship, format: :json)
end
