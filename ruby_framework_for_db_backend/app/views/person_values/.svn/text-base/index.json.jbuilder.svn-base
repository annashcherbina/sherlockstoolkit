json.array!(@person_values) do |person_value|
  json.extract! person_value, :id, :person_id, :attribute_id, :choice_id, :attribute_type, :attribute_int, :attribute_float, :attribute_string, :attribute_bool, :source, :is_truth
  json.url person_value_url(person_value, format: :json)
end
