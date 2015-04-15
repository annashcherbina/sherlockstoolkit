# This class provides an object model for accessing FASTQ sequences from
# a FASTQ sequence library input text file.
#
# Author::      Darrell O. Ricke, Ph.D.  (mailto: Darrell.Ricke@ll.mit.edu)

require 'input_file.rb'
require 'fastq_sequence.rb'

###############################################################################
class FastqIterator < InputFile
# Attributes:
# - end_of_file - the current end-of-file status (0 = false; 1 = true)
# - line - the current line of the input text file.
# - name - the name of the input text file.

# fastq sequences read from the current FASTQ file
  attr_reader :fastqs

###############################################################################
# Create the FastqIterator object on named FASTQ sequence library file.
  def initialize(name)
    super(name) # initialize InputFile
    @fastq = nil
    @fastqs = {}
  end

  # method initialize

###############################################################################
# Return all of the FASTQ sequences in a hash keyed by sequence name.
  def read_fastqs
    @fastqs = {}
    while  self.is_end_of_file? == false
      seq = next_sequence
      seq.sequence_data = SeqTools.trim_ns(seq.sequence_data) if !seq.nil?
      @fastqs[seq.sequence_name] = seq if (!seq.nil?) && (seq.sequence_data.length > 0)
    end # while

    @fastqs
  end

  # method read_fastqs

###############################################################################
# Return all of the FASTQ sequence names in a hash keyed by sequence name.
  def read_names
    @names = {}
    while  self.is_end_of_file? == false
      seq = next_sequence
      @names[seq.sequence_name] = true if (!seq.nil?) && (seq.sequence_data.length > 0)
    end # while

    @names
  end

  # method read_names

###############################################################################
# Return all of the FASTQ sequences in to an array.
  def fastqs_to_array
    @fastqs = []
    while  self.is_end_of_file? == false
      seq = next_sequence
      if (!seq.nil?) && (seq.sequence_data.length > 0)
        @fastqs << seq
      end # if
    end # while

    @fastqs
  end

  # method fastqs_to_array

###############################################################################
# Get the next sequence from the FASTQ library file.
  def next_sequence
    # Create a new FASTQ sequence object.
    @fastq = FastqSequence.new('', '', '', '', '')

    # Parse the header line.
    @fastq.parse_header(@line.chomp)

    # puts "head: #{@line}"
    # Read in the sequence data.
    next_line
    # @fastq.sequence_data = @line.chomp
    seq = ''
    while  (self.is_end_of_file? == false) &&
        (@line[0] != '+')
      seq = seq + @line.chomp
      next_line
    end # while
    @fastq.sequence_data = seq
    # puts "seq : #{seq[0...20]}...#{seq[-20..-1]}"

    # self.next_line  # + line
    # puts "plus: #{@line}"

    # Read in the quality data.
    next_line
    # @fastq.sequence_quality = @line.chomp
    qual = ''
    while  (self.is_end_of_file? == false) &&
        (qual.size < seq.size)
      qual = qual + @line.chomp
      next_line
    end # while
    @fastq.sequence_quality = qual
    # puts "qual: #{qual[0...20]}...#{qual[-20..-1]}"
    # puts "seq.size #{seq.size} : qual.size #{qual.size}"

    @fastq
  end # method next_sequence
end # class FastqIterator

###############################################################################
# Testing module.
def test_fastq_iterator
  in_fastq = FastqIterator.new('test.fastq')
  in_fastq.open_file
  in_fastq.next_line
  while  in_fastq.is_end_of_file? == false
    fastq = in_fastq.next_sequence
    if  fastq != nil
      print 'name = ', fastq.sequence_name, ' '
      print 'desc = ', fastq.sequence_description, "\n"
      print 'seq  = ', fastq.sequence_data, "\n"
      fastq.parse_quality(fastq.sequence_quality)
      print 'qual = ', fastq.quality, "\n"
      puts
      puts fastq.to_fasta
    end # if
  end # while
  in_fastq.close_file
end # method test_fastq_iterator

###############################################################################
# test_fastq_iterator()
