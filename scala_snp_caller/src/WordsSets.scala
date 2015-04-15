import scala.collection.mutable.{Map, Set}

// ****************************************************************************
class WordsSets( targets: Map[String, String], word_size: Int) {

  private[this] val seq_tools = new SeqTools()

  val targets_seqs = Map[String, String]()
  val targets_words = Map[String, Set[String]]()
   targets foreach {case (name, seq) =>
     targets_seqs  += (name -> seq)
     targets_words += (name -> seq_tools.seq_split( seq, word_size ) ) 
   }  // foreach

  // **************************************************************************


def find( sequence: Sequence ): Tuple3[String, Int,Int] = {
    var best_forward = lookup( sequence.seq_forward, sequence.forward_words )
    var best_reverse = lookup( sequence.seq_reverse, sequence.reverse_words )
    if ( best_forward._2 > best_reverse._2 ) return best_forward
    else return best_reverse
  }  // find


  // **************************************************************************
  def lookup( query_seq: String, seq_set: Set[String] ): Tuple3[String, Int,Int] = {
    var best_count = 0
    var best_name = ""
    var max_base=0
    var best_set = Set[String]()
    targets_words foreach {case (name, micro_set) =>
      val common_set = seq_set & micro_set
      val count = common_set.size
      if ( count > best_count ) { best_count = count; best_name = name; best_set = common_set }
   }// foreach

   // Validate the best match
   //println(best_name)
   if ( best_name.length > 0 ) {
     val micro = targets_seqs( best_name )
     var align = micro.toArray
     best_set foreach {case (word) =>
       val index = micro.indexOf( word )
       for (i <- 0 until word_size) {align(index+i) = '|'}
     }  // foreach

     var count = 0
     align foreach { case (base) => if (base == '|') 
     {count += 1
     if(base > max_base)
     {
     max_base=base
     }	
     }
     if ( count < micro.length - 2 ) {
       best_name = ""
       best_count = 0
     }  // if
   } // if
  } // lookup
  return (best_name, best_count,max_base)
}
  // **************************************************************************
}  // class WordsSets
