json.array!(@primers) do |primer|
  json.extract! primer, :id, :name, :is_forward, :sequence
  json.url primer_url(primer, format: :json)
end
