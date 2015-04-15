require 'fasta_sequence.rb'

# This class provides an object model for a FASTQ sequence (header line, sequence, quality).
#
# Author::    	Darrell O. Ricke, Ph.D.  (mailto: Darrell.Ricke@ll.mit.edu)

###############################################################################
class FastqSequence < FastaSequence
# quality - ascii values of quality string
  attr_accessor :quality
# quality_offset - starting zero value for quality encoding
  attr_accessor :quality_offset
# sequence_quality - FASTQ quality string for this sequence
  attr_accessor :sequence_quality

###############################################################################
# Create a new FASTA sequence object.
  def initialize(name, desc, seq, seq_type, seq_qual)
    super(name, desc, seq, seq_type)
    @quality_offset = 33
    parse_quality(seq_qual)
  end

  # method initialize

###############################################################################
# This method parses the sequence quality string to integer values
  def parse_quality(seq_qual)
    @sequence_quality = seq_qual
    @quality = []
    seq_qual.each_byte do |byte|
      # p=exp[ (ord(c) - 33) / ( -10 * log(10) )
      @quality << byte - @quality_offset
    end # do
  end

  # method parse_quality

###############################################################################
# Generates a FASTA string for this sequence.
  def to_fasta
    return '' if @sequence_name.nil?
    @sequence_description = '' if @sequence_description.nil?
    str = '>' + @sequence_name + ' ' + @sequence_description + "\n"
    seq_start = 0
    seq_end = 50

    while  seq_end < @sequence_data.length
      str += @sequence_data[seq_start...seq_end] + "\n"
      seq_start = seq_end
      seq_end += 50
    end # while

    str += @sequence_data[seq_start...@sequence_data.length] + "\n"
    str
  end

  # method to_string

###############################################################################
# Generates a FASTQ string for this sequence.
  def to_string
    return '' if @sequence_name.nil?
    @sequence_description = '' if @sequence_description.nil?
    str = '@' + @sequence_name + ' ' + @sequence_description + "\n"
    seq_start = 0
    seq_end = 50

    while  seq_end < @sequence_data.length
      str += @sequence_data[seq_start...seq_end] + "\n"
      seq_start = seq_end
      seq_end += 50
    end # while

    str += @sequence_data[seq_start...@sequence_data.length] + "\n+\n"

    qual_start = 0
    qual_end = 50
    while  qual_end < @sequence_quality.length
      str += @sequence_quality[qual_start...qual_end] + "\n"
      qual_start = qual_end
      qual_end += 50
    end # while

    str += @sequence_quality[qual_start...@sequence_quality.length] + "\n"
    str
  end # method to_string

###############################################################################
end # FastqSequence

###############################################################################
# Testing module.
def test_fastq_sequence
  fastq = FastqSequence.new('AB00001', "/name=\"fun\" /gene=\"test\"", 'ACGTGTCATAGCAT', 'DNA', "'-/#.!)(&$,*%)")
  fastq.parse_header(">AB00001 /name=\"fun\" /gene=\"test\" ")
  print 'name = ', fastq.sequence_name, "\n"
  print 'desc = ', fastq.sequence_description, "\n"
  fastq.parse_annotation
  fastq.parse_quality(fastq.sequence_quality)
  print 'seq  = ', fastq.sequence_data, "\n"
  print 'qual = ', fastq.quality, "\n"
end # method test_fastq_sequence

# test_fastq_sequence()
