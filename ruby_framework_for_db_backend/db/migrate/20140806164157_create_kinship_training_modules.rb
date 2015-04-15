class CreateKinshipTrainingModules < ActiveRecord::Migration
  def change
    create_table :kinship_training_modules do |t|
      t.references :parameter

      t.string :name, :limit => 255
      t.binary    :estimator_degree,            default: nil, :limit => 4.gigabytes - 1 #longblob
      t.binary    :estimator_relationship,      default: nil, :limit => 4.gigabytes - 1 #longblob
      t.binary    :feature_class_relationship,  default: nil, :limit => 1.megabytes #blob
      t.binary    :normalization,               default: nil, :limit => 1.megabytes #blob
      t.binary    :feature_class_degree,        default: nil, :limit => 1.megabytes #blob
    end
  end
end
