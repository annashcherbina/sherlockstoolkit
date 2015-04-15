import scala.util.control.Breaks._
import scala.actors.Actor, Actor._
// import scala.actors.remote.RemoteActor.{Node, select}
import scala.actors.remote.RemoteActor, RemoteActor._
import scala.actors.remote._
//OLD import scala.collection.mutable.Map
import scala.collection.mutable.{ ArrayBuffer, Map }
import scala.collection.mutable.MutableList
import scala.math._

class SnpPlayer(id: Int, barcodes: Map[String, String], word_size: Int, host: String, snp_pos_map: Map[String, Array[String]]) extends Actor {
  //@Anna: This let's you run the code across multiple different hosts? 
  RemoteActor.classLoader = getClass().getClassLoader()

  val counts: Counts = new Counts()
  val barcodes_set = new WordsSets(barcodes, word_size)

  //create word sets for the flanking sequence 
  val flank_5_forward: Map[String, String] = collection.mutable.Map[String, String]()
  val flank_3_forward: Map[String, String] = collection.mutable.Map[String, String]()
  val flank_5_reverse: Map[String, String] = collection.mutable.Map[String, String]()
  val flank_3_reverse: Map[String, String] = collection.mutable.Map[String, String]()
  snp_pos_map foreach {
    case (rs, flanks) =>
      flank_5_forward(rs) = flanks(0)
      flank_3_forward(rs) = flanks(1)
      flank_5_reverse(rs) = flanks(2)
      flank_3_reverse(rs) = flanks(3)
  }

  val flank_5_forward_set = new WordsSets(flank_5_forward, word_size)
  val flank_3_forward_set = new WordsSets(flank_3_forward, word_size)
  val flank_5_reverse_set = new WordsSets(flank_5_reverse, word_size)
  val flank_3_reverse_set = new WordsSets(flank_3_reverse, word_size)
// ***************************************************************************
   def randomString(length: Int): String = {
    val chars = ('a' to 'z') ++ ('A' to 'Z') ++ ('0' to '9')
    randomStringFromCharList(length, chars)
  }
// ***************************************************************************
  def randomStringFromCharList(length: Int, chars: Seq[Char]): String = {
    val sb = new StringBuilder
    for (i <- 1 to length) {
      val randomNum = util.Random.nextInt(chars.length)
      sb.append(chars(randomNum))
    }
    sb.toString
  }


  // ***************************************************************************

