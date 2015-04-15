
import scala.actors.Actor
import scala.actors.Actor._

// ****************************************************************************
class Report( file_name:String, cores: Int,reportType:String ) extends Actor {

  private[this] val out_file: OutputFile = new OutputFile( file_name )

  // **************************************************************************
  def act() {
    var closed: Int = 0
   reportType match {
  case "flank"  => out_file.write("Barcode\tLocus\tStrand\tFlank\tCount\tAllele\n")
  case "stats"  => out_file.write("Barcode\tLocus\tCount\n") 
  case "snps" => out_file.write("Barcode\tSNP(IfFound)\tAlleles\tMinorAllele\tBase1\tCounts1\tForQuality1\tRevQuality1\tBase2\tCounts2\tForQuality2\tRevQuality2\tBase3\tCounts3\tForQuality3\tRevQuality3\tBase4\tCounts4\tForQuality4\tRevQuality4\tTotalCounts\tForwardCounts\tMAF\tLow\tAmbiguous\tStrandSep\n")
  // catch the default with a variable so you can print it
  case whoa  => println("Unexpected report type: " + whoa.toString)
}
    loop {
      react {
        case msg: String => { out_file.write( msg + "\n" ); }
        case done: Double => {
          closed += 1
          if ( closed >= cores )
            exit()
        }  // case done
      }  // react
    }  // loop
  }  // method act

  // **************************************************************************

}  // class Report

