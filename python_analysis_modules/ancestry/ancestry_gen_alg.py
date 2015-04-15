#genetic algorithm to compute biogeographic ancestry. 
#applicable for computing mixed ancestries with multiple contributing populations. 

from Population import *
import Params; 
from genetic_helpers import* 
from Outputs import * 
import sys; 
import os; 
from math import log; 
from math import exp; 
import re; 
import operator; 
import MySQLdb as mdb; 


def recordAttachmentParameterMappings(cur,attachment_id): 
    attachments=[attachment_id] 
    parameter_ids=[Params.maf_thresh_individual_amb_id,Params.maf_thresh_individual_low_id,Params.toolowthreshold_id,Params.contributing_thresh_id,Params.runxtimes_id,Params.maxtoreport_id,Params.minsnpspresent_id,Params.maf_thresh_individual_amb_upper_id,Params.maf_thresh_individual_high_id,Params.strand_bias_thresh_id,Params.ambiguous_thresh] 
    for attachment_id in attachments: 
        for param_id in parameter_ids: 
            query="insert into attachments_parameters (attachment_id,parameter_id) VALUES("+str(attachment_id)+","+str(param_id)+");"
            cur.execute(query) 

def getParameters(cur,user_id,parameter_group):
    #get maf individual threshold 
    query="Select id,value from parameters where  group_name='"+str(parameter_group)+"' and name like '%Reference - MAF for 0 Minor Alleles (upper bound%' order by id DESC limit 1;" 
    cur.execute(query)
    values=cur.fetchone()
    if values==None: 
        #use the default 
        query="select id,value from parameters where user_id=1 and name like '%Reference - MAF for 0 Minor Alleles (upper bound%';"
        cur.execute(query) 
        values=cur.fetchone() 
    Params.maf_thresh_individual_low_id=values[0] 
    Params.maf_thresh_individual_low=values[1]/100.0 

    #get maf individual ambiguous 
    query="Select id,value from parameters where  group_name='"+str(parameter_group)+"'  and name like '%Reference - MAF for 1 Minor Allele (lower bound%' order by id DESC limit 1;" 
    cur.execute(query)
    values=cur.fetchone()
    if values==None: 
        #use the default 
        query="select id,value from parameters where user_id=1 and name like '%Reference - MAF for 1 Minor Allele (lower bound%';"
        cur.execute(query) 
        values=cur.fetchone() 
    Params.maf_thresh_individual_amb_id=values[0] 
    Params.maf_thresh_individual_amb=values[1]/100.0

    #get maf individual ambiguous (upper) 
    query="Select id,value from parameters where  group_name='"+str(parameter_group)+"'  and name like '%Reference - MAF for 1 Minor Allele (upper bound%' order by id DESC limit 1;" 
    cur.execute(query)
    values=cur.fetchone()
    if values==None: 
        #use the default 
        query="select id,value from parameters where user_id=1 and name like '%Reference - MAF for 1 Minor Allele (upper bound%';"
        cur.execute(query) 
        values=cur.fetchone() 
    Params.maf_thresh_individual_amb_upper_id=values[0] 
    Params.maf_thresh_individual_amb_upper=values[1]/100.0 


    #get maf individual high 
    query="Select id,value from parameters where group_name='"+str(parameter_group)+"'  and name like '%Reference - MAF for 2 Minor Alleles (lower bound%' order by id DESC limit 1;" 
    cur.execute(query)
    values=cur.fetchone()
    if values==None: 
        #use the default 
        query="select id,value from parameters where user_id=1 and name like '%Reference - MAF for 2 Minor Alleles (lower bound%';"
        cur.execute(query) 
        values=cur.fetchone() 
    Params.maf_thresh_individual_high_id=values[0] 
    Params.maf_thresh_individual_high=values[1]/100.0



    #get minimum number of calls to accept an allele 
    query="Select id,value from parameters where group_name='"+str(parameter_group)+"' and name like '%Minimum Reads per Locus%' order by id DESC limit 1;" 
    cur.execute(query)
    values=cur.fetchone()
    if values==None: 
        #use the default 
        query="select id,value from parameters where user_id=1 and name like '%Minimum Reads per Locus%';"
        cur.execute(query) 
        values=cur.fetchone() 
    Params.toolowthreshold_id=values[0] 
    Params.toolowthreshold=values[1]

    #get minimum ancestry contributing percentage to report 
    query="Select id,value from parameters where group_name='"+str(parameter_group)+"' and name like '%Minimum ancestry contributions to report (\%)%' order by id DESC limit 1;" 
    cur.execute(query)
    values=cur.fetchone()
    if values==None: 
        #use the default 
        query="select id,value from parameters where user_id=1 and name like '%Minimum ancestry contributions to report (\%)%';"
        cur.execute(query) 
        values=cur.fetchone() 
    Params.contributing_thresh_id=values[0] 
    Params.contributing_thresh=values[1]/100.0

    #get maximum contributing ancestries to report. 
    query="Select id,value from parameters where group_name='"+str(parameter_group)+"' and  name like '%Minimum ancestry contributions to report (integer)%' order by id DESC limit 1;" 
    cur.execute(query)
    values=cur.fetchone()
    if values==None: 
        #use the default 
        query="select id,value from parameters where user_id=1 and name like '%Minimum ancestry contributions to report (integer)%';"
        cur.execute(query) 
        values=cur.fetchone() 
    Params.maxtoreport_id=values[0] 
    Params.maxtoreport=values[1] 

    #get minimum number of SNPs that must be present to perform the ancestry computation. 
    query="Select id,value from parameters where group_name='"+str(parameter_group)+"' and name like '%Minimum number of Kidd SNPs present (integer 1 to 128)%' order by id DESC limit 1;" 
    cur.execute(query)
    values=cur.fetchone()
    if values==None: 
        #use the default 
        query="select id,value from parameters where user_id=1 and name like '%Minimum number of Kidd SNPs present (integer 1 to 128)%';"
        cur.execute(query) 
        values=cur.fetchone() 
    Params.minsnpspresent_id=values[0] 
    Params.minsnpspresent=values[1] 


    #find the number of algorithm iterations to be executed 
    query="Select id,value from parameters where group_name='"+str(parameter_group)+"' and name like '%Genetic algorithm runs for subject%';"
    cur.execute(query) 
    values=cur.fetchone() 
    if values==None: 
        #use the default 
        query="select id,value from parameters where user_id=1 and name like '%Genetic algorithm runs for subject%';"
        cur.execute(query) 
        values=cur.fetchone() 
    Params.runxtimes_id=values[0] 
    Params.runxtimes=int(values[1]) 

    #get ambiguous threshold 
    query="Select id,value from parameters where  group_name='"+str(parameter_group)+"' and name like '%Ambiguous Bias%' order by id DESC limit 1;" 
    cur.execute(query)
    values=cur.fetchone()
    if values==None: 
        #use the default 
        query="select id,value from parameters where user_id=1 and name like '%Ambiguous Bias%';"
        cur.execute(query) 
        values=cur.fetchone() 
    Params.ambiguous_thresh_id=values[0] 
    Params.ambiguous_thresh=values[1]/100.0 
    
    #get strand bias threshold 
    query="Select id,value from parameters where  group_name='"+str(parameter_group)+"' and name like '%Strand Bias%' order by id DESC limit 1;" 
    cur.execute(query)
    values=cur.fetchone()
    if values==None: 
        #use the default 
        query="select id,value from parameters where user_id=1 and name like '%Strand Bias%';"
        cur.execute(query) 
        values=cur.fetchone() 
    Params.strand_bias_thresh_id=values[0] 
    Params.strand_bias_thresh=values[1]/100.0


