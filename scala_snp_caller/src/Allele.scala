import scala.util.matching.Regex

// ****************************************************************************
class Allele( val locus: String, val allele_name: String, val pattern: String, val re: Regex, val order: Int ) extends Serializable {

  // **************************************************************************
  def snap = { "Allele|" + locus + "|" + allele_name + "|" + pattern + "|" }

  // **************************************************************************
  def to_string = { locus + "\t" + allele_name + "\t" + pattern }

  // **************************************************************************
}  // class Allele
