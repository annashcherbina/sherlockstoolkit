import MySQLdb as mdb 
import os
import sys 
import Params; 
from Outputs import * 


def recordAttachmentParameterMappings(cur,attachment_id): 
    attachments=[attachment_id] 
    parameter_ids=[Params.maf_thresh_individual_amb_id,Params.maf_thresh_individual_low_id,Params.min_calls_id,Params.ambiguous_thresh_id,Params.strand_bias_thresh_id,Params.maf_thresh_individual_high_id,Params.maf_thresh_individual_amb_upper_id] 
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
        query="select id,value from parameters where user_id=1  and name like '%Reference - MAF for 0 Minor Alleles (upper bound%';"
        cur.execute(query) 
        values=cur.fetchone() 
    Params.maf_thresh_individual_low_id=values[0]
    Params.maf_thresh_individual_low=values[1]/100.0

    #get maf individual ambiguous 
    query="Select id,value from parameters where group_name='"+str(parameter_group)+"' and name like '%Reference - MAF for 1 Minor Allele (lower bound%' order by id DESC limit 1;" 
    cur.execute(query)
    values=cur.fetchone()
    if values==None: 
        #use the default 
        query="select id,value from parameters where user_id=1  and name like '%Reference - MAF for 1 Minor Allele (lower bound%';"
        cur.execute(query) 
        values=cur.fetchone() 
    Params.maf_thresh_individual_amb_id=values[0] 
    Params.maf_thresh_individual_amb=values[1]/100.0 

    #get maf individual high
    query="Select id,value from parameters where  group_name='"+str(parameter_group)+"' and name like '%Reference - MAF for 2 Minor Alleles (lower bound%' order by id DESC limit 1;" 
    cur.execute(query)
    values=cur.fetchone()
    if values==None: 
        #use the default 
        query="select id,value from parameters where user_id=1  and name like '%Reference - MAF for 2 Minor Alleles (lower bound%';"
        cur.execute(query) 
        values=cur.fetchone() 
    Params.maf_thresh_individual_high_id=values[0] 
    Params.maf_thresh_individual_high=values[1]/100.0

    #get maf individual 1 minor allele upper threshold 
    query="Select id,value from parameters where  group_name='"+str(parameter_group)+"' and name like '%Reference - MAF for 1 Minor Allele (upper bound%' order by id DESC limit 1;" 
    cur.execute(query)
    values=cur.fetchone()
    if values==None: 
        #use the default 
        query="select id,value from parameters where user_id=1  and name like '%Reference - MAF for 1 Minor Allele (upper bound%';"
        cur.execute(query) 
        values=cur.fetchone() 
    Params.maf_thresh_individual_amb_upper_id=values[0] 
    Params.maf_thresh_individual_amb_upper=values[1]/100.0 


    #get minimum number of calls to accept an allele 
    query="Select id,value from parameters where  group_name='"+str(parameter_group)+"' and name like '%Minimum Reads per Locus%' order by id DESC limit 1;" 
    cur.execute(query)
    values=cur.fetchone()
    if values==None: 
        #use the default 
        query="select id,value from parameters where user_id=1  and name like '%Minimum Reads per Locus%';"
        cur.execute(query) 
        values=cur.fetchone() 
    Params.min_calls_id=values[0] 
    Params.min_calls=values[1] 

    #get ambiguous threshold 
    query="Select id,value from parameters where group_name='"+str(parameter_group)+"' and name like '%Ambiguous Bias%' order by id DESC limit 1;" 
    cur.execute(query)
    values=cur.fetchone()
    if values==None: 
        #use the default 
        query="select id,value from parameters where user_id=1  and name like '%Ambiguous Bias%';"
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



def usage(): 
    print "Usage: python analyzeReplicates.py -h <host ip> -db <database> -u <database user> -p <database password> -id_user <id of user running the analysis> -id_folder <id of folder where analysis results are to be stored> -rep [replicate samples to analyze] -truth <optional replicate to treat as truth>"

