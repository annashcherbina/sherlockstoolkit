#This module will draw an S-curve for a set of selected profiles. 
import MySQLdb as mdb 
import os
import sys 
import Params 
from Outputs import * 

def recordAttachmentParameterMappings(attachment,cur): 
    attachments=[attachment] 
    parameter_ids=[Params.min_calls_id]
    print str(parameter_ids) 
    for attachment_id in attachments: 
        for param_id in parameter_ids: 
            query="insert into attachments_parameters (attachment_id,parameter_id) VALUES("+str(attachment_id)+","+str(param_id)+");"
            cur.execute(query) 

def getParameters(cur,user_id,parameter_group):
    #get minimum number of calls to accept an allele 
    query="Select id,value from parameters where user_id="+str(user_id)+" and group_name='"+str(parameter_group)+"' and name like '%Minimum Reads per Locus%' order by id DESC limit 1;" 
    cur.execute(query)
    values=cur.fetchone()
    if values==None: 
        #use the default 
        query="select id,value from parameters where user_id=1 and name like '%Minimum Reads per Locus%';"
        cur.execute(query) 
        values=cur.fetchone() 
    Params.min_calls_id=values[0] 
    Params.min_calls=values[1] 



def usage(): 
    print "Usage: python qcSamples.py -h <host ip> -db <database> -u <database user> -p <database password> -id_user <id of user running the analysis> -id_folder <id of folder where analysis results are to be stored> -samples [samples to analyze]"
def check_if_exists(cur,samples,locus_group):
    samples.sort() 
    existing=[] 
    param_hash=str(Params.min_calls_id) +str(locus_group) 
    qc_name=param_hash+"qc" 
    for sample in samples: 
        qc_name=qc_name+"_"+sample 
    qc_name=hash(qc_name) 
    query="select id from images where internal_hash ="+str(qc_name)+";"
    print str(query) 
    cur.execute(query) 
    id_qc=cur.fetchone()
    if id_qc==None: 
        return []
    else: 
        existing.append(id_qc[0]) 
    
    query="select id from attachments where internal_hash ="+str(qc_name)+";"
    print str(query) 
    cur.execute(query) 
    id_qc=cur.fetchone()
    if id_qc==None: 
        return []
    else: 
        existing.append(id_qc[0]) 
    return existing

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
        elif entry.__contains__('-samples'): 
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
    if host==None or db==None or user==None or password==None or len(samples)==0 or user_id==None or folder_id==None or locus_group==None or  quality==None: 
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
            print " missing -samples (samples)" 
        if user_id==None: 
            print " missing -id_user" 
        if folder_id==None: 
            print " missing -id_folder" 
        if locus_group==None: 
            print " missing -locus_group" 
        if quality==None: 
            print "missing -quality" 
        #usage() 
        sys.exit(0) 
    else: 
        return host,db,user,password,samples,user_id,folder_id,parameter_group,locus_group,quality


def main(): 
    host,db,user,password, samples, user_id,folder_id,parameter_group,locus_group,quality=parseInputs() 

    con,cur=connect(host,user,password,db); 
    getParameters(cur,user_id,parameter_group) 
    existing_id=check_if_exists(cur,samples,locus_group) 
    if existing_id!=[]: 
        print "Image already exists!"
        print str(existing_id[0])+ " " + str(existing_id[1])  
        sys.exit(0) 
    
    #if a locus group is specified, limit the analysis only to snps within the locus group 
    locus_group_name="Unspecified" 
    locus_group_snps=[] 
    if locus_group!=0: 
        query="select locus_id from loci_loci_groups where loci_group_id="+str(locus_group)+";" 
        cur.execute(query)
        locus_group_snps=[i[0] for i in cur.fetchall()] 
        query="select name from loci_groups where id="+str(locus_group)+";" 
        cur.execute(query) 
        locus_group_name=cur.fetchone()[0]
    sample_to_ma=dict()
    snp_to_freq=dict() 
    for i in range(len(samples)): 
        sample=samples[i] 
        sample_to_ma[sample]=[] 
        query="select minor_allele_frequency,total_count,forward_count,locus_id from calls where sample_id="+str(sample)+";"
        cur.execute(query) 
        ma_data=cur.fetchall() 
        for entry in ma_data: 
            maf=entry[0] 
            counts=entry[1]
            forward_counts=entry[2] 
            locus_id=entry[3] 
            if locus_id not in snp_to_freq: 
                snp_to_freq[locus_id]=dict() 
            snp_to_freq[locus_id][sample]=[maf,counts,forward_counts] 
            if (locus_group !=0) and locus_id not in locus_group_snps: 
                continue 
            if forward_counts <Params.min_calls: 
                maf=-.1*(i+1) 
            if (counts - forward_counts)< Params.min_calls: 
                maf=-.1*(i+1) 
            sample_to_ma[sample].append(maf) 


    for sample in sample_to_ma: 
        sample_to_ma[sample].sort() 
    
    image_id=generate_image(sample_to_ma,cur,user_id,folder_id,quality,locus_group_name,locus_group) 
    attachment_id=generate_attachment(sample_to_ma,cur,user_id,folder_id,parameter_group,quality,locus_group_name,locus_group_snps,locus_group,snp_to_freq) 
    query="update images set associated_attachment_id="+str(attachment_id)+" where id="+str(image_id)+";" 
    cur.execute(query) 
    recordAttachmentParameterMappings(attachment_id,cur)
    disconnect(con,cur) 
    print str(image_id) + " " + str(attachment_id) 
    
                



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
