json.array!(@parameters) do |parameter|
  json.extract! parameter, :id, :comparison_id, :kinship_id, :name, :attribute_type, :attribute_int, :attribute_float, :attribute_string, :attribute_bool
  json.url parameter_url(parameter, format: :json)
end
