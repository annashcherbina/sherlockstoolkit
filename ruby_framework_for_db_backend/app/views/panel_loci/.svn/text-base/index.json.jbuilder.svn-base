json.array!(@panel_loci) do |panel_locus|
  json.extract! panel_locus, :id, :panel_id, :locus_id, :exclude, :ambiguous, :low, :strand_bias
  json.url panel_locus_url(panel_locus, format: :json)
end