  def analyze(seq_name: String, seq_f: String, qual: String, word_size: Int): Result = {

    val result = new Result(seq_name, seq_f)
    val sequence_f = new Sequence(seq_f, word_size)

    //assign a barcode to the sequence 
    val seq_start = if (seq_f.length > 16) seq_f.substring(0, 16) else seq_f
    val seq_front = new Sequence(seq_start, word_size)
    val barcode_f = find_matches(seq_front, barcodes, barcodes_set).values
    var barcode = "No_barcode"
    if (barcode_f.size > 0)
      barcode = barcode_f.head
    result.barcodes_f = barcode

    var found_match: Boolean = false
    //check for perfect matches 
    val perfectMatchs_forward_5: collection.mutable.Set[String] = collection.mutable.Set[String]()
    val perfectMatchs_forward_3: collection.mutable.Set[String] = collection.mutable.Set[String]()
    val perfectMatchs_reverse_5: collection.mutable.Set[String] = collection.mutable.Set[String]()
    val perfectMatchs_reverse_3: collection.mutable.Set[String] = collection.mutable.Set[String]()

    //check for a perfect flank match on the forward strand of the reference
    breakable {
      flank_5_forward foreach {
        case (locus, flank_5_f) =>
          val f_5_index = seq_f.indexOf(flank_5_f)
          val flank_3_f = flank_3_forward(locus)
          val f_3_index = seq_f.indexOf(flank_3_f)
          if (min(f_5_index, f_3_index) > -1) {
            result.allele_strand = '+'
            result.flank_with_snp = seq_f.substring(f_5_index, min(seq_f.length, f_5_index + 21))
            result.qualstring = qual.substring(f_5_index, min(qual.length, f_5_index + 21))
            result.flank_5 = flank_5_f
            result.flank_3 = flank_3_f
	    result.locus=locus
            found_match = true
            break
          } else if (f_5_index > -1) {
            perfectMatchs_forward_5 += (locus)
          } else if (f_3_index > -1) {
            perfectMatchs_forward_3 += (locus)
          }
      }
    }

    //check for a perfect flank match on the reverse strand of the reference 
    if (found_match == false) {
      breakable {
        flank_5_reverse foreach {
          case (locus, flank_5_r) =>
            val flank_3_r = flank_3_reverse(locus)
            val r_5_index = seq_f.indexOf(flank_5_r)
            val r_3_index = seq_f.indexOf(flank_3_r)
            if (min(r_5_index, r_3_index) > -1) {
              result.allele_strand = '-'
              result.flank_with_snp = seq_f.substring(r_5_index, min(seq_f.length, r_5_index + 21))
              result.qualstring = qual.substring(r_5_index, min(qual.length, r_5_index + 21))
              result.flank_5 = flank_5_r
              result.flank_3 = flank_3_r
	      result.locus=locus 
              found_match = true
              break
            } else if (r_5_index > -1) {
              perfectMatchs_reverse_5 += (locus)
            } else if (r_3_index > -1) {
              perfectMatchs_reverse_3 += (locus)
            }
        }
      }
    }

    //handle cases where one of the flanks (5 or 3 ) match perfectly, and the other one does not. 
    if (found_match == false) {
      var bestLocus = "No_locus"
      var minDist = 10000
      var strand: Char = '.'
      var flank: String = ""
      var bestFlank5: String = ""
      var bestFlank3: String = ""
      var qualstring: String = ""

      perfectMatchs_forward_5 foreach {
        case locus =>
          val f_5_index = seq_f.indexOf(flank_5_forward(locus))
          if (seq_f.length > f_5_index + 10) {
            val f_3_flank = seq_f.substring(f_5_index + 11, min(f_5_index + 21, seq_f.length))
            val dist = distance(f_3_flank, flank_3_forward(locus))
            if (dist < minDist) {
              bestLocus = locus
              minDist = dist
              strand = '+'
              flank = seq_f.substring(f_5_index, min(seq_f.length, f_5_index + 21))
              qualstring = qual.substring(f_5_index, min(seq_f.length, f_5_index + 21))
              bestFlank5 = flank_5_forward(locus)
              bestFlank3 = ""
            }
          }
      }

      perfectMatchs_forward_3 foreach {
        case locus =>
          val f_3_index = seq_f.indexOf(flank_3_forward(locus))
          if (f_3_index > 0) {
            val f_5_flank = seq_f.substring(max(0, f_3_index - 11), f_3_index - 1)
            val dist = distance(f_5_flank, flank_5_forward(locus))
            if (dist < minDist) {
              bestLocus = locus
              minDist = dist
              strand = '+'
              flank = seq_f.substring(max(0, f_3_index - 11), f_3_index + 10)
              qualstring = qual.substring(max(0, f_3_index - 11), f_3_index + 10)
              bestFlank5 = ""
              bestFlank3 = flank_3_forward(locus)
            }
          }
      }

      perfectMatchs_reverse_5 foreach {
        case locus =>
          val r_5_index = seq_f.indexOf(flank_5_reverse(locus))
          if (seq_f.length > r_5_index + 10) {
            val r_3_flank = seq_f.substring(r_5_index + 11, min(r_5_index + 21, seq_f.length))
            val dist = distance(r_3_flank, flank_3_reverse(locus))
            if (dist < minDist) {
              bestLocus = locus
              minDist = dist
              strand = '-'
              flank = seq_f.substring(r_5_index, min(seq_f.length, r_5_index + 21))
              qualstring = qual.substring(r_5_index, min(seq_f.length, r_5_index + 21))
              bestFlank3 = ""
              bestFlank5 = flank_5_reverse(locus)
            }
          }
      }

      perfectMatchs_reverse_3 foreach {
        case locus =>
          val r_3_index = seq_f.indexOf(flank_3_reverse(locus))
          if (r_3_index > 0) {
            val r_5_flank = seq_f.substring(max(0, r_3_index - 11), r_3_index - 1)
            val dist = distance(r_5_flank, flank_5_reverse(locus))
            if (dist < minDist) {
              bestLocus = locus
              minDist = dist
              strand = '-'
              flank = seq_f.substring(max(0, r_3_index - 11), r_3_index + 10)
              qualstring = qual.substring(max(0, r_3_index - 11), r_3_index + 10)
              bestFlank5 = ""
              bestFlank3 = flank_3_reverse(locus)
            }
          }
      }

      result.allele_strand = strand
      result.locus = bestLocus
      result.flank_with_snp = flank
      result.qualstring = qualstring
      result.flank_3 = bestFlank3
      result.flank_5 = bestFlank5
    }
    if (result.locus=="No_locus")
    {
    var r=new scala.util.Random(10) 
    
    }
    result
  } //analyze

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

