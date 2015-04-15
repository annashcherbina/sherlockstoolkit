class Attachment < ActiveRecord::Base
  has_and_belongs_to_many :parameters
  has_many :experiment
  has_many :panel
  belongs_to :user
  belongs_to :folder

  validates :file_name, uniqueness: true

  scope :has_content, lambda { where("attachments.content_type is NOT NULL") }

  def datafile=(input_data)
    self.file_name = input_data.original_filename
    self.content_type = input_data.content_type.chomp
    self.contents = input_data.read
    self.content_bytes = self.contents.size
  end


  def self.panel_datafile(input_data, description, panel_type)
    return nil if input_data == '' || input_data.nil? #no file name was entered
    attachment = Attachment.new
    attachment.user_id = User.find_by_name('SYSTEM').id
    attachment.folder_id = Folder.find_by_name('Panel Data').id
    attachment.file_name = input_data.original_filename
    attachment.description = description
    attachment.file_type = panel_type
    attachment.content_type = input_data.content_type.chomp
    attachment.contents = input_data.read
    attachment.content_bytes = attachment.contents.size
    attachment.save
    attachment.id
  end

  # datafile

  def self.grab_shortinfo(folder_id)
    sql_cmd = "SELECT id, file_name from attachments where folder_id=#{folder_id}"
    info = Attachment.find_by_sql(sql_cmd)
    info
  end
end # Attachment
