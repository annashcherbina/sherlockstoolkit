def patch_all_samples
  puts "Begin #{Time.now}"
  sample_hash = {}
  Sample.all.each do |sample|
    sample_hash[sample.id] = 0
  end

  puts "Making Calls Hash #{Time.now}"
  calls_hash = Tools::to_hash(Call.all)
  calls_hash.each do |call_id, call|
    sample_hash[call.sample_id] += call.total_count
  end

  puts "Begin Updating each Sample #{Time.now}"
  sample_hash.each do |k, v|
    Sample.update(k, total_reads: v)
  end

  puts "Completed, All Samples have been updated, #{Time.now}"
end

#patch_all_samples