def check_if_exists(cur,replicates,truth,quality,locus_group): 
    param_hash=str(Params.maf_thresh_individual_low_id)+str(Params.maf_thresh_individual_amb_id)+str(Params.min_calls_id)+str(Params.ambiguous_thresh_id)+str(Params.strand_bias_thresh_id)+str(Params.maf_thresh_individual_high_id)+str(Params.maf_thresh_individual_amb_upper_id)+str(quality)+str(locus_group)   
    rep_hist_name="ReplicateHist"
    if truth: 
        rep_hist_name=rep_hist_name+"_Reference_"
    for replicate in replicates: 
        rep_hist_name=rep_hist_name+"_"+str(replicate) 
    rep_hist_name=rep_hist_name+".png"
    rep_details_name="ReplicateDetails"
    if truth: 
        rep_details_name=rep_details_name+"_Reference__"
    for replicate in replicates:
        rep_details_name=rep_details_name+"_"+str(replicate) 
    rep_details_text=rep_details_name+".xlsx" 
    rep_details_png=rep_details_name+".png" 
    
    existing_ids=[] 

    #check if each of these file names has already been stored in the database. 
    rep_hist_name=hash(param_hash+rep_hist_name); 
    rep_details_text=hash(param_hash+rep_details_text) 
    rep_details_png=hash(param_hash+rep_details_png) 
    query="select id from images where internal_hash ="+str(rep_hist_name)+";" 
    cur.execute(query) 
    id_rep_hist=cur.fetchone() 
    print str(query) 
    print "id_rep_hist:"+str(id_rep_hist) 
    if id_rep_hist==None: 
        print "rep_hist_name:"+str(rep_hist_name) 
        print "rep_details_text:"+str(rep_details_text) 
        print "rep_details_png:"+str(rep_details_png) 
        return [],rep_hist_name,rep_details_text,rep_details_png
    else : 
        existing_ids.append(id_rep_hist[0])
    
    #rep_details_png=hash(param_hash+rep_details_png)
    query="select id from images where internal_hash ="+str(rep_details_png)+";"
    cur.execute(query) 
    id_det_png=cur.fetchone()
    print str(query) 
    print str(id_det_png) 
    if id_det_png ==None: 
        print "rep_hist_name:"+str(rep_hist_name) 
        print "rep_details_text:"+str(rep_details_text) 
        print "rep_details_png:"+str(rep_details_png) 
        return [],rep_hist_name,rep_details_text,rep_details_png
    else: 
        existing_ids.append(id_det_png[0]) 
    #rep_details_text=hash(param_hash+rep_details_text) 
    query="select id from attachments where internal_hash ="+str(rep_details_text)+";" 
    cur.execute(query) 
    id_det_text=cur.fetchone()
    print str(query) 
    print str(id_det_text) 
    if id_det_text==None: 
        print "rep_hist_name:"+str(rep_hist_name) 
        print "rep_details_text:"+str(rep_details_text) 
        print "rep_details_png:"+str(rep_details_png) 
        return [],rep_hist_name,rep_details_text,rep_details_png
    else:
        existing_ids.append(id_det_text[0])
    print "rep_hist_name:"+str(rep_hist_name) 
    print "rep_details_text:"+str(rep_details_text) 
    print "rep_details_png:"+str(rep_details_png) 
    return existing_ids,rep_hist_name,rep_details_text,rep_details_png

def parseInputs(): 
    host=None
    db=None
    user=None
    password=None
    replicates=[] 
    truth=[]
    user_id=None 
    folder_id=None
    parameter_group=None
    quality=None 
    locus_group=None 
    sys.argv=[i.replace('\xe2\x80\x93','-') for i in sys.argv]
    for i in range(1,len(sys.argv)): 
        entry=sys.argv[i]
        print "entry:"+str(entry) 
        if entry=='-h': 
            host=sys.argv[i+1] 
        elif entry=='-db': 
            db=sys.argv[i+1] 
        elif entry=='-u': 
            user=sys.argv[i+1] 
        elif entry=='-p': 
            password=sys.argv[i+1] 
        elif entry.__contains__('-rep'): 
            for j in range(i+1,len(sys.argv)): 
                if not sys.argv[j].startswith('-'): 
                    replicates.append(sys.argv[j])
                else: 
                    break; 
        elif entry.__contains__('-id_user'): 
            user_id=sys.argv[i+1] 
            #print "set user id: "+str(user_id) 
        elif entry.__contains__('-id_folder'): 
            folder_id=sys.argv[i+1] 
        elif entry.__contains__('-truth'): 
            for j in range(i+1,len(sys.argv)): 
                if not sys.argv[j].startswith('-'): 
                    truth.append(sys.argv[j]) 
                else:
                    break 
        elif entry.__contains__('-parameter_group'): 
            parameter_group=sys.argv[i+1] 
        elif entry.__contains__('-quality'): 
            quality=int(sys.argv[i+1]) 
        elif entry.__contains__('-locus_group'): 
            locus_group=int(sys.argv[i+1]) 
    #make sure all the necessary arguments have been supplied 
    if host==None or db==None or user==None or password==None or len(replicates)==0 or user_id==None or folder_id==None: 
        print "-1 incorrect parameters passed to function" 
        if host==None: 
            print " missing -host" 
        if db==None: 
            print " missing -db" 
        if user==None: 
            print " missing -u (database user)" 
        if password==None: 
            print " missing -p (database password)" 
        if replicates==None: 
            print " missing -rep (replicates)" 
        if user_id==None: 
            print " missing -id_user" 
        if folder_id==None: 
            print " missing -id_folder" 
        #usage() 
        sys.exit(0) 
    else: 
        return host,db,user,password,replicates,truth,user_id,folder_id,parameter_group,quality,locus_group
    
