class Folder < ActiveRecord::Base
  belongs_to :parent, class_name: :Folder, foreign_key: :parent_id
  has_many :children, class_name: :Folder, foreign_key: :parent_id
  belongs_to :user
  has_many :attachments#, dependent: :destroy
  has_many :images#, dependent: :destroy

  def is_empty?
    self.children.empty? && self.attachments.empty? && self.images.empty? ? true : false
  end

end
