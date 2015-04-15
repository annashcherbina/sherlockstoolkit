json.array!(@frequencies) do |frequency|
  json.extract! frequency, :id, :locus_id, :geographic_id, :allele_frequency, :source
  json.url frequency_url(frequency, format: :json)
end
