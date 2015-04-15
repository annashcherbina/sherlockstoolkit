class Call < ActiveRecord::Base
  belongs_to :experiment
  belongs_to :locus
  belongs_to :sample
  has_and_belongs_to_many :comparisons

end
