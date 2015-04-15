module AttachmentsHelper
  def map_params(description)
    #gets a lookup array from Ancestries, in the form of an Array of tuples, [source_description, person_sample_id]
    lookup_array = Ancestry.uniq.pluck(:source_description, :person_sample_id)
    #makes the lookup_array into a hash for ease of use
    lookup_hash = Hash[ lookup_array ]


    description_lines = description.split(/\n/)
    target_person_sample_ids=[]
    description_lines.each do |line|
      target_person_sample_ids << lookup_hash[line] unless lookup_hash[line].nil?
    end
    target_person_sample_ids
  end
end
