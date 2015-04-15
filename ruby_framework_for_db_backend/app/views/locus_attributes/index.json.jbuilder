json.array!(@locus_attributes) do |locus_attribute|
  json.extract! locus_attribute, :id, :locus_id, :attribute_name, :attribute_choice
  json.url locus_attribute_url(locus_attribute, format: :json)
end
