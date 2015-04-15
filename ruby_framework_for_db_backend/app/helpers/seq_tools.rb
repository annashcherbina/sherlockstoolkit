# This class provides sequence tools.
#
# Author::    	Darrell O. Ricke, Ph.D.  (mailto: darrell.ricke@ll.mit.edu)


###############################################################################
class SeqTools


################################################################################

  @@codons = {"A" => ["gct", "gcc", "gca", "gcg"],
              "C" => ["tgt", "tgc"],
              "D" => ["gat", "gac"],
              "E" => ["gaa", "gag"],
              "F" => ["ttt", "ttc"],
              "G" => ["ggt", "ggc", "gga", "ggg"],
              "H" => ["cat", "cac"],
              "I" => ["att", "atc", "ata"],
              "K" => ["aaa", "aag"],
              "L" => ["ctt", "ctc", "cta", "ctg"],
              "M" => ["atg"],
              "N" => ["aat", "aac"],
              "P" => ["cct", "ccc", "cca", "ccg"],
              "Q" => ["caa", "cag"],
              "R" => ["cgt", "cgc", "cga", "cgg", "aga", "agg"],
              "S" => ["tct", "tcc", "tca", "tcg", "agt", "agc"],
              "T" => ["act", "acc", "aca", "acg"],
              "V" => ["gtt", "gtc", "gta", "gtg"],
              "W" => ["tgg"],
              "Y" => ["tat", "tac"],
              "*" => ["taa", "tag", "tga"]}

  @@map = {"ttt" => "ttc", # Phe
           "ttc" => "ttt", # Phe
           "tta" => "ctc", # L
           "ttg" => "ctt", # L

           "ctt" => "ttg", # L
           "ctc" => "tta", # L
           "cta" => "ttg", # L
           "ctg" => "tta", # L

           "att" => "ata", # I
           "atc" => "ata", # I
           "ata" => "atc", # I
           "atg" => "atg", # M

           "gtt" => "gtg", # V
           "gtc" => "gta", # V
           "gta" => "gtc", # V
           "gtg" => "gtt", # V

           "tct" => "agc", # S
           "tcc" => "agt", # S
           "tca" => "agc", # S
           "tcg" => "agt", # S

           "cct" => "ccg", # P
           "ccc" => "cca", # P
           "cca" => "ccc", # P
           "ccg" => "cct", # P

           "act" => "acg", # T
           "acc" => "aca", # T
           "aca" => "acc", # T
           "acg" => "act", # T

           "gct" => "gcg", # A
           "gcc" => "gca", # A
           "gca" => "gcc", # A
           "gcg" => "gct", # A

           "tat" => "tac", # Y
           "tac" => "tat", # Y
           "taa" => "tga", # ochre
           "tag" => "tga", # amber

           "cat" => "cac", # H
           "cac" => "cat", # H
           "caa" => "cag", # Q
           "cag" => "caa", # Q

           "aat" => "aac", # N
           "aac" => "aat", # N
           "aaa" => "aag", # K
           "aag" => "aaa", # K

           "gat" => "gac", # D
           "gac" => "gat", # D
           "gaa" => "gag", # E
           "gag" => "gaa", # E

           "tgt" => "tgc", # C
           "tgc" => "tgt", # C
           "tga" => "tag", # opal
           "tgg" => "tgg", # W

           "cgt" => "agg", # R
           "cgc" => "aga", # R
           "cga" => "agg", # R
           "cgg" => "aga", # R

           "agt" => "tcg", # S
           "agc" => "tca", # S
           "aga" => "cgc", # R
           "agg" => "cgt", # R

           "ggt" => "ggg", # G
           "ggc" => "gga", # G
           "gga" => "ggc", # G
           "ggg" => "ggt"} # G


  @@translate = {"ttt" => "F", # Phe
                 "ttc" => "F", # Phe
                 "tta" => "L", # L
                 "ttg" => "L", # L

                 "ctt" => "L", # L
                 "ctc" => "L", # L
                 "cta" => "L", # L
                 "ctg" => "L", # L

                 "att" => "I", # I
                 "atc" => "I", # I
                 "ata" => "I", # I
                 "atg" => "M", # M

                 "gtt" => "V", # V
                 "gtc" => "V", # V
                 "gta" => "V", # V
                 "gtg" => "V", # V

                 "tct" => "S", # S
                 "tcc" => "S", # S
                 "tca" => "S", # S
                 "tcg" => "S", # S

                 "cct" => "P", # P
                 "ccc" => "P", # P
                 "cca" => "P", # P
                 "ccg" => "P", # P

                 "act" => "T", # T
                 "acc" => "T", # T
                 "aca" => "T", # T
                 "acg" => "T", # T

                 "gct" => "A", # A
                 "gcc" => "A", # A
                 "gca" => "A", # A
                 "gcg" => "A", # A

                 "tat" => "Y", # Y
                 "tac" => "Y", # Y
                 "taa" => "*", # ochre
                 "tag" => "*", # amber

                 "cat" => "H", # H
                 "cac" => "H", # H
                 "caa" => "Q", # Q
                 "cag" => "Q", # Q

                 "aat" => "N", # N
                 "aac" => "N", # N
                 "aaa" => "K", # K
                 "aag" => "K", # K

                 "gat" => "D", # D
                 "gac" => "D", # D
                 "gaa" => "E", # E
                 "gag" => "E", # E

                 "tgt" => "C", # C
                 "tgc" => "C", # C
                 "tga" => "*", # opal
                 "tgg" => "W", # W

                 "cgt" => "R", # R
                 "cgc" => "R", # R
                 "cga" => "R", # R
                 "cgg" => "R", # R

                 "agt" => "S", # S
                 "agc" => "S", # S
                 "aga" => "R", # R
                 "agg" => "R", # R

                 "ggt" => "G", # G
                 "ggc" => "G", # G
                 "gga" => "G", # G
                 "ggg" => "G", # G

                 # Uppercase
                 "TTT" => "F", # Phe
                 "TTC" => "F", # Phe
                 "TTA" => "L", # L
                 "TTG" => "L", # L

                 "CTT" => "L", # L
                 "CTC" => "L", # L
                 "CTA" => "L", # L
                 "CTG" => "L", # L

                 "ATT" => "I", # I
                 "ATC" => "I", # I
                 "ATA" => "I", # I
                 "ATG" => "M", # M

                 "GTT" => "V", # V
                 "GTC" => "V", # V
                 "GTA" => "V", # V
                 "GTG" => "V", # V

                 "TCT" => "S", # S
                 "TCC" => "S", # S
                 "TCA" => "S", # S
                 "TCG" => "S", # S

                 "CCT" => "P", # P
                 "CCC" => "P", # P
                 "CCA" => "P", # P
                 "CCG" => "P", # P

                 "ACT" => "T", # T
                 "ACC" => "T", # T
                 "ACA" => "T", # T
                 "ACG" => "T", # T

                 "GCT" => "A", # A
                 "GCC" => "A", # A
                 "GCA" => "A", # A
                 "GCG" => "A", # A

                 "TAT" => "Y", # Y
                 "TAC" => "Y", # Y
                 "TAA" => "*", # oChre
                 "TAG" => "*", # Amber

                 "CAT" => "H", # H
                 "CAC" => "H", # H
                 "CAA" => "Q", # Q
                 "CAG" => "Q", # Q

                 "AAT" => "N", # N
                 "AAC" => "N", # N
                 "AAA" => "K", # K
                 "AAG" => "K", # K

                 "GAT" => "D", # D
                 "GAC" => "D", # D
                 "GAA" => "E", # E
                 "GAG" => "E", # E

                 "TGT" => "C", # C
                 "TGC" => "C", # C
                 "TGA" => "*", # opAl
                 "TGG" => "W", # W

                 "CGT" => "R", # R
                 "CGC" => "R", # R
                 "CGA" => "R", # R
                 "CGG" => "R", # R

                 "AGT" => "S", # S
                 "AGC" => "S", # S
                 "AGA" => "R", # R
                 "AGG" => "R", # R

                 "GGT" => "G", # G
                 "GGC" => "G", # G
                 "GGA" => "G", # G
                 "GGG" => "G"} # G


