import os; 
version=1.0
#Parameters for mixture analysis 
global maf_thresh_mixture
maf_thresh_individual_low=0.1
maf_thresh_individual_low_id=-1 
maf_thresh_individual_amb=0.3 
maf_thresh_individual_amb_id=-1 
maf_thresh_individual_high=0.9 
maf_thresh_individual_high_id=-1 
maf_thresh_individual_amb_upper=0.7
maf_thresh_individual_amb_upper_id=-1 

min_calls=50; 
min_calls_id=-1 
ambiguous_thresh=90; 
ambiguous_thresh_id=-1 
strand_bias_thresh=90; 
strand_bias_thresh_id=-1;

#output directories for replicates
#create output directories for each data type, if they don't exist yet 
output_details_excel='output/replicate_details_excel/'
output_details_plot='output/replicate_details_image/'
output_histogram='output/replicate_hist/' 
if not os.path.exists('output'):
    os.mkdir('output') 
if not os.path.exists(output_details_excel): 
    os.mkdir(output_details_excel) 
if not os.path.exists(output_details_plot): 
    os.mkdir(output_details_plot) 
if not os.path.exists(output_histogram): 
    os.mkdir(output_histogram) 
