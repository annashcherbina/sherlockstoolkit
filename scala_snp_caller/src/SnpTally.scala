import scala.math
import scala.collection.mutable.Map
import scala.collection.mutable.Set
import scala.util.control.Breaks._

// ****************************************************************************
class SnpTally(val locus: String, reports: Reports, locus_alleles: String, locus_ma: String, low_thresh: Int, ambiguous_0: Double, ambiguous_1: Double, ambiguous_2: Double, ambiguous_3: Double) {

  //barcode-->strand-->flanks-->counts
  var snps_seen = scala.collection.mutable.Map[String, Map[Char, Map[String, Int]]]()
  var qual_seen = scala.collection.mutable.Map[String, Map[Char, Map[String, Double]]]()
  val alleles_seen = Map[String, Map[String, Map[Char, Int]]]()
  val alleles_qual = Map[String, Map[String, Map[Char, Double]]]() // stores average quality score observed for each allele 

  //barcode--> value 
  var maf = Map[String, Double]()
  var total_counts = Map[String, Int]()
  var forward_counts = Map[String, Int]()
  var low_counts = Map[String, Int]()
  var ambiguous = Map[String, Int]()
  var strand_sep = Map[String, Int]()

  def seq_split(seq: String): scala.collection.mutable.Map[String, Int] = {
    var new_set = scala.collection.mutable.Map[String, Int]()
    for (i <- 0 until seq.length) {
      val seq1 = seq.substring(0, i)
      val seq2 = seq.substring(i + 1)
      new_set += ((seq1 + seq2) -> i)
    }
    new_set
  }

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

  def call_individual_allele(flank5: String, flank3: String, flank: String,strand: Char): Array[String] = {
    var call = Array("", "")
    var allele = ""
    //in most cases the 2 flanks should match exactly 
    val match5 = flank.indexOf(flank5)
    val match3 = flank.indexOf(flank3)

    if ((match3 > -1) && (match5 > -1) && (match3 >= (match5 + flank5.length))) {
      ////println("both flanks match")
      allele = flank.substring(match5 + flank5.length, match3)
      call(0) = allele
      if (flank.length < 12)
        call(1) = flank.substring(9)
      else
        call(1) = flank.substring(9, 12)
    } else if (match5 > -1) {

      if (flank3.contains('N') || flank3.length == 1) {
        allele = flank(match5 + flank5.length).toString
      } else if (flank.length == flank5.length) {
        allele == ""
      } else {
        val subflank = flank.substring(match5 + flank5.length + 1)
        val words = seq_split(flank3)
        val subflankwords = seq_split(subflank)
        var commonwords = words.keys.toSet & subflankwords.keys.toSet
        if (commonwords.size > 0) {
          val posOmitted = words(commonwords.head)
          if (posOmitted > 0)
            allele = flank(match5 + flank5.length).toString
          else
            allele = subflank.substring(0, 2)
        }
      }
      call(0) = allele
      if (flank.length < 12)
        call(1) = flank.substring(9)
      else
        call(1) = flank.substring(9, 12)

    } else if (match3 > 0) {
      if (flank5.contains('N')) {
        allele = flank(match3 - 1).toString
      } else {
        val subflank = flank.substring(0, match3 - 1)
        val words = seq_split(flank5)
        val subflankwords = seq_split(subflank)
        var commonwords = words.keys.toSet & subflankwords.keys.toSet
        if (commonwords.size > 0) {
          val posOmitted = words(commonwords.head)
          if (posOmitted < (subflank.length - 1)) {
            allele = flank(match3 - 1).toString
          } else {
            allele = flank.substring(match3 - 1, match3 + 1)
          }
        }
      }
      call(0) = allele
      if (flank.length < 12)
        call(1) = flank.substring(9)
      else
        call(1) = flank.substring(9, 12)
    }
    else
    {
    println("bad flanks:"+flank5+","+flank3+","+flank) 
    }
    if (strand=='-')
    {
    if (call(0)!="")
       call(0)=compliment(call(0).charAt(0)).toString
       }
    call
  }

