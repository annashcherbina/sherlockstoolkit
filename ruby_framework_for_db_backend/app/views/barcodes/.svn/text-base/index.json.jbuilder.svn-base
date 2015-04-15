json.array!(@barcodes) do |barcode|
  json.extract! barcode, :id, :experiment_id, :panel_id, :barcode_type, :is_mixture, :minor_alleles_called
  json.url barcode_url(barcode, format: :json)
end
