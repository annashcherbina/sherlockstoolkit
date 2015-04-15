json.array!(@comparisons) do |comparison|
  json.extract! comparison, :id, :barcode_id, :barcode2_id, :tp_count, :fp_count, :fn_count, :tn_count, :ma_threshold1, :ma_threshold2, :rmne, :likelihood_ratio
  json.url comparison_url(comparison, format: :json)
end
