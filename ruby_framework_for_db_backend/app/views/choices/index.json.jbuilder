json.array!(@choices) do |choice|
  json.extract! choice, :id, :attribute_id, :name
  json.url choice_url(choice, format: :json)
end