#Connect to the database                                                                                           
def connect(host,connecting_user,password,dbName):
    try:
        con = mdb.connect(host,connecting_user,password,dbName)
        cur = con.cursor()
        con.begin()
        #Execute a test query to make sure the database connection has been successful. 
        return con,cur

    except mdb.Error,e:
        error_message = e.__str__();
        print error_message
        sys.exit(0) 
    

#close connection to the database                                                                                
def disconnect(con,cur):
    try:
        con.commit(); 
        cur.close(); 
        con.close(); 
    except mdb.Error,e:
        error_message=e.__str__(); 
        print error_message
        sys.exit(0) 




def parseInputs(): 
    host=None
    db=None
    user=None
    password=None
    samples=[] 
    user_id=None 
    folder_id=None
    parameter_group=None
    quality=None 
    locus_group=0 
    sys.argv=[i.replace('\xe2\x80\x93','-') for i in sys.argv]
    for i in range(1,len(sys.argv)): 
        entry=sys.argv[i]
        if entry =='-h': 
            host=sys.argv[i+1] 
        elif entry=='-db': 
            db=sys.argv[i+1] 
        elif entry=='-u': 
            user=sys.argv[i+1] 
        elif entry=='-p': 
            password=sys.argv[i+1] 
        elif entry.__contains__('-sample'): 
            for j in range(i+1,len(sys.argv)): 
                if not sys.argv[j].startswith('-'): 
                    samples.append(sys.argv[j])
                else: 
                    break; 
        elif entry.__contains__('-id_user'): 
            user_id=sys.argv[i+1] 
            #print "set user id: "+str(user_id) 
        elif entry.__contains__('-id_folder'): 
            folder_id=sys.argv[i+1] 
        elif entry.__contains__('-parameter_group'): 
            parameter_group=sys.argv[i+1] 
        elif entry.__contains__('-quality'): 
            quality=int(sys.argv[i+1]) 
        elif entry.__contains__('-locus_group'): 
            locus_group=int(sys.argv[i+1]) 
            
    #make sure all the necessary arguments have been supplied 
    if host==None or db==None or user==None or password==None or len(samples)==0 or user_id==None or folder_id==None or locus_group==None or quality==None: 
        print "host:"+str(host) 
        print "db:"+str(db) 
        print "user:"+str(user) 
        print "password:"+str(password) 
        print "samples:"+str(samples) 
        print "user_id:"+str(user_id) 
        print "folder_id:"+str(folder_id) 
        print "locus_group:"+str(locus_group) 
        print "quality:"+str(quality) 
        usage() 
        sys.exit(0) 
    else: 
        return host,db,user,password,samples,user_id,folder_id,parameter_group,quality,locus_group 


    
