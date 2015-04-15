json.array!(@instruments) do |instrument|
  json.extract! instrument, :id, :name
  json.url instrument_url(instrument, format: :json)
end
