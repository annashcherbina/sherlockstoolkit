import scala.collection.mutable.{ArrayBuffer, Map}

// ****************************************************************************
class FastaIterator( file_name: String ) extends InputFile( file_name ) {
  
  private[this] var fasta: FastaSequence = null

  // **************************************************************************
  def get_fasta: FastaSequence = fasta

  // **************************************************************************
  def fastas(): ArrayBuffer[FastaSequence] = {
    val seqs: ArrayBuffer[FastaSequence] = ArrayBuffer()

    // Read in all of the sequences
    while ( end_of_file == false ) {
      next
      seqs += fasta
    }  // while

    seqs
  }  // fastas

  // **************************************************************************
  def micro_rnas( species: String ): Map[String, String] = {
    val seqs = collection.mutable.Map[String, String]()

    // Read in all of the sequences
    while ( end_of_file == false ) {
      next
      if ( fasta.description contains species ) {
        fasta.sequence = fasta.sequence.replace( 'U', 'T' )
        seqs += (fasta.sequence -> fasta.name)
      }  // if
    }  // while

    seqs
  }  // micro_rnas

  // **************************************************************************
  def next: FastaSequence = {
    fasta = new FastaSequence()

    // println( "FastaIterator.next: line = " + line )

    fasta.parseHeader( line )

    readSequence()

    fasta
  }  // method next

  // **************************************************************************
  def countSequences: Int = {
    var count: Int = 0

    next_line
    while ( end_of_file == false ) {
      if ( line.charAt( 0 ) == '>' ) 
        count += 1
      next_line
    }  // while

    count
  }  // method countSequences


  // **************************************************************************
  def readSequence() {
    var seq: String = ""

    next_line
    while ( ( end_of_file == false ) && ( line.charAt( 0 ) != '>' ) )
    {
      if ( line.charAt( 0 ) != '>' )
      {
        seq += line
        next_line
      }  // if
    }  // while

    // println( "FastaIterator.readSequence: seq = " + seq )

    fasta.sequence = seq
  }  // method readSequence


  // **************************************************************************

}  // class FastaIterator
