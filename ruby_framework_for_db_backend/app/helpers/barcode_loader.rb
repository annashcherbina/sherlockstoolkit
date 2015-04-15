class BarcodeLoader
###############################################################################
  def self.load_barcodes(attachment, panel_id)
    Barcode.transaction do

      lines = attachment.contents.split("\n")

      lines.each do |line|
        line.chomp!
        BarcodeLoader::process_line(line, panel_id) if line.length > 0
      end
    end
  end

  # load_barcodes


  ###############################################################################
  def self.process_line(line, panel_id)
    tokens = line.split("\t")

    bc_hash = {}
    bc_hash[:name] = tokens[0]
    bc_hash[:panel_id] = panel_id
    bc_hash[:barcode_seq] = tokens[1]
    bc_hash[:barcode_type] = 'single'

    Barcode.where(bc_hash).first_or_create
  end

  # process line

  def self.validate(attachment)
    tokens = attachment.contents.split("\n")
    if tokens[0].nil?
      false
    else
      tokens[0].split("\t").length == 2
    end
  end # validation
end # class