def get_sample_snps(maf_dict,cur,sample,globally_bad_snps,locus_group_snps): 
    ma_snps=set([]) 
    query="select minor_allele_frequency,locus_id,total_count,forward_count from calls where sample_id="+str(sample); 
    print str(query) 
    cur.execute(query) 
    sample_mafs=cur.fetchall() 
    print "there are " + str(len(sample_mafs)) +" loci" 

    use_locus_group=False 
    if len(locus_group_snps)>0: 
        use_locus_group=True 

    if sample_mafs==None or len(sample_mafs)==0: 
        return maf_dict,ma_snps 
    for entry in sample_mafs: 
        maf=entry[0] 
        locid=entry[1] 
        if locid in globally_bad_snps:
            continue 
        if use_locus_group and (locid not in locus_group_snps): 
            continue 
        total_count=int(entry[2]) 
        forward_count=int(entry[3]) 
        #filter low count, strand-biased, and ambiguous snps 
        #if forward_count < Params.min_calls: 
        #    continue         
        #if (total_count - forward_count) < Params.min_calls: 
        #    continue 
          
        #if (maf > Params.maf_thresh_individual_low) and (maf < Params.maf_thresh_individual_amb): 
        #    continue 
        
        #if (maf > Params.maf_thresh_individual_amb_upper) and (maf < Params.maf_thresh_individual_high): 
        #    continue 
        
        ma_snps.add(locid) 
        if locid not in maf_dict:
            maf_dict[locid]=dict() 
        maf_dict[locid][sample]=[maf,total_count,forward_count]  
    return maf_dict,ma_snps

def get_sample_metadata(replicates,cur):
    metadata_dict=dict()
    for rep in replicates: 
        query="select experiment_id,barcode_id from samples where id="+str(rep)+";"
        #print str(query) 
        cur.execute(query) 
        result=cur.fetchone()
        exp_id=result[0] 
        barcode_id=result[1] 
        query="select hash_name,name,primer_panel_id from experiments where id="+str(exp_id)+";" 
        cur.execute(query) 
        exp_hash_name,exp_name,panel_id=cur.fetchone() 
        query="select name from panels where id="+str(panel_id); 
        cur.execute(query) 
        panel_name=cur.fetchone()[0] 
        query="select name from barcodes where id="+str(barcode_id)+";"
        cur.execute(query) 
        barcode_name=cur.fetchone()[0]
        query="select person_id from person_samples where sample_id="+str(rep)+";" 
        cur.execute(query) 
        person_samples=cur.fetchall() 
        sources=set([]) 
        if len(person_samples) > 1: 
            person_string="Mixture:"
            for p in person_samples: 
                query="select id_code,source from people where id="+str(p)+";"
                cur.execute(query) 
                p_det=cur.fetchone() 
                p_name=p_det[0] 
                p_source=p_det[1] 
                source.add(p_source) 
                person_string=person_string+" "+str(p_name) 
        else: 
            query="select id_code,source from people where id="+str(person_samples[0][0])+";"
            #print str(query) 
            cur.execute(query)
            p_det=cur.fetchone() 
            person_string=p_det[0] 
            p_source=p_det[1] 
            sources.add(p_source) 
        metadata_dict[rep]=[exp_hash_name,barcode_name,person_string,exp_name,panel_name,sources] 
    return metadata_dict
