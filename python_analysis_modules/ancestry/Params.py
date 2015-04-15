import os; 
version=1.0 
mutation_rate=1.1e-8 #per base random mutation rate 
#set parameters for genetic algorithm 
toolowthreshold=50#We need to have at least 50 hits for a SNP to consider it 
toolowthreshold_id=-1
contributing_thresh=0.1
contributing_thresh_id=-1  
runxtimes = 2; # run the entire algorithm 10 times and average the results from across the individual runs. 
runxtimes_id=-1 
maxtoreport=4
maxtoreport_id=-1 
minsnpspresent=30
minsnpspresent_id=-1 

#genotype assignment thresholds 
maf_thresh_individual_low=0.1
maf_thresh_individual_low_id=-1 
maf_thresh_individual_amb=0.3 
maf_thresh_individual_amb_id=-1 
maf_thresh_individual_amb_upper=0.7
maf_thresh_individual_amb_upper_id=-1 
maf_thresh_individual_high=0.9 
maf_thresh_individual_high_id=-1 

strand_bias_thresh_id=-1 
strand_bias_thresh=90

ambiguous_thresh_id=-1 
ambiguous_thresh=90 


#fixed parameters 
miniter=5; #at least 6 iterations 
maxcontributors = 6 #allow up to 6 contributing populations 
percenttokeep=0.20 #keep top 10 percent of population assignments at each generation 
percenttodrop = 0.20 #this should generally match the percent to keep to ensure a constant population size. 
minimprovement = .05 #minimum improvement in fitness between most fit populations in generation n and n+1 
ancestry_assignments = dict(); #keep track of the ancestry assigned to each barcode.
toolow = 0.05
totalSnps=128 

#output directories for replicates
#create output directories for each data type, if they don't exist yet 
output_excel='output/ancestry/'
if not os.path.exists('output'):
    os.mkdir('output') 
if not os.path.exists(output_excel): 
    os.mkdir(output_excel) 
