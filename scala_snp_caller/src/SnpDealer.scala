import scala.actors.Actor
import Actor._
import scala.util.control.Breaks._
import scala.actors.remote.RemoteActor.{ alive, register }
import scala.collection.mutable.Map
import scala.collection.mutable.MutableList

//STRdealder takes fastq file, but SnpDealer should take fastq
class SnpDealer(fastq_name: String, barcode_name: String, ref_name: String, cores: Int, num_reducers: Int, q_min: Int, low_thresh: Int, ambiguous_0: Double, ambiguous_1: Double, ambiguous_2: Double, ambiguous_3: Double) extends Actor {

  // ***************************************************************************
  def shutdown(players: Array[SnpPlayer], reducers: Array[SnpReducer]) {
    players foreach { case (player) => player ! 0.0 }

    reducers foreach { case (reducer) => reducer ! 0.0 }

    exit()
  } // shutdown

  // **************************************************************************
  def compliment(base: Char): Char = {
    base match {
      case 'A' => 'T'
      case 'a' => 't'
      case 'C' => 'G'
      case 'c' => 'g'
      case 'G' => 'C'
      case 'g' => 'c'
      case 'T' => 'A'
      case 't' => 'a'
      case 'N' => 'N'
      case 'n' => 'n'
      case 'R' => 'Y'
      case 'r' => 'y'
      case 'Y' => 'R'
      case 'y' => 'r'
      case '.' => '.'
      case '-' => '-'
      case _   => '?'
    } // match
  } // compliment

  // **************************************************************************
  def reverse_compliment(sequence: String): String = {
    var seq_reverse = new StringBuilder()
    for (i <- sequence.length - 1 to 0 by -1)
      seq_reverse += compliment(sequence.charAt(i))
    seq_reverse.toString()
  } // reverse_compliment

  // ***************************************************************************
  def act() {
    val host = "localhost"
    val word_size = 5
    // scala.actors.Debug.level = 3
    // println( "SnpDealer started" )

    // Read in the sequence barcodes
    val barcode_reader = new TableReader(barcode_name)

    // Read in the STR reference sequences and store them in a dictionary of rs --> 10bp flank forward orientation 1, 10 bp flank reverse orientation 1, 10 bp flank forward orientation 2, 10 bp flank reverse orientation 2

    val ref_reader = new FastaIterator(ref_name)
    val ref_seqs = ref_reader.fastas.tail
    val snp_pos_map: Map[String, Array[String]] = collection.mutable.Map[String, Array[String]]()

    ref_seqs foreach {
      case (ref_fasta) =>
        val header_components = ref_fasta.description.split("\\|").tail
        val rs = "rs" + header_components(0).split("=")(1)
        var snppos: Int = (header_components(1).split("=")(1)).toInt
        var flanksize: Int = (header_components(2).split("=")(1)).toInt
        var alleles: String = (header_components(6).split("=")(1)).trim 	
        var ma: String = (header_components(9).split("=")(1).split(":")(0))
	if (alleles.contains(ma)==false)
	ma=compliment(ma.charAt(0)).toString 
        val f_seq = ref_fasta.sequence.toUpperCase
        val f_5_flank = f_seq.substring(snppos - 11, snppos - 1)
        val f_3_flank = f_seq.substring(snppos, snppos + 10)
        val r_5_flank = reverse_compliment(f_3_flank).toUpperCase
        val r_3_flank = reverse_compliment(f_5_flank).toUpperCase

        snp_pos_map(rs) = Array(f_5_flank, f_3_flank, r_5_flank, r_3_flank, alleles, ma)
    }
    snp_pos_map("No_locus")=Array("NNNNNNNNNN","NNNNNNNNNN","NNNNNNNNNN","NNNNNNNNNN","N/N","N")
    // Start up some compute engines.
    val players = new Array[SnpPlayer](cores)
    for (i <- 1 to cores) {
      players(i - 1) = new SnpPlayer(i, barcode_reader.hash_1, word_size, host, snp_pos_map)
      players(i - 1).start()
    } // for

    // Create the report files.
    val reports = new Reports(fastq_name, num_reducers)

    // Start up the reduce engines.
    val reducers = new Array[SnpReducer](num_reducers)
    val mid_map_for_setup: Map[Int, collection.mutable.MutableList[String]] = collection.mutable.Map[Int, collection.mutable.MutableList[String]]()
    val mid_map: Map[String, Int] = collection.mutable.Map[String, Int]()

    //figure out which reducer to use for which MID 
    var i = 0
    snp_pos_map foreach {
      case (locus, flank_array) =>
        if (mid_map_for_setup.keySet.contains(i)) {
          mid_map_for_setup(i) += locus
        } else {
          mid_map_for_setup += (i -> collection.mutable.MutableList[String]())
          mid_map_for_setup(i) += locus
        }
        mid_map += (locus -> i)
        i = (i + 1) % (num_reducers)
      //println("i:"+i) 
    }

    for (j <- 0 to (num_reducers - 1)) {
      reducers(j) = new SnpReducer(j, mid_map_for_setup(j), barcode_reader.hash_1.keys.toArray, ref_seqs, host, reports, snp_pos_map, q_min, low_thresh, ambiguous_0, ambiguous_1, ambiguous_2, ambiguous_3)
      reducers(j).start()
    }

    // Process the Sequence dataset.
    val chunksize: Int = 2500
    //val chunksize: Int = 250
    val fastq_iterator: FastqIterator = new FastqIterator(fastq_name)

    fastq_iterator.next_line
    alive(19000)
    register('SnpDealer, self)
    var sequences_sent = 0
    var sequences_received = 0
    var no_primer = 0
    //TODO keep track of failed sequences and re-assign them for processing 
    loop {
      receive {
        case msg: String => {
          println("Received: " + msg)
          if (fastq_iterator.end_of_file == false) {
            //read in a chunk of data.
            val inputfastq = collection.mutable.MutableList[FastqSequence]()

            breakable {
              for (i <- 0 to chunksize by 1) {
                inputfastq += fastq_iterator.next
                sequences_sent += 1
                if (fastq_iterator.end_of_file == true)
                  break
              }
            }

            println(sequences_sent)
            reply(inputfastq.toArray)

          } else if (sequences_sent == sequences_received)
            shutdown(players, reducers)
        } // case String
        case resultlist: Array[Result] => {
          // Process this list of results.
          resultlist foreach {
            case (result) =>
              sequences_received += 1

              if (mid_map.contains(result.locus)) {
                reducers(mid_map(result.locus)) ! result
              } else {
                no_primer += 1
              }
          }
          // Send out the next chunk of sequence.
          if (fastq_iterator.end_of_file == false) {

            //read in a chunk of data. 
            val inputfastq = collection.mutable.MutableList[FastqSequence]()

            breakable {
              for (i <- 0 to chunksize by 1) {
                inputfastq += fastq_iterator.next
                sequences_sent += 1
                if (fastq_iterator.end_of_file == true)
                  break
              }
            }

            //if (sequences_sent %10000 == 0)
            println(sequences_sent)
            reply(inputfastq.toArray)

          } else if (sequences_sent == sequences_received) {
            println("No primer: " + no_primer)
            shutdown(players, reducers)

          }

        } // case Result
      } // receive
    } // loop
  } // act

  // ***************************************************************************
} // class SnpDealer
