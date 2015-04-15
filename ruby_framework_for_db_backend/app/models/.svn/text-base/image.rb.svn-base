class Image < ActiveRecord::Base
  belongs_to :folder
  belongs_to :user

  belongs_to :associated_attachment, foreign_key: 'associated_attachment_id', class_name: 'Attachment'
  belongs_to :associated_image, foreign_key: 'associated_image_id', class_name: 'Image'

  #validate :extension_check

  def datafile=(input_data)
    self.name = input_data.original_filename
    self.content_type = input_data.content_type.chomp
    self.picture = input_data.read
    self.picture_bytes = self.picture.size
  end  # datafile

  private

  def extension_check
    if !self.name.end_with?('.png', '.jpeg', '.jpg', '.gif', '.bmp')
      errors[:base] << "Not a valid image file"
    end
  end

  def self.grab_shortinfo(folder_id)
    sql_cmd = "SELECT id, file_name from images where folder_id=#{folder_id}"
    info = Attachment.find_by_sql(sql_cmd)
    info
  end
end