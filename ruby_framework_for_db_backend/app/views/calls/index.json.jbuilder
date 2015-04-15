json.array!(@calls) do |call|
  json.extract! call, :id, :experiment_id, :locus_id, :sample_id, :minor_allele_frequency, :total_count, :forward_count, :is_good_thresh_fifty
  json.url call_url(call, format: :json)
end
