json.array!(@experiments) do |experiment|
  json.extract! experiment, :id, :instrument_id, :hash, :name, :is_mixture, :call_url, :run_date
  json.url experiment_url(experiment, format: :json)
end
