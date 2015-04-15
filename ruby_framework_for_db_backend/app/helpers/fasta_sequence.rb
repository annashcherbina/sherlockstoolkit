# This class provides an object model for a FASTA sequence (header line, sequence).
#
# Author::    	Darrell O. Ricke, Ph.D.  (mailto: d_ricke@yahoo.com)

require 'seq_tools.rb'

###############################################################################
class FastaSequence
# annotation - current sequence annotation
  attr_accessor :annotation
# flag - processing flag
  attr_accessor :flag
# partial - partial sequence flag
  attr_accessor :partial
# sequence_data - current sequence data.
  attr_accessor :sequence_data
# sequence_description - current sequence description.
  attr_accessor :sequence_description
# sequence_name - current sequence name.
  attr_accessor :sequence_name
# sequence_type - current sequence type.
  attr_accessor :sequence_type

###############################################################################
# Create a new FASTA sequence object.
  def initialize
    @annotation = {} # sequence annotation
    @flag = nil # processing flag
    @partial = false # partial sequence flag
    @sequence_data = '' # sequence
    @sequence_description = '' # sequence description
    @sequence_name = '' # sequence name
    @sequence_type = '' # sequence type
  end

  # method initialize

###############################################################################
# Create a new FASTA sequence object.
  def initialize(name, desc, seq, seq_type)
    @annotation = {} # sequence annotation
    @flag = nil # processing flag
    @partial = false # partial sequence flag
    @sequence_data = seq # sequence
    @sequence_description = desc # sequence description
    @sequence_name = name # sequence name
    @sequence_type = seq_type # sequence type
  end

  # method initialize

###############################################################################
  def blank_ends
    @sequence_data = SeqTools.blank_ends(@sequence_data)
  end

  # blank_ends

###############################################################################
# Counts the number of gap characters to determine if partial sequence.
  def check_partial(max_length)
    @partial = true

    # Check for a partial length sequence
    return if @sequence_data.length < (3 * max_length) / 4

    gaps = 0

    # Assert: sequence data
    return if (@sequence_data.nil?) || (@sequence_data.length < 1)

    # Count the gap characters in the sequence.
    for i in 0...@sequence_data.length do
      residue = @sequence_data[i, 1]
      gaps += 1 if (residue == '-') || (residue == '.')
    end # do

    # Define a partial sequence as having less than 25% of the length missing.
    @partial = (gaps >= @sequence_data.length / 4)
  end

  # method check_partial

###############################################################################
  def reverse_compliment
    SeqTools.reverse_compliment(@sequence_data)
  end

  # method reverse_compliment

###############################################################################
  def parse_annotation
    @annotation = SeqTools.parse_annotation(@sequence_description)
  end

  # parse_annotation

###############################################################################
  def parse_header(line)
    @sequence_name, @sequence_description = SeqTools.parse_header(line)
  end

  # parse_header

###############################################################################
# Generates a FASTA string of this sequence.
  def to_string
    return '' if @sequence_name.nil?

    str = '>' + @sequence_name + ' ' + @sequence_description + "\n"
    str += SeqTools.to_blocks(@sequence_data)
    str
  end # method to_string

###############################################################################
end # FastaSequence

###############################################################################
# Testing module.
def test_fasta_sequence
  fasta = FastaSequence.new
  fasta.parse_header(">AB00001 /name=\"fun\" /gene=\"test\" ")
  fasta.sequence_data = 'ACGT'
  print 'name = ', fasta.sequence_name, "\n"
  print 'desc = ', fasta.sequence_description, "\n"
  fasta.parse_annotation
  print 'seq  = ', fasta.sequence_data, "\n"
end # method test_fata_sequence

# test_fasta_sequence()
