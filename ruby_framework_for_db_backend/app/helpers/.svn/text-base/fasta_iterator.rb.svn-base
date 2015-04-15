# This class provides an object model for accessing FASTA sequences from
# a FASTA sequence library input text file.
#
# Author::      Darrell O. Ricke, Ph.D.  (mailto: d_ricke@yahoo.com)
# Copyright::   Copyright (C) 2000 Darrell O. Ricke, Ph.D., Paragon Software

require 'input_file.rb'
require 'fasta_sequence.rb'
require 'seq_tools.rb'

###############################################################################
class FastaIterator < InputFile
# Attributes:
# - end_of_file - the current end-of-file status (0 = false; 1 = true)
# - line - the current line of the input text file.
# - name - the name of the input text file.

# fasta sequenes read from the current FASTA file
  attr_reader :fastas

###############################################################################
# Create the FastaIterator object on named FASTA sequence library file.
  def initialize(name)
    super(name) # initialize InputFile
    @fasta = nil
    @fastas = {}
  end

  # method initialize

###############################################################################
# Return all of the FASTA sequences in a hash keyed by sequence name.
  def read_fastas
    @fastas = {}
    while  self.is_end_of_file? == false
      seq = next_sequence
      seq.sequence_data = SeqTools.trim_ns(seq.sequence_data) if !seq.nil?
      @fastas[seq.sequence_name] = seq if (!seq.nil?) && (seq.sequence_data.length > 0)
    end # while

    @fastas
  end

  # method read_fastas

###############################################################################
# Return all of the FASTA sequence names in a hash keyed by sequence name.
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
# Return all of the FASTA sequences in to an array.
  def fastas_to_array
    @fastas = []
    while  self.is_end_of_file? == false
      seq = next_sequence
      if (!seq.nil?) && (seq.sequence_data.length > 0)
        @fastas << seq
      end # if
    end # while

    @fastas
  end

  # method fastas_to_array

###############################################################################
# Return the next FASTA header line - skipping sequence data.
  def next_header
    # Find the start of the next sequence.
    while  (self.is_end_of_file? == false) &&
        (not (@line =~ /^>/))
      next_line
    end # while

    # Check for end of file.
    return '' if  @end_of_file == 1

    @line # return the header line
  end

  # method next_header

###############################################################################
# Get the next sequence from the FASTA library file.
  def next_sequence
    # Advance to the next FASTA header line.
    next_header

    # Create a new FASTA sequence object.
    @fasta = FastaSequence.new('', '', '', '')

    # Parse the header line.
    @fasta.parse_header(@line)

    # Read in the sequence data.
    next_line
    seq = ''
    while  (self.is_end_of_file? == false) &&
        (not (@line =~ /^>/))
      seq = seq + @line.chomp
      next_line
    end # while
    @fasta.sequence_data = seq

    @fasta
  end # method next_sequence
end # class FastaIterator

###############################################################################
# Testing module.
def test_fasta_iterator
  in_fasta = FastaIterator.new('test.data')
  in_fasta.open_file
  while  in_fasta.is_end_of_file? == false
    fasta = in_fasta.next_sequence
    if  fasta != nil
      print 'name = ', fasta.sequence_name, ' '
      print 'desc = ', fasta.sequence_description, "\n"
      print 'seq  = ', fasta.sequence_data, "\n"
      puts
    end # if
  end # while
  in_fasta.close_file
end # method test_fasta_iterator

###############################################################################
# test_fasta_iterator()
