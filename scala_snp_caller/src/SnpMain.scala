//  This is the main class for SnpDealer class.
// ******************************************************************************
object SnpMain {

  //****************************************************************************
  // This method tests the Snp class.
  def main(args: Array[String]) {
    //val dealer: SnpDealer = new SnpDealer( "data/H72JP8R01AmpTrim.fasta", "data/STR_barcodes.tsv", "data/STR_primers.tsv", "data/str_alleles.csv", "data/str_refs.fa", 4 )
    // val dealer: SnpDealer = new SnpDealer( "data/str_test.fa", "data/STR_barcodes.tsv", "data/STR_primers.tsv", "data/str_alleles.csv", "data/str_refs.fa", 4 )
    // val dealer: SnpDealer = new SnpDealer( "data/th01_test.fa", "data/STR_barcodes.tsv", "data/STR_primers.tsv", "data/str_alleles.csv", "data/str_refs.fa", 1 )
    val dealer: SnpDealer = new SnpDealer("../DOR84.fastq", "../inputs/FluidigmBarsDOR84.tsv","../inputs/IAD1312_seqs.fasta",30,30,0,50,0.15,0.30,0.7,0.85) 
    //val dealer: SnpDealer = new SnpDealer("../YWRFO.fastq", "../inputs/IonXpressBarsYWRFO.tsv", "../inputs/IAD28825_seqs.fasta",30,30,20) 
    //val dealer: SnpDealer = new SnpDealer("../X5QP7.fastq", "../inputs/IonXpressBarsX5QP7.tsv", "../inputs/IAD30341_primers.txt", "../inputs/IAD30341_seqs.fasta",64,128) 
    //val dealer: SnpDealer = new SnpDealer("../RAY9L.fastq", "../inputs/FluidigmBarsRAY9L.tsv", "../inputs/IAD1438_primers.txt", "../inputs/IAD1438_seqs.fasta",64,128)
    //val dealer: SnpDealer = new SnpDealer("../mixAP_small.fastq", "../inputs/IonXpressBarsFull.tsv", "../inputs/IAD39359_primers.txt", "../inputs/IAD39359_seqs.fasta",32,32,20)
    // (305 seconds) val dealer: SnpDealer = new SnpDealer("../IA89K.fastq", "../inputs/FluidigmBarsIA89K.tsv", "../inputs/IAD1438_primers.txt", "../inputs/IAD1438_seqs.fasta",128) 
    //val dealer: SnpDealer = new SnpDealer("../Z5TDC.fastq", "../inputs/IonXpressBarsZ5TDC.tsv", "../inputs/IAD39359_primers.txt", "../inputs/IAD39359_seqs.fasta",32) 
    //val dealer: SnpDealer = new SnpDealer("../MID-22_rs12555932.fasta", "../inputs/FluidigmBarsDOR84.tsv", "../inputs/IAD1312_primers.txt", "../inputs/IAD1312_seqs.fasta",128) 
    //val dealer: SnpDealer = new SnpDealer("../dk5.fastq", "../inputs/IonXpressBarsSub.tsv", "../inputs/panel_1568_primers.txt", "../inputs/panel_1568.fasta",70) 
    dealer.start()
  }  // main

}  // object SnpMain
