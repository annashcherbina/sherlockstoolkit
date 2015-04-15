import os; 
version=1.0
#Parameters for mixture analysis 
global maf_thresh_mixture
min_calls=50; 
min_calls_id=-1

#output directories for replicates
#create output directories for each data type, if they don't exist yet 
if not os.path.exists('output'):
    os.mkdir('output') 
