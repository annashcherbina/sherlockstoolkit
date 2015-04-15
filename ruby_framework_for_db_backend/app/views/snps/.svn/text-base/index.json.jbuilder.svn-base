json.array!(@snps) do |snp|
  json.extract! snp, :id, :experiment_id, :primer_id, :locus_id, :sample_id, :allele_base, :count, :forward_qual, :reverse_qual, :is_minor, :flank5, :flank3
  json.url snp_url(snp, format: :json)
end