###############################################################################
# This methods replaces leading and trailing gaps with spaces.
  def self.blank_ends(seq)
    # Blank the leading gap characters.
    i = 0
    while (i < seq.length) && (seq[i, 1] == "-")
      seq[i] = ' '
      i += 1
    end # while

    # Blank the trailing gap characters.
    i = seq.length - 1
    while (i > 0) && (seq[i, 1] == "-")
      seq[i] = " "
      i -= 1
    end # while

    return seq
  end

  # method blank_ends


###############################################################################
# Creates a blank sequence of alignment gap characters of specified length.
  def self.blank_seq(length)
    seq = ""
    for i in 0...length do
      seq += "-"
    end # for
    return seq
  end

  # method blank_seq


###############################################################################
# Counts the number of gap characters to determine if partial sequence.
  def check_partial(max_length)
    @partial = true

    # Check for a partial length sequence
    return if (@sequence_data.length < (3 * max_length) / 4)

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
# Method to compare two aligned sequences.
  def self.compare(seq1, seq2)
    identities = 0
    residues = 0

    # Compare the sequences.
    for i in 0...seq2.length do

      # Check within the length of this sequence.
      if i < seq1.length
        residue = seq2[i, 1]

        # Don't count gap characters or unknown residues.
        if (residue != '.') && (residue != '-') && (residue != 'X') && (residue != 'x')

          # Count only identities
          identities += 1 if residue == seq1[i, 1]

          residues += 1
        end # if
      end # if
    end # for

    return identities, residues
  end

  # method compare


