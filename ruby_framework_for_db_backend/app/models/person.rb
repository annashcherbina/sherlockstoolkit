class Person < ActiveRecord::Base
  has_many :person_samples
  has_many :samples, through: :person_samples
  belongs_to :best_sample, foreign_key: "best_sample_id", class_name: "Sample"

  validates :id_code, uniqueness: true

  scope :sorted_by_id_code, lambda { order('people.id_code+0<>0 DESC, people.id_code+0, people.id_code') }
end