  // **************************************************************************
  def call_alleles(flanks_ref: Array[String]) {

    snps_seen foreach {
      case (barcode, strands) =>
        strands foreach {
          case (strand, flanks) =>
            //9-12 base region in flank --> called snp
            val snp_region = Map[String, String]()
            var flank5: String = ""
            var flank3: String = ""
            if (strand == '+') {
              flank5 = flanks_ref(0)
              flank3 = flanks_ref(1)
            } else {
              flank5 = flanks_ref(2)
              flank3 = flanks_ref(3)
            }
            //get the flank with the maximum counts, since this is most likely the allele flank. 
            val highestflank = flanks.maxBy(_._2)._1
            var count = flanks(highestflank)
            var qual_total = qual_seen(barcode)(strand)(highestflank)
            var allele = ""

            if (highestflank.length == 0) {
              reports.flank_report ! barcode + "\t" + locus + "\t" + strand + "\t" + highestflank + "\t" + count + "\t" + allele
            } else {
              val alleleInfo = call_individual_allele(flank5, flank3, highestflank,strand)
              allele = alleleInfo(0)
              val center_flank = alleleInfo(1)

              snp_region += (center_flank -> allele)
              reports.flank_report ! barcode + "\t" + locus + "\t" + strand + "\t" + highestflank + "\t" + count + "\t" + allele
            }

            //record the new allele and the associated mean quality score 

            if (alleles_seen.contains(barcode) == false) {
              alleles_seen += barcode -> Map[String, Map[Char, Int]]()
              alleles_qual += barcode -> Map[String, Map[Char, Double]]()
            }
            if (alleles_seen(barcode).contains(allele) == false) {
              alleles_seen(barcode) += allele -> Map[Char, Int]()
              alleles_qual(barcode) += allele -> Map[Char, Double]()
            }
            if (alleles_seen(barcode)(allele).contains(strand) == false) {
              alleles_seen(barcode)(allele) += strand -> count
              alleles_qual(barcode)(allele) += strand -> qual_total
            } else {
              alleles_seen(barcode)(allele)(strand) += count
              alleles_qual(barcode)(allele)(strand) += qual_total
            }

            flanks.remove(highestflank)

            flanks foreach {
              case (flank, count) =>
                allele = ""
		qual_total= qual_seen(barcode)(strand)(flank)
                //if flank is empty, no snp called 
                if (flank.length == 0) {
                  reports.flank_report ! barcode + "\t" + locus + "\t" + strand + "\t" + flank + "\t" + count + "\t" + allele
                } else {
                  var center_flank = ""
                  if (flank.length < 12)
                    center_flank = flank.substring(9)
                  else
                    center_flank = flank.substring(9, 12)

                  val alleleInfo = call_individual_allele(flank5, flank3, flank,strand)
                  allele = alleleInfo(0)

                  if (allele == "") {
                    if (snp_region.contains(center_flank))
                      allele = snp_region(center_flank)
                  } else {
                    snp_region += (center_flank -> allele)
                  }

                  reports.flank_report ! barcode + "\t" + locus + "\t" + strand + "\t" + flank + "\t" + count + "\t" + allele
                }
                //record the new allele

                if (alleles_seen.contains(barcode) == false) {
                  alleles_seen += barcode -> Map[String, Map[Char, Int]]()
                  alleles_qual += barcode -> Map[String, Map[Char, Double]]()
                }
                if (alleles_seen(barcode).contains(allele) == false) {
                  alleles_seen(barcode) += allele -> Map[Char, Int]()
                  alleles_qual(barcode) += allele -> Map[Char, Double]()
                }
                if (alleles_seen(barcode)(allele).contains(strand) == false) {
                  alleles_seen(barcode)(allele) += strand -> count
                  alleles_qual(barcode)(allele) += strand -> qual_total
                } else {
                  alleles_seen(barcode)(allele)(strand) += count
                  alleles_qual(barcode)(allele)(strand) += qual_total
                }
            }
        }
    }
  } //call_alleles

  // **************************************************************************
  def get_quality(qualstring: String): Double = {
    if (qualstring == "") {
      return 0
    }
    var totalqual: Double = 0
    var numqual: Double = 0
    qualstring foreach {
      case (qual_char) =>
        totalqual += qual_char.toInt - 33
        numqual += 1
    }
    val quotient: Double = totalqual / numqual
    //println("totalqual:"+totalqual.toString) 
    //println("numqual:"+numqual.toString) 
    //println("quotient:"+quotient.toString) 
    return quotient
  }

  // **************************************************************************

  // **************************************************************************
  def add_result(result: Result, qualcutoff: Int) {
    //get the quality score at positions 10,11,12 
    val qualscore = get_quality(result.qualstring)
    var snpQualityHigh = true
    if (qualscore < qualcutoff) {
      snpQualityHigh = false
    }
    //only add the flanking bases if the quality at positions 10,11,12 is greater than the cutoff 
    if (snpQualityHigh == true) {
      // Check if seen Allele barcode yet.
      if (snps_seen.contains(result.barcodes_f) == false) {
        snps_seen += result.barcodes_f -> Map[Char, Map[String, Int]]()
        qual_seen += result.barcodes_f -> Map[Char, Map[String, Double]]()
      }
      // Check if seen allele strand yet.
      if (snps_seen(result.barcodes_f).contains(result.allele_strand) == false) {
        snps_seen(result.barcodes_f) += result.allele_strand -> Map[String, Int]()
        qual_seen(result.barcodes_f) += result.allele_strand -> Map[String, Double]()
      }
      // Check if seen allele flank yet.

      if (snps_seen(result.barcodes_f)(result.allele_strand).contains(result.flank_with_snp) == false) {
        snps_seen(result.barcodes_f)(result.allele_strand) += result.flank_with_snp -> 1
        qual_seen(result.barcodes_f)(result.allele_strand) += result.flank_with_snp -> qualscore
      } else {
        snps_seen(result.barcodes_f)(result.allele_strand)(result.flank_with_snp) += 1
        qual_seen(result.barcodes_f)(result.allele_strand)(result.flank_with_snp) += qualscore
      }
    }
  } // add_result

