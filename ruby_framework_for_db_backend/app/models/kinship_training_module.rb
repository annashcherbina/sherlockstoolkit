class KinshipTrainingModule < ActiveRecord::Base
  validates :name, uniqueness: true
end
