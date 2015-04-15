import scala.actors.Actor, Actor._
import scala.actors.remote.RemoteActor, RemoteActor._
import scala.actors.remote._
import scala.collection.mutable.{ Map, ArrayBuffer }

class SnpReducer(id: Int, loci: collection.mutable.MutableList[String], barcode: Array[String], ref_seqs: ArrayBuffer[FastaSequence], host: String, reports: Reports, snp_pos_map: Map[String, Array[String]], qualcutoff: Int, low_thresh: Int, ambiguous_0: Double, ambiguous_1: Double, ambiguous_2: Double, ambiguous_3: Double) extends Actor {
  RemoteActor.classLoader = getClass().getClassLoader()

  // ***************************************************************************
  def write_reports(locus_count: Map[String, Int], locus: String) {
    locus_count foreach { case (name, cnt) => reports.stats_report ! name + "\t" + locus + "\t" + cnt }
  } // write_reports

  // ***************************************************************************
  def act() {
    // scala.actors.Debug.level = 3
    //println( "SnpReducer started: " + id )
    val dealer_node = select(scala.actors.remote.Node(host, 19000), 'SnpDealer)
    val locus_count: Map[String, Map[String, Int]] = collection.mutable.Map[String, collection.mutable.Map[String, Int]]()
    var locus_to_tally: Map[String, SnpTally] = collection.mutable.Map[String, SnpTally]()
    var counts: Map[String, Int] = collection.mutable.Map[String, Int]()

    loci foreach {
      case (locus) =>
        val snp_tally = new SnpTally(locus, reports, snp_pos_map(locus)(4), snp_pos_map(locus)(5), low_thresh, ambiguous_0, ambiguous_1, ambiguous_2, ambiguous_3)
        counts += (locus -> 0)
        locus_to_tally += (locus -> snp_tally)
        locus_count += (locus -> collection.mutable.Map[String, Int]())
    }
    //val snp_tally = new SnpTally( locus, reports)
    loop {
      react {
        case msg: String => println("SnpReducer: " + msg)
        case result: Result => {

          //can't write details because haven't called the locus
          //reports.details_report ! result.to_string

          //call the appropriate SNPTally object base on the locus 
          val curLocus = result.locus
          counts(curLocus) += 1
          locus_to_tally(curLocus).add_result(result, qualcutoff)

          if (locus_count(curLocus).contains(result.barcodes_f))
            locus_count(curLocus)(result.barcodes_f) += 1
          else
            locus_count(curLocus) += (result.barcodes_f -> 1)
        } // case Result
        //aggregate information for all observed flanking sequences to call alleles and write reports 
        case done: Double => {
          locus_to_tally.keySet foreach {
            case (locus) =>
              if (counts(locus) > 1) {
                write_reports(locus_count(locus), locus)
                locus_to_tally(locus).call_alleles(snp_pos_map(locus))
                locus_to_tally(locus).get_performance()
                locus_to_tally(locus).write_snps_report() //this is the main report that will go into the forensic database system 
                println("SnpReducer Done! locus: " + locus + ", count: " + counts(locus));
              } //if
          } //foreach

          reports.close
          exit()
        }
        case _ => { println("Ooops!"); dealer_node ! "error" }
      } // receive
    } // loop
  } // act
} // class SnpReducer