def call_allele(tfract,afract,cfract,gfract): 
    alleles = ['T','A','C','G']; 
    freqs = [tfract,afract,cfract,gfract]
    
    highestfreq = max(freqs); 
    max_index = freqs.index(highestfreq); 
    allele1 = alleles[max_index]; 
    alleles.remove(alleles[max_index]); 
    freqs.remove(freqs[max_index]); 
    second_highest_freq = max(freqs); 
    if abs(highestfreq - second_highest_freq) <.2 : #heterozygote! 
        second_highest_freq_index = freqs.index(second_highest_freq); 
        allele2 = alleles[second_highest_freq_index]; 
    else: 
        allele2 = allele1; 
    return allele1,allele2; 

def get_pop_freqs(cur,locus_group,quality): #allele_freqs_file,regions_file,fst_file):     
    
    #get all the loci that are in the Kidd panel 
    query="Select locus_id,ethnicity_id,allele_frequency from frequencies where source='Kidd';"
    cur.execute(query) 
    locus_ids=cur.fetchall() 
    ethnicity_ids=[i[1] for i in locus_ids]
    allele_freqs=[i[2] for i in locus_ids] 
    locus_ids=[i[0] for i in locus_ids];     
    #Find the names of all populations and regions that are in the Kidd panel 
    #ethnicity_ids=list(set(ethnicity_ids))
    ethnicity_id_string='|'.join(list(set([str(i) for i in ethnicity_ids])))
    query="select id,name,geographic_id from ethnicities where (name !='global') and ( id REGEXP '("+ethnicity_id_string+")');"
    #print str(query) 
    cur.execute(query) 
    ethnicity_metadata=cur.fetchall() 
    ethnicity_id_to_name=dict() 
    regions=dict() 
    for i in ethnicity_metadata: 
        ethnicity_id=i[0] 
        ethnicity_name=i[1] 
        region=i[2] 
        ethnicity_id_to_name[ethnicity_id]=ethnicity_name 
        regions[ethnicity_id]=region 
    ethnicities=list(ethnicity_id_to_name.values()) 

    #remove globally-bad loci and loci not in the specified locus group 
    loci=set(filter_snps(cur,locus_ids,locus_group,quality))
    loci_string='|'.join([str(i) for i in loci])

    #get the ma freqs for each popuations for all loci. 
    #popfreqs: ethnicity-> locus_id -> allele_freq 
    popfreqs=dict() 
    for i in range(len(ethnicity_ids)): 
        ethnicity_id=ethnicity_ids[i] 
        locus_id=locus_ids[i]
        if locus_id not in loci: 
            continue #don't store any loci that are globally bad or not in the locus_group 
        allele_freq=allele_freqs[i] 
        if ethnicity_id not in popfreqs: 
            popfreqs[ethnicity_id]=dict() 
        popfreqs[ethnicity_id][locus_id]=allele_freq; 

    #get the FST value for each locus 
    query="select id,fst from loci where id REGEXP '("+loci_string+")';"
    cur.execute(query) 
    fst_data=cur.fetchall() 
    fstmap=dict() 
    for i in fst_data: 
        fstmap[i[0]]=i[1]  

    return loci,popfreqs,ethnicity_id_to_name,regions,fstmap 

