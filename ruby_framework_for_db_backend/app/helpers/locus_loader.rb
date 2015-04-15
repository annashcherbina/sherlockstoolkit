class LocusLoader
  #attachment is the fasta file
  def self.load_loci(attachment, panel_id)
    Locus.transaction do
      qualities = [0, 20, 30, 40]
      tokens = attachment.contents.split(/\n>/)

      tokens.each do |token|
        locus_parts = token.split("\n")
        #header is the first line
        header = locus_parts[0]
        #discarding the header
        locus_parts.shift
        #the body is everything else joined together but without the newlines
        body = locus_parts.join.delete("\n\r")

        #getting the header parts
        header_parts = header.split(' ')
        #name is the first part of the header
        fasta_sequence_name = header_parts[0]
        #description is the second part of the header
        fasta_sequence_description = header_parts[1]
        locus_name = fasta_sequence_name.split('|').last

        locus = Locus.where(name: locus_name).first_or_create

        pos_pattern = Regexp.new('pos=\\d+')
        num_pattern = Regexp.new('\\d+')
        locus_pos = num_pattern.match(pos_pattern.match(fasta_sequence_description).to_s).to_s.to_i

        #if the locus is not populated yet, go ahead and do it
        if !locus_pos.nil? && locus.locus_type.nil?
          flank5 = body[0...(locus_pos - 1)]
          #trims flank5 to proper length if it is greater than 500 characters
          flank5 = flank5[(flank5.length - 500)..-1] if flank5.length > 500
          snp_iub = body[locus_pos - 1]
          flank3 = body[locus_pos..-1]
          #trims flank3 to proper length if it is greater than 500 characters
          flank3 = flank3[0...500] if flank3.length > 500

          locus.update(locus_type: 'SNP', exclude: false, flank5: flank5, snp_iub: snp_iub, flank3: flank3)
        end #if

        #creating the PanelLocus entry
        qualities.each do |quality|
          PanelLocus.where(panel_id: panel_id, locus_id: locus.id, quality_thresh: quality).first_or_create
        end
      end # token.each
    end #transaction
  end #load loci

  #simply checks if the contents is a string that starts with a '>' sign
  def self.validate(attachment)
    attachment.contents.respond_to?(:starts_with?) && attachment.contents.starts_with?('>')
  end
end # class