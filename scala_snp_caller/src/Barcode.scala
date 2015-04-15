
// ****************************************************************************
class Barcode( val name: String, val barcode1: String, val barcode2: String ) extends Serializable {

  // **************************************************************************
  override def toString(): String = { name + "\t" + barcode1 + "\t" + barcode2 }

  // **************************************************************************
}  // class Barcode