  // *************************************************************************
  def get_performance() {
  val goodalleles=List("a","t","c","g","A","T","C","G")
    alleles_seen foreach {
      case (barcode, alleles) =>
        var macount: Int = 0
        var totalcount: Int = 0
        var forwardcount: Int = 0
        alleles foreach {
          case (name, counts) =>
	  if (goodalleles.contains(name)){
            counts foreach {
              case (strand, count) =>
	      //println("name:"+name+",ma:"+locus_ma)
                if (name == locus_ma)
                  macount += count
                totalcount += count
                if (strand == '+')
                  forwardcount += count
            }
	   }
        }
        //store the maf value 
	var mafval=0.00
	if (totalcount>0)		 
	   mafval = (macount*1.0) / totalcount
        maf += barcode -> mafval
        total_counts += barcode -> totalcount
        forward_counts += barcode -> forwardcount

        //determine if a failure case is present : not enough reads, strand separation, ambiguous maf 
        if (totalcount < 2 * low_thresh)
          low_counts += barcode -> 1
        else
          low_counts += barcode -> 0

        if ((forwardcount < low_thresh) || ((totalcount - forwardcount) < low_thresh))
          strand_sep += barcode -> 1
        else
          strand_sep += barcode -> 0

        ambiguous += barcode -> 0
        //check if the maf is in the ambiguous range 
        if ((ambiguous_0 != null) && (ambiguous_1 != null)) {
          if ((mafval > ambiguous_0) && (mafval < ambiguous_1)) {
            ambiguous(barcode) = 1
          }
        } else if ((ambiguous_2 != null) && (ambiguous_3 != null)) {
          if ((mafval > ambiguous_2) && (mafval < ambiguous_3)) {
            ambiguous(barcode) = 1
          }
        }
    }
  }
  // *************************************************************************

  // **************************************************************************
  def write_snps_report() {
    alleles_seen foreach {
      case (barcode, alleles) =>
        var line_out: String = barcode + "\t" + locus + "\t" + locus_alleles + "\t" + locus_ma

        var a_count: Int = 0
        var a_forward_qual: Double = 0
        var a_rev_qual: Double = 0

        var t_count: Int = 0
        var t_forward_qual: Double = 0
        var t_rev_qual: Double = 0

        var c_count: Int = 0
        var c_forward_qual: Double = 0
        var c_rev_qual: Double = 0

        var g_count: Int = 0
        var g_forward_qual: Double = 0
        var g_rev_qual: Double = 0

        var allele_count: Int = 0
        var forward_qual = -1: Double
        var reverse_qual = -1: Double

        alleles foreach {
          case (name, counts) =>
            allele_count = 0
            forward_qual = 0
            reverse_qual = 0
            counts foreach {
              case (strand, count) =>
                allele_count += count
                if (strand == '+')
                  forward_qual = alleles_qual(barcode)(name)(strand) / alleles_seen(barcode)(name)(strand)
                else if (strand == '-')
                  reverse_qual = alleles_qual(barcode)(name)(strand) / alleles_seen(barcode)(name)(strand)
            }
            if (name == "A" || name == "a") {
              a_count += allele_count
              a_forward_qual += forward_qual
              a_rev_qual += reverse_qual
            } else if (name == "T" || name == "t") {
              t_count += allele_count
              t_forward_qual += forward_qual
              t_rev_qual += reverse_qual
            }else if (name == "C" || name == "c") {
              c_count += allele_count
              c_forward_qual += forward_qual
              c_rev_qual += reverse_qual
            } else if (name == "G" || name == "g") {
              g_count += allele_count
              g_forward_qual += forward_qual
              g_rev_qual += reverse_qual
            }
	    else{
	    println("UNRECOGNIZED ALLELE:"+name.toString) 
	    }

        }
	a_forward_qual=math.round(a_forward_qual) 
	a_rev_qual=math.round(a_rev_qual)
	c_forward_qual=math.round(c_forward_qual) 
	c_rev_qual=math.round(c_rev_qual)
	t_forward_qual=math.round(t_forward_qual) 
	t_rev_qual=math.round(t_rev_qual)
	g_forward_qual=math.round(g_forward_qual) 
	g_rev_qual=math.round(g_rev_qual) 
	
        line_out = line_out + "\t" + "A" + "\t" + a_count.toString + "\t" + a_forward_qual.toString + "\t" + a_rev_qual.toString + "\t" + "C" + "\t" + c_count.toString + "\t" + c_forward_qual.toString + "\t" + c_rev_qual.toString + "\t" + "T" + "\t" + t_count.toString + "\t" + t_forward_qual.toString + "\t" + t_rev_qual.toString + "\t" + "G" + "\t" + g_count.toString + "\t" + g_forward_qual.toString + "\t" + g_rev_qual.toString + "\t" + total_counts(barcode).toString + "\t" + forward_counts(barcode).toString + "\t" + maf(barcode).toString + "\t" + low_counts(barcode).toString + "\t" + ambiguous(barcode).toString + "\t" + strand_sep(barcode).toString
        reports.snps_report ! line_out
    }
  } // write_snps_report

  // **************************************************************************
} // class SnpTally