  //***************************************************************************
  def combine(m1: collection.Map[Int, String], m2: collection.Map[Int, String]): collection.Map[Int, String] = {
    var k1 = Set(m1.keysIterator.toList: _*)
    var k2 = Set(m2.keysIterator.toList: _*)
    var intersection = k1 & k2
    var r1 = for (key <- intersection) yield (key -> (m1(key) + m2(key)))
    var r2 = m1.filterKeys(!intersection.contains(_)) ++ m2.filterKeys(!intersection.contains(_))
    r2 ++ r1
  } //combine

  def minimum(i1: Int, i2: Int, i3: Int) = min(min(i1, i2), i3)

  def distance(s1: String, s2: String) = {
    val dist = Array.tabulate(s2.length + 1, s1.length + 1) { (j, i) => if (j == 0) i else if (i == 0) j else 0 }

    for (j <- 1 to s2.length; i <- 1 to s1.length)
      dist(j)(i) = if (s2(j - 1) == s1(i - 1)) dist(j - 1)(i - 1)
      else minimum(dist(j - 1)(i) + 1, dist(j)(i - 1) + 1, dist(j - 1)(i - 1) + 1)

    val finaldist=dist(s2.length)(s1.length)
    finaldist
  }

  // ***************************************************************************

  def find_matches(sequence: Sequence, target_map: Map[String, String], target_words: WordsSets): collection.mutable.Map[Int, String] = {
    val found = collection.mutable.Map[Int, String]() //map target to position where it ends.
    target_map foreach {
      case (name, target_seq) =>
        if (sequence.seq_forward contains target_seq) {
          val index_start = sequence.seq_forward.indexOfSlice(target_seq)
          val index_end = index_start + target_seq.length
          found += (index_end -> name)
        } else if (sequence.seq_reverse contains target_seq) {
          val index_start = sequence.seq_reverse.indexOfSlice(target_seq)
          val index_end = index_start + target_seq.length
          found += (index_end -> name)
        }
    } // foreach

    // Check for no perfect matches.
    if (found.size == 0) {
      // Search with mismatches allowed.
      val search = target_words.find(sequence)
      if (search._2 > 0) found += (search._3 + 1 -> search._1)
    } // if

    found
  } // find_matches

  def act() {
    // scala.actors.Debug.level = 3
    //println( "SnpPlayer started: " + id )
    Thread.sleep(3000)
    val dealer_node = select(scala.actors.remote.Node(host, 19000), 'SnpDealer)
    println(dealer_node.toString())
    dealer_node ! "I'm alive!"
    println("SnpPlayer -> dealer")
    loop {
      react {
        case msg: String => println("SnpPlayer: " + msg)
        case fastqinput: Array[FastqSequence] => {
          val analyzedfastq = collection.mutable.MutableList[Result]()
          //println("SnpPlayer begining to process new chunk of data") 
          fastqinput foreach {
            case fastq =>
              val seq_f = fastq.sequence.toUpperCase()
              analyzedfastq += analyze(fastq.name, seq_f, fastq.quality, word_size)
          }
          dealer_node ! analyzedfastq.toArray
        }
        case fastainput: Array[FastaSequence] => {
          val analyzedfasta = collection.mutable.MutableList[Result]()
          fastainput foreach {
            case fasta =>
              val seq_f = fasta.sequence.toUpperCase()
              analyzedfasta += analyze(fasta.name, seq_f, "", word_size)
          }
          dealer_node ! analyzedfasta.toArray
        }
        case done: Double => { println("Done!"); exit() }
        case _            => { println("Ooops!"); dealer_node ! "error" }
      } // receive
    } //loop
  } // act
} // class SnpPlayer
