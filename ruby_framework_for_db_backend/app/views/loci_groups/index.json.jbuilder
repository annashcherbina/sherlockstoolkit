json.array!(@loci_groups) do |loci_group|
  json.extract! loci_group, :id, :name
  json.url loci_group_url(loci_group, format: :json)
end