def get_snp_to_pos(snps): 
    snp_to_pos=dict() 
    counter=0 
    for snp in snps: 
        snp_to_pos[snp]=counter 
        counter+=1
    print "snp_to_pos:"+str(snp_to_pos) 
    return snp_to_pos; 

def main():

    host,db,user,password, replicates, truth, user_id,folder_id,parameter_group,quality,locus_group=parseInputs() 
    print "replicates:"+str(replicates) 
    print "truth:"+str(truth) 
    if len(truth)==0: 
        truth=None 
    if truth: 
        replicates=set(replicates) 
        replicates.add(truth[0]) 
        replicates=list(replicates)
        if len(truth)>1: 
            print " -4 Only a single truth sample is allowed for a replicate comparison" 
            sys.exit(0)
        truth=truth[0] 
    replicates.sort() 
    if len(replicates)==1: 
        print " -2 More than one sample must be selected for replicate analysis" 
        sys.exit(0)
        truth=truth[0] 
    con,cur=connect(host,user,password,db);  
    getParameters(cur,user_id,parameter_group)
    #check to see if we already have the result of this analysis and if so, return the appropriate id's. 
    existing_ids,rep_hist_name,rep_details_text_name,rep_details_png_name=check_if_exists(cur,replicates,truth,quality,locus_group)
    existing_ids=[] 
    print "existing ids:"+str(existing_ids)
    if len(existing_ids) >  0: 
        id_string=str(existing_ids[0]) 
        for idval in existing_ids[1::]: 
            id_string=id_string+" "+str(idval)
        print "already exists!"
        print id_string 
        disconnect(con,cur) 
        sys.exit(0) 
    maf_dict=dict() 
    
    
    #get the globally bad snps 
    query="select locus_id from panel_loci where  quality_thresh="+str(quality)+"  and ((ambiguous/total_count >= "+str(Params.ambiguous_thresh)+") or (strand_bias/total_count >= "+str(Params.strand_bias_thresh)+"));"
    print str(query) 
    cur.execute(query) 
    globally_bad =cur.fetchall()
    if globally_bad==None: 
        globally_bad=[] 
    if globally_bad!=[]:
        globally_bad=[i[0] for i in globally_bad]; 
    
    #get the locus group name 
    if locus_group==0: 
        locus_group_name="Unspecified" 
    else: 
        query="select name from loci_groups where id="+str(locus_group)+";"
        cur.execute(query) 
        locus_group_name=cur.fetchone()[0]
    
    #get the locus group snps 
    locus_group_snps=[] 
    if locus_group!=0: 
        query="select locus_id from loci_loci_groups where loci_group_id="+str(locus_group)+";"  
        cur.execute(query) 
        locus_group_snps=[i[0] for i in cur.fetchall()] 
    
        
    loci=set([])
    for sample in replicates: 
        maf_dict,loci_for_sample=get_sample_snps(maf_dict,cur,sample,globally_bad,locus_group_snps)
        for snp in loci_for_sample: 
            loci.add(snp) 
    loci=list(loci) 
    
    snp_to_pos=get_snp_to_pos(maf_dict.keys()) 
    sample_metadata=get_sample_metadata(replicates,cur); 
    ###### Generate Output Files #####
    attachment_id=outputExcelSummary(maf_dict,loci,replicates,truth,rep_details_text_name,sample_metadata,cur,user_id,folder_id,parameter_group,quality,locus_group_name,locus_group_snps)
    details_image_id=outputDetailsImage(maf_dict,loci,replicates,truth,rep_details_png_name,sample_metadata,cur,user_id,folder_id,snp_to_pos,quality,locus_group_name) 
    hist_image_id=outputHistImage(maf_dict,loci,replicates,truth,rep_hist_name,sample_metadata,cur,user_id,folder_id,quality,locus_group_name) 
    query="update images set associated_image_id="+str(details_image_id)+ " where id="+str(hist_image_id)+";" 
    cur.execute(query) 
    query="update images set associated_image_id="+str(hist_image_id)+",associated_attachment_id="+str(attachment_id)+" where id="+str(details_image_id)+";" 
    cur.execute(query) 
    recordAttachmentParameterMappings(cur,attachment_id)    

    ###### Disconnect from the Database and write the id's of the Output Files######    
    disconnect(con,cur)
    print "ran from scratch!"
    print str(hist_image_id)+' '+str(details_image_id)+" "+ str(attachment_id)         


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



if __name__=='__main__': 
    main() 
