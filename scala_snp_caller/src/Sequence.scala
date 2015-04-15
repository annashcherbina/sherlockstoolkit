
import scala.collection.mutable.Set

// ****************************************************************************
class Sequence(val seq_forward: String, val word_size: Int) {
  val seq_tools = new SeqTools()

  val seq_reverse = seq_tools.reverse_compliment( seq_forward )
  val forward_words: collection.mutable.Set[String] = seq_tools.seq_split( seq_forward, word_size )
  val reverse_words: collection.mutable.Set[String] = seq_tools.seq_split( seq_reverse, word_size )

  // **************************************************************************
}  // class Sequence
