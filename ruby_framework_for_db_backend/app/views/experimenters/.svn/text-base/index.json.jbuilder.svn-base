json.array!(@experimenters) do |experimenter|
  json.extract! experimenter, :id, :experiment_id, :person_id, :role, :empcr, :uncertain_empcr, :seq, :uncertain_seq
  json.url experimenter_url(experimenter, format: :json)
end