#filters down the initial set of Kidd SNPs to remove globally bad loci as well as loci not in the specified locus group 
def filter_snps(cur,loci,locus_group,quality):
    loci=list(set(loci))
    loci_string='|'.join([str(i) for i  in loci])
    #remove the set of globally ambiguous or strand-biased loci 
    query="select locus_id from panel_loci where (locus_id REGEXP '("+loci_string+")') and ( quality_thresh="+str(quality)+")  and ((ambiguous/total_count >= "+str(Params.ambiguous_thresh)+") or (strand_bias/total_count >= "+str(Params.strand_bias_thresh)+"));"
    #print str(query) 
    cur.execute(query) 
    globally_bad_loci =set([i[0] for i in cur.fetchall()]) 
    remaining_loci=list(set(loci)-globally_bad_loci); 
    
    #find the set of loci that are in the locus group 
    if locus_group!="0": 
        query="select locus_id from loci_loci_groups where loci_group_id="+str(locus_group)+";" 
        cur.execute(query) 
        locus_group_loci=[i[0] for i in cur.fetchall()]
        remaining_loci = list(set(loci)-set(locus_group_loci))
    return remaining_loci; 


#get ma values for the sample 
def readdata(sample,cur,loci,popfreqs,locus_group,fst_map): 
    loci_string='|'.join([str(i) for i  in loci])
    #print "loci string for reading data:"+str(loci_string) 
    query="select locus_id,minor_allele_frequency,total_count,forward_count from calls where sample_id="+str(sample)+" and locus_id REGEXP '("+loci_string+")';"
    cur.execute(query) 
    locus_info=cur.fetchall() 
    #check to see if this is a failed sample -- too few Kidd loci are present 
    print "readdata found :"+str(len(locus_info)) +" loci" 
    if len(locus_info)< Params.minsnpspresent:
        return dict(),True 
    #store a dictionary of locus --> maf 
    sample_freqs=dict()
    for entry in locus_info: 
        #check to see if the locus is low, strand bias, or ambiguous 
        locus_id=entry[0] 
        maf=entry[1] 
        total=entry[2] 
        forward=entry[3] 
        
        if forward < Params.toolowthreshold: 
            continue 
        if (total -forward) < Params.toolowthreshold: 
            continue 
        if (maf > Params.maf_thresh_individual_low) and (maf < Params.maf_thresh_individual_high): 
            continue 
        if (maf > Params.maf_thresh_individual_amb_upper) and (maf < Params.maf_thresh_individual_high): 
            continue 
        
        sample_freqs[locus_id]=maf 
    #check again to see if too few SNPs passed the quality filtering 
    if len(sample_freqs.keys())< Params.minsnpspresent: 
        return dict(),True 

    #stores the probability of obsering the sample genotype | sample is a member of the specified population. 
    #format: population->locus->probability 
    sample_probs=dict()
    #print str(popfreqs.keys())
    for pop in popfreqs: 
        sample_probs[pop]=dict()
        #print str(popfreqs[pop]) 
        for locus in loci: 
            if locus not in sample_freqs: 
                continue 
            pop_ma=popfreqs[pop][locus]
            sample_ma= sample_freqs[locus]
            if pop==71: 
                query="select name from loci where id="+str(locus)+";" 
                cur.execute(query) 
                loc_name=cur.fetchone()[0] 
                print "india:"
                print "locus:"+str(locus)+","+str(loc_name)  
                print "pop_ma:"+str(pop_ma)+" sample_ma:"+str(sample_ma)
            
            if sample_ma <= Params.maf_thresh_individual_low:
                sample_probs[pop][locus]=(1-pop_ma)*(1-pop_ma)*fst_map[locus]*(1-abs(pop_ma-sample_ma))
            elif (sample_ma >=Params.maf_thresh_individual_amb) and (sample_ma <=Params.maf_thresh_individual_amb_upper):
                sample_probs[pop][locus]=(1-pop_ma)*pop_ma* fst_map[locus]*(1-abs(pop_ma-sample_ma))
            else:
                sample_probs[pop][locus]=pop_ma*pop_ma*fst_map[locus]*(1-abs(pop_ma-sample_ma))
            
    return sample_probs,False 