###############################################################################
# Parse the FASTA description line for annotation /key=value pairs.
  def self.parse_annotation(description)
    annotation = {}
    tokens = description.split(" /")
    tokens.each do |pair|
      if pair.length > 0
        tuple = pair.strip.split('=')
        annotation[tuple[0].delete('/')] = tuple[1].delete('"') if tuple[1] != nil
      end # if
    end # do
    return annotation
  end

  # method parse_annotation


###############################################################################
# Parse the FASTA header line.
  def self.parse_header(line)
    name = ""
    description = ""
    return name, description if line.nil?

    space = line.index(' ')
    if (space == nil)
      name = line[1..-1]
      name.chomp! if (!name.nil?) && (name.include?("\n"))
      return name, description
    end # if
    name = line[1...space]

    description = line[(space+1)..-1].chomp()

    return name, description
  end

  # method parse_header


###############################################################################
# This method compliments a DNA base.
  def self.compliment(base)
    case base
      when 'A'
        paired = "T"
      when 'a'
        paired = "t"
      when 'C'
        paired = "G"
      when 'c'
        paired = "g"
      when 'G'
        paired = "C"
      when 'g'
        paired = "c"
      when 'T'
        paired = "A"
      when 't'
        paired = "a"
      when 'N'
        paired = "N"
      when 'n'
        paired = "n"
      when 'R'
        paired = "Y"
      when 'r'
        paired = "y"
      when 'Y'
        paired = "R"
      when 'y'
        paired = "r"
      else
        paired = "n"
    end # case

    return paired
  end

  # method compliment


###############################################################################
# This method reverses and compliments a DNA sequence.
  def self.reverse_compliment(seq)
    comp = ""
    for i in 0...seq.size do
      comp << SeqTools.compliment(seq[i..i])
    end # do

    return comp.reverse
  end

  # method reverse_compliment


################################################################################
# This method translates a coding region into amino acids.
  def self.translate(coding)
    protein = ""
    i = 0
    while (i < coding.size)
      codon = ""
      codon = coding[i..(i+2)] if i+2 < coding.size
      amino = @@translate[codon]
      # puts "Bad codon: #{codon}" if amino.nil?
      protein << amino if !amino.nil?
      i += 3
    end # while

    # puts "DNA: " + coding
    # puts "AA-: " + protein

    return protein
  end

  # method translate


###############################################################################
# This method trims N's from the end of the sequence.
  def self.trim_dis(seq)
    seq = trim_pattern(seq, "(GT){8,}.*(GT){10,}")
    seq = trim_pattern(seq, "(AC){8,}.*(AC){10,}")
    return seq
  end

  # method trim_dis


###############################################################################
  def self.trim_pattern(seq, re_pat)
    pattern = Regexp.new(re_pat, Regexp::IGNORECASE)
    match = pattern.match(seq)
    if !match.nil?
      if match.post_match.size < 30 # check if match is near the end of the sequence
        seq = match.pre_match # trim the sequence
      end # if
    end # if

    return seq
  end

  # method trim_pattern


###############################################################################
# This method trims N's from the end of the sequence.
  def self.trim_ns(seq)
    last_char = seq[seq.size - 1]
    while (last_char == 'N') || (last_char == 'n')
      seq = seq[0...(seq.size - 1)]
      last_char = ' '
      last_char = seq[seq.size - 1] if seq.size > 0
    end # while

    return seq
  end

  # method trim_ns


###############################################################################
# Generates the blocks for a sequence.
  def self.to_blocks(seq)
    str = ""
    return str if (seq.nil?) || (seq.length < 1)

    seq_start = 0
    seq_end = 50
    while (seq_end < seq.length)
      str += seq[seq_start...seq_end] + "\n"
      seq_start = seq_end
      seq_end += 50
    end # while

    str += seq[seq_start...seq.length] + "\n"
    return str
  end # method to_blocks


###############################################################################

end # SeqTools

