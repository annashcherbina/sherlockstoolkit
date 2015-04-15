json.array!(@allele_references) do |allele_reference|
  json.extract! allele_reference, :id, :locus_id, :allele_name, :allele_sequence, :regular_expression
  json.url allele_reference_url(allele_reference, format: :json)
end
