json.array!(@loci) do |locus|
  json.extract! locus, :id, :name, :locus_type, :chromosome, :region, :position, :exclude, :str_unit, :flank5, :snp_iub, :flank3
  json.url locus_url(locus, format: :json)
end
