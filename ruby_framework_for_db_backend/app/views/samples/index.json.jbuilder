json.array!(@samples) do |sample|
  json.extract! sample, :id, :experiment_id, :barcode_id, :is_good, :is_mixture, :minor_alleles_called
  json.url sample_url(sample, format: :json)
end
