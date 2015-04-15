class Panel < ActiveRecord::Base

  belongs_to :attachment
  has_many :barcodes
  has_many :primers
  has_many :panel_loci
  has_many :loci, through: :panel_loci

  validates :description, presence: true
  validate :has_valid_attachment

  PANEL_TYPE = ["Barcodes", "Primers", "SNP References"]

  def datafile=(input_data)
    self.attachment_id = Attachment::panel_datafile(input_data, self.description, self.panel_type)
    self.name = input_data.original_filename
  end # datafile=

  private

  def self.make_snp_loader_hash
    hash = {}

    Panel.where(panel_type: 'SNP References').each do |panel|
      hash[panel.description] = panel
    end

    hash
  end


  def has_valid_attachment
    if attachment.nil?
      errors[:base] << 'No experiment file selected for upload, or file by same name is already uploaded!'
    else
      case panel_type
        when "Barcodes"
          bool_valid = BarcodeLoader::validate(attachment)
        when "Primers"
          bool_valid = PrimerLoader::validate(attachment)
        when "SNP References"
          bool_valid = LocusLoader::validate(attachment)
        else
          false
      end
      errors[:base] << "The experiment file is an invalid file." if !bool_valid
    end
  end #has_valid_attachment

end # class