def usage(): 
    print "Usage: python ancestry_gen_alg.py -h <host ip> -db <database> -u <database user> -p <database password> -id_user <id of user running the analysis> -id_folder <id of folder where analysis results are to be stored> -samples [samples to analyze]"


def check_if_exists(samples,cur,locus_group): 
    samples.sort() 
    param_hash=str(Params.toolowthreshold_id)+str(Params.contributing_thresh_id)+str(Params.runxtimes_id)+str(Params.maxtoreport_id)+str(Params.minsnpspresent_id)+str(Params.maf_thresh_individual_low_id)+str(Params.maf_thresh_individual_amb_id)+str(Params.maf_thresh_individual_amb_upper_id)+str(Params.maf_thresh_individual_high_id)+str(Params.strand_bias_thresh)+str(Params.ambiguous_thresh)+str(locus_group) 
    internal_hash=param_hash+"Ancestries" 
    for sample in samples:
        query="select id from person_samples where sample_id="+str(sample)+';' 
        cur.execute(query) 
        person_sample_id=cur.fetchone()[0] 
        internal_hash=internal_hash+"_"+str(person_sample_id) 
    print "internal_hash checked:"+str(internal_hash) 
    internal_hash=hash(internal_hash)
    print "checking for hash:"+str(internal_hash) 
    query="select id from attachments where internal_hash="+str(internal_hash)+";"
    print str(query) 
    cur.execute(query) 
    found=cur.fetchone() 
    print str(found) 
    if found==None: 
        return [],-1 
    else: 
        attach_id=found[0] 
        #this analysis has already been done; get the people_samples associated with each sample 
        people_samples=[] 
        for sample in samples: 
            query="select id from person_samples where sample_id="+str(sample) 
            cur.execute(query) 
            person_id=cur.fetchone()[0] 
            people_samples.append(person_id) 
        return people_samples,attach_id 
        

