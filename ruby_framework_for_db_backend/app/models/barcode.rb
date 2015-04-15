class Barcode < ActiveRecord::Base
  belongs_to :panel
  has_many :samples
  has_many :comparisons

  private
  def self.make_snp_loader_hash
    hash = {}

    Barcode.all.each do |barcode|
      hash[barcode.name] = barcode
    end

    hash
  end
end
