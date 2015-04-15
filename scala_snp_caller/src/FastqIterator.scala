import scala.collection.mutable.ArrayBuffer

// ****************************************************************************
class FastqIterator( file_name: String ) extends InputFile( file_name ) {

  var fastq: FastqSequence = null

  // **************************************************************************
  def fastqs(): ArrayBuffer[FastqSequence] = {
    val seqs: ArrayBuffer[FastqSequence] = ArrayBuffer()

    // Read in all of the sequences
    while ( end_of_file == false ) {
      next
      seqs += fastq
    }  // while

    seqs
  }  // fastqs

  // **************************************************************************
  def micro_rnas( species: String ): ArrayBuffer[FastqSequence] = {
    val seqs: ArrayBuffer[FastqSequence] = ArrayBuffer()

    // Read in all of the sequences
    while ( end_of_file == false ) {
      next
      if ( fastq.description contains species ) {
        println( "Human: " + fastq.name + " " + fastq.description )
        fastq.sequence = fastq.sequence.replace( 'U', 'T' )
        seqs += fastq
      }  // if
    }  // while

    seqs
  }  // fastqs

  // **************************************************************************
  def next(): FastqSequence = {
    fastq = new FastqSequence()

    fastq.parseHeader( line, '@' )

    readEntry()
  }  // method next

  // **************************************************************************
  def readEntry(): FastqSequence = {
    var seq: String = ""
    var qual: String = ""

    next_line()
    while ( ( end_of_file == false ) && ( line.charAt( 0 ) != '+' ) )
    {
      if ( line.charAt( 0 ) != '+' )
      {
        seq += line
        next_line()
      }  // if
    }  // while
    fastq.sequence = seq

    // Read in the quality letters.
    next_line()
    while ( ( end_of_file == false ) && ( qual.length < seq.length ) )
    {
      qual += line
      next_line()
    }  // while
    fastq.quality = qual

    if ( qual.length != seq.length )
      println( "*Warning* sequence length != quality length:\n" + seq + "\n" + qual + "\n" )
     
    //println("seq:"+fastq.sequence)
    //println("qual:"+fastq.quality)
    fastq
  }  // method readEntry

  // **************************************************************************

}  // class FastqIterator