#mids are a list
def main():
    host,db,user,password,samples,user_id,folder_id,parameter_group,quality,locus_group=parseInputs() 
    con,cur=connect(host,user,password,db)
    getParameters(cur,user_id,parameter_group)
    #get all Kidd-specific metadata 
    loci,popfreqs,races,regions,fst_map = get_pop_freqs(cur,locus_group,quality);


    numloci = len(loci);
    print "numloci:"+str(numloci) 
    ancestryAssignments=dict() 
    aggregateAncestries = dict(); 
    startingAncestries=dict() 
    all_fails=[]
    fails_for_check=[] 
    person_samples=[] 
    
    for sample in samples: 
        barcodedata,fail = readdata(sample,cur,loci,popfreqs,locus_group,fst_map);
        
        startingAncestries[sample]=barcodedata 
        if fail:
            query="select id from person_samples where sample_id="+str(sample)+";" 
            cur.execute(query) 
            fail_person_sample=cur.fetchone()[0] 
            all_fails.append(fail_person_sample) 
            fails_for_check.append(sample) 
    #check to see if analysis has already been done: 
    print "samples:"+str(samples) 
    print "fails_for_check:"+str(fails_for_check) 
    existing_ids,attach_id=check_if_exists(list(set(samples)-set(fails_for_check)),cur,locus_group)
    print "existing_ids:"+str(existing_ids) 
    '''
    if len(existing_ids) > 0: 
        existing="success "+str(existing_ids[0]) 
        for i in range(1,len(existing_ids)): 
            existing=existing+' '+str(existing_ids[i])
        existing_fail="fail" 
        for fid in all_fails: 
            existing_fail=existing_fail+' '+str(fid) 
        print "attachment_id "+str(attach_id) 
        print str(existing_fail) 
        print str(existing) 
        sys.exit(0) 
    '''
    #calculate the ancestry for each sample not in the fails group 
    for sample in list(set(samples)-set(fails_for_check)): 
        barcodedata=startingAncestries[sample]
        aggregateAncestries[sample]=dict() 
        #run the genetic algorithm a specified number of times and average the results across all the iterations. 
        #print "starting gen alg\n"
        for instance in range(Params.runxtimes):
           #create starting populations 
            population_pool = dict(); 
            for sourcePop in barcodedata:
                newPop = Population(); 
                newPop.contributors.append(sourcePop);
                newPop.allancestors.append(sourcePop); 
                newPop.probs = barcodedata[sourcePop]; 
                newPop.findFitness();
                if population_pool.__contains__(newPop.fitness): 
                    population_pool[newPop.fitness].append(newPop); 
                else: 
                    population_pool[newPop.fitness]=[newPop]; 

                print "sourcepop::"+str(sourcePop)
                print newPop.toString() 
            #print "starting population_pool:"+str(population_pool) 
            #starting conditions.             
            iter=0;
            improvement = 10; #percent improvement in fitness since the last generation, found by comparing the two most fit populations from gen_n and gen_n+1;         
            #ensure that the number of algorithm iterations exceeds a previously defined minimum. 
            while iter < Params.miniter or improvement > Params.minimprovement:  
                #find the most and least fit populations for this generation 
                topPops = findMostFitPopulations(population_pool,Params.percenttokeep); 
                #print "topPops:"+str(topPops) 
                
                #fail 
                #mate the most fit populations with each other to produce next generation 
                nextGen = getNextGen(topPops,loci);                
                #print str(nextGen) 
                improvement = getImprovement(topPops,nextGen); 
                #modify the population pool by adding any new, fitter populations and removing the least fit populations
                population_pool = selectForFitness(population_pool,nextGen); 
                iter+=1; 

            #assign ancestry to current barcode in consideration, this is a list of ancestries with an equally high fitness level in the context of the genetic algorithm. 
            Params.ancestry_assignments[sample] = assignAncestry(population_pool);
            for pop in Params.ancestry_assignments[sample]: 
                ancestorWeights = getAncestorWeights(pop); 
                for ancestor in ancestorWeights:
                    if aggregateAncestries[sample].__contains__(ancestor):
                        aggregateAncestries[sample][ancestor]+=ancestorWeights[ancestor]; 
                    else: 
                        aggregateAncestries[sample][ancestor]=ancestorWeights[ancestor]; 
    print str(aggregateAncestries) 
    if len(aggregateAncestries)>0: 
        person_samples,attach_id=createOutputFile(aggregateAncestries,races,regions,cur,user_id,folder_id,parameter_group,quality,locus_group) 
        recordAttachmentParameterMappings(cur,attach_id)     
    else: 
        person_samples=[]
        attach_id=-1
    disconnect(con,cur)
    #generate the output 
    print "attachment_id "+str(attach_id) 
    if len(all_fails)==0: 
        print "fail " 
    else: 
        all_fails_line=str(all_fails[0]) 
        for i in range(1,len(all_fails)): 
            all_fails_line=all_fails_line+" "+str(all_fails[i]) 
        print "fail "+all_fails_line
    if len(person_samples)==0: 
        print "success " 
    else: 
        person_sample_string=str(person_samples[0]) 
        for i in range(1,len(person_samples)): 
            person_sample_string=person_sample_string+ " "+str(person_samples[i]) 
        print "success "+person_sample_string 
if  __name__ =='__main__':main()
