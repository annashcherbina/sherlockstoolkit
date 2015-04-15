class User < ActiveRecord::Base
  has_many :folders
  has_many :images
  has_many :attachments
  belongs_to :home_folder, class_name: :Folder, foreign_key: :home_folder_id

  validates :name, presence: true
  validates :is_admin, inclusion: { :in => [true, false] }

  def self.create_with_folder(user_hash)
    user = User.create(user_hash)
    folder_name = user.name.downcase.sub(' ', '_')
    master_user_folder = Folder.find_by_name('Users')
    home_folder = Folder.create(parent_id: master_user_folder.id, user_id: user.id, name: folder_name, description: "#{user.name}'s home folder", level: 1)
    user.update(home_folder_id: home_folder.id)
  end

#############################################################################
  def password
    @password
  end
  # method password


  #############################################################################
  def password=(pwd)
    @password = pwd
    create_new_salt
    self.hashed_password = encrypted_password(self.password, self.salt)
  end
  # method password=


  #############################################################################
  def authenticate(username, password)
    user = self.find_by_username(username)
    if user
      expected_password = encrypted_password(password, user.salt)
      if user.hashed_password != expected_password
        user = nil
      end # if
    end # if
    user
  end

  # method authenticate


  #############################################################################
  def verify_password(password)
    expected_password = encrypted_password(password, self.salt)
    if self.hashed_password != expected_password
      return false
    end # if
    return true
  end

  # method verify_password


  #############################################################################
  private


  #############################################################################
  def create_new_salt
    self.salt = self.object_id.to_s + rand.to_s
  end

  # method create_new_salt


  #############################################################################
  def encrypted_password(password, salt)
    string_to_hash = password + "salad" + salt
    Digest::SHA1.hexdigest(string_to_hash)
  end # method encrypted_password
end
