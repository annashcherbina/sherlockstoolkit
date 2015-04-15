class LociGroup < ActiveRecord::Base
  validates :name, uniqueness: true, presence: true
  has_and_belongs_to_many :loci

  private
  #inserts into the join table between loci and loci_groups that dictate which loci are in which loci_groups
  def self.create_group(loci_group_id, file_data)
    locus_names = file_data.read.split.map{|i| i.split[0].chomp}

    locus_hash = Hash[Locus.pluck(:name, :id)]

    locus_ids = Set.new
    invalid_names = Set.new

    locus_names.each do |name|
      next if name.empty?
      locus_id = locus_hash[name]
      if locus_id.nil?
        invalid_names.add(name)
      else
        locus_ids.add(locus_hash[name])
      end
    end

    value_string = locus_ids.map{|v| "(#{v}, #{loci_group_id})" }.join(',')
    insert_sql = "insert into loci_loci_groups (locus_id, loci_group_id) values #{value_string}"
    ActiveRecord::Base.connection.execute insert_sql

    invalid_names
  end
end