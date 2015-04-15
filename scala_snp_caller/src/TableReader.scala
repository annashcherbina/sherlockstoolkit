
import scala.collection.mutable.Map

// ****************************************************************************
class TableReader( val table_name: String ) {

  val hash_1 = collection.mutable.Map[String, String]() 
  val hash_2 = collection.mutable.Map[String, String]() 

  // println( "TableReader called" )
  private[this] val table_file = new InputFile( table_name )
  private[this] val lines = table_file.read_contents().split( "\n" )

  for ( i <- 0 until lines.length ) {
    val tokens = lines( i ).split( "\t" )
    hash_1 += (tokens(0) -> tokens(1).toUpperCase())
    if ( tokens.length > 2 )
      hash_2 += (tokens(0) -> tokens(2).toUpperCase())
  }  // for

  // **************************************************************************

}  // class TableReader
