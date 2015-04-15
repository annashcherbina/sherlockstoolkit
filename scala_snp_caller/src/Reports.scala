

// ****************************************************************************
class Reports( file_name:String, cores: Int ) {

  val filename = file_name.replaceAll( "(.fasta)|(.fastq)|(.fa)|(.fq)", "" )
  
  //val alleles_report = new Report( filename + "_alleles.csv", cores )
  //alleles_report.start()

  //val counts_report = new Report( filename + "_counts.csv", cores )
  //counts_report.start()

  //val details_report = new Report( filename + "_details.csv", cores )
  //details_report.start()

  val stats_report = new Report( filename + "_stats.csv", cores,"stats" )
  stats_report.start()

  val snps_report = new Report( filename + "_snps.csv", cores,"snps" )
  snps_report.start()

  //val summary_report = new Report( filename + "_summary.csv", cores )
  //summary_report.start()

  val flank_report=new Report(filename+"_flank.csv",cores,"flank") 
  flank_report.start() 


  // **************************************************************************
  def close = {
    //alleles_report ! 0.0
    //counts_report ! 0.0
    //details_report ! 0.0
    stats_report ! 0.0
    snps_report ! 0.0
    //summary_report ! 0.0
    flank_report ! 0.0 
  }  // close

  // **************************************************************************

}  // class Reports

