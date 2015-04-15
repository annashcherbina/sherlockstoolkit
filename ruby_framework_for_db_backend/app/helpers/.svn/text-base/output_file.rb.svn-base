# This class provides an object model for an output file.
#
# Author::      Darrell O. Ricke, Ph.D.  (mailto: d_ricke@yahoo.com)
# Copyright::   Copyright (C) 2000 Darrell O. Ricke, Ph.D., Paragon Software

###############################################################################
class OutputFile
# lines - the number of lines written to the output text file
  attr_accessor :lines
# file_name - the name of the output file
  attr_accessor :file_name

###############################################################################
# Create an output object for the named file.
  def initialize(n)
    @lines = 0 # lines written
    close_file # close the file
    @file = nil
    @file_name = n # set the file name
  end

  # method initialize

###############################################################################
# Open the output file.
  def open_file
    @file = File.new(@file_name, 'w')
  end

  # method open_file

###############################################################################
# Close the output file.
  def close_file
    @file.close unless @file.nil? # close file
  end

  # method close_file

###############################################################################
# Delete the file.
  def delete_file
    close_file # close the file if open
    File.delete(@file_name) # delete the file by name
  end

  # method delete_file

###############################################################################
# Write a text string to the output text file.
  def write(text)
    begin
      @file.print(text) unless @file.nil?
      @lines += 1
    rescue
      print 'Write error'
    end # begin
  end

  # method write

###############################################################################
# Write a binary data to the output file.
  def write_binary(data)
    begin
      @file.binmode
      @file.write(data) unless @file.nil?
    rescue
      print 'write_binary error'
    end
  end # method write_binary
end # class OutputFile

###############################################################################
# Testing module.
def test_output_file
  file = OutputFile.new('test.data')
  file.open_file
  file.write(">Seq1 This is a FASTA sequence file.\n")
  file.write("ACGTACGTACGT\n")
  file.write(">Seq2 This second sequence in the file.\n")
  file.write("AAAACCCCGGGGTTTT\n")
  file.close_file
  print 'The number of lines written is ', file.lines, "\n"
end # method test_output_file

# test_output_file()
