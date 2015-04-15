json.array!(@strs) do |str|
  json.extract! str, :id, :experiment_id, :primer_id, :locus_id, :sample_id, :name, :is_stutter, :is_novel_allele, :is_novel_flank, :novel_flank_name, :flank5, :flank3, :str_call
  json.url str_url(str, format: :json)
end
