class PrimerLoader

  def self.load_primers(attachment, panel_id)
    Primer.transaction do

      lines = attachment.contents.split("\n")

      lines.each do |line|
        line.chomp!
        PrimerLoader::process_line(line, panel_id) if line.length > 0
      end
    end
  end

  # load_primers

  def self.process_line(line, panel_id)
    tokens = line.split("\t")

    locus_id = Locus.where(name: tokens[0]).first_or_create.id

    forward_primer_hash = {}
    forward_primer_hash[:panel_id] = panel_id
    forward_primer_hash[:locus_id] = locus_id
    forward_primer_hash[:is_forward] = true
    forward_primer_hash[:sequence] = tokens[1]

    reverse_primer_hash = {}
    reverse_primer_hash[:panel_id] = panel_id
    reverse_primer_hash[:locus_id] = locus_id
    reverse_primer_hash[:is_forward] = false
    reverse_primer_hash[:sequence] = tokens[2]


    #forward primer
    Primer.where(forward_primer_hash).first_or_create

    #backward primer
    Primer.where(reverse_primer_hash).first_or_create
  end

  # process_line
  def self.validate(attachment)
    tokens = attachment.contents.split("\n")
    if tokens[0].nil?
      false
    else
      tokens[0].split("\t").length == 3
    end
  end # validation
end # class
