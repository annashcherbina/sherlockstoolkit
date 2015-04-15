// ****************************************************************************
class Result( val seq_name: String, var seq: String ) extends Serializable { 
    var barcodes_f: String = "No_barcode"
    var locus: String = "No_locus"
    var allele_name: String = ""
    var allele_strand: Char = '.'
    var ref_strand: String=""
    var flank_5: String = ""
    var flank_3: String = ""
    var flank_with_snp="" 
    var qualstring:String=""
    
  // **************************************************************************
  def to_string = { seq_name+"\t" +barcodes_f + "\t" + locus + "\t"  + allele_strand + "\t" + flank_5 +"\t"  + flank_3 +"\t"+flank_with_snp}

  // **************************************************************************
}  // class Result
