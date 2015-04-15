#this module generates kinship coefficient plot, kinship excel file, kinship machine learning coefficient matrix 
import MySQLdb as mdb 
import os
import sys 
import Params 
from Output import * 
from ml_helpers import * 
import pandas as pd; 
import time; 
from helpers import * 
from math import log,pow

def recordAttachmentParameterMappings(cur,attachment_id,training_module_id): 
    attachments=[attachment_id] 
    parameter_ids=[Params.max_0_ma_id, Params.min_1_ma_id,Params.min_calls_id, Params.ambiguous_thresh_id,Params.strand_bias_thresh_id,Params.strand_bias_thresh_id,Params.ambiguous_thresh_id,Params.min_2_ma_id,Params.max_1_ma_id,Params.max_impossible_id]
    print str(parameter_ids) 
    for attachment_id in attachments: 
        for param_id in parameter_ids: 
            query="insert into attachments_parameters (attachment_id,parameter_id,kinship_module_id) VALUES("+str(attachment_id)+","+str(param_id)+","+str(training_module_id)+");"
            print str(query) 
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
    Params.max_0_ma_id=values[0] 
    Params.max_0_ma=values[1]/100.0 
    

    #get maf individual ambiguous 
    query="Select id,value from parameters where group_name='"+str(parameter_group)+"' and name like '%Reference - MAF for 1 Minor Allele (lower bound%' order by id DESC limit 1;" 
    cur.execute(query)
    values=cur.fetchone()
    if values==None: 
        #use the default 
        query="select id,value from parameters where user_id=1 and name like '%Reference - MAF for 1 Minor Allele (lower bound%';"
        cur.execute(query) 
        values=cur.fetchone() 
    Params.min_1_ma_id=values[0] 
    Params.min_1_ma=values[1]/100.0
    


    #get maf individual threshold 
    query="Select id,value from parameters where  group_name='"+str(parameter_group)+"' and name like '%Reference - MAF for 1 Minor Allele (upper bound%' order by id DESC limit 1;" 
    cur.execute(query)
    values=cur.fetchone()
    if values==None: 
        #use the default 
        query="select id,value from parameters where user_id=1 and name like '%Reference - MAF for 1 Minor Allele (upper bound%';"
        cur.execute(query) 
        values=cur.fetchone() 
    Params.max_1_ma_id=values[0] 
    Params.max_1_ma=values[1]/100.0 
    

    #get maf individual ambiguous 
    query="Select id,value from parameters where  group_name='"+str(parameter_group)+"' and name like '%Reference - MAF for 2 Minor Alleles (lower bound%' order by id DESC limit 1;" 
    cur.execute(query)
    values=cur.fetchone()
    if values==None: 
        #use the default 
        query="select id,value from parameters where user_id=1 and name like '%Reference - MAF for 2 Minor Alleles (lower bound%';"
        cur.execute(query) 
        values=cur.fetchone() 
    Params.min_2_ma_id=values[0] 
    Params.min_2_ma=values[1]/100.0
    


    #get minimum number of calls to accept an allele 
    query="Select id,value from parameters where  group_name='"+str(parameter_group)+"'  and name like '%Minimum Reads per Locus%' order by id DESC limit 1;" 
    cur.execute(query)
    values=cur.fetchone()
    if values==None: 
        #use the default 
        query="select id,value from parameters where user_id=1 and name like '%Minimum Reads per Locus%';"
        cur.execute(query) 
        values=cur.fetchone() 
    Params.min_calls_id=values[0] 
    Params.min_calls=values[1] 
    

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
    
#get max impossible 
    query="Select id,value from parameters where  group_name='"+str(parameter_group)+"' and name like '%Maximum Impossible for Kinship%' order by id DESC limit 1;"
    #print str(query) 
    cur.execute(query) 
    values=cur.fetchone() 
    if values==None: 
        #use the default 
        query="select id,value from parameters where user_id=1 and name like  '%Maximum Impossible for Kinship%';"
        cur.execute(query) 
        values=cur.fetchone() 
    Params.max_impossible_id=values[0] 
    Params.max_impossible=values[1] 


def count_ma(maf): 
    if maf <= Params.max_0_ma: 
        return 0 
    elif (maf >= Params.min_1_ma) and (maf <= Params.max_1_ma): 
        return 1
    elif(maf>=Params.min_2_ma): 
        return 2
    else:
        print "-6: count_ma returned an impossible case!!: " + str(maf) 
        sys.exit(0) 

def get_H_H2(snp_dict,loci,samples): 
    H=0 
    H2=0 
    for locus in loci:
        p_hat=0
        AA=0
        Aa=0
        aa=0
        badlocus=False 
        for sample in samples: 
            if locus in snp_dict[sample] and snp_dict[sample][locus][1]>=Params.min_calls:
                #check for ambiguous calls 
                if  (snp_dict[sample][locus][0]> Params.max_0_ma) and (snp_dict[sample][locus][0] < Params.min_1_ma): 
                    badlocus=True
                    continue 
                if  (snp_dict[sample][locus][0]> Params.max_1_ma) and (snp_dict[sample][locus][0] < Params.min_2_ma): 
                    badlocus=True 
                    continue 
                maf_count=count_ma(snp_dict[sample][locus][0]) 
                #print str(maf_count) 
                if maf_count==2: 
                    aa+=1
                if maf_count==1: 
                    Aa+=1
                if maf_count==0: 
                    AA+=1
        if badlocus==True: 
            continue 
        if (AA+Aa+aa)==0:
            continue 
        #print "aa:"+str(aa)+" Aa:"+str(Aa)+" AA:"+str(AA) 
        p_hat=(AA+0.5*Aa)/(AA+Aa+aa) 
        #p_hat=p_hat/float(len(samples)) 
        H+=2*p_hat*(1-p_hat) 
        H2+=2*(p_hat**2)*(1-p_hat)**2 
    return H,H2 

def get_origins(samples,cur): 
    origin_dict=dict() 
    origin_dict_named=dict() 
    for sample in samples: 
        query="select person_id from person_samples where sample_id="+str(sample)+";"
        cur.execute(query) 
        person_id=cur.fetchone()[0]
        query="select self_reported_ancestry from people where id="+str(person_id)+";" 
        print str(query) 
        cur.execute(query); 
        ancestry=cur.fetchone()[0].split(',') 
        origin_dict_named[sample]=ancestry[0] 
        #origin_dict_named[sample]='EUROPE' 
        if '' in ancestry: 
            ancestry.remove('') 
        ancestry='|'.join(ancestry); 
        query="select id from geographics where region_name REGEXP '("+ancestry+")';"; 
        #print str(query)
        cur.execute(query) 
        regions=[i[0] for i in cur.fetchall()] 
        regions.sort(reverse=True) 
        #origin_dict[sample]=[6]
        origin_dict[sample]=regions        
        if regions=='': 
            print "no origin information:"+str(sample) 
    print "origin_dict_named:"+str(origin_dict_named) 
    return origin_dict,origin_dict_named

    
def get_gender(samples,snp_dict,loci,cur): 
    #find all the X_snps 
    locinames='|'.join([str(i) for i in loci])
    query="select id from loci where chromosome=\"X\" and id REGEXP'("+locinames+")';"; 
    cur.execute(query) 
    xloci=[i[0] for i in cur.fetchall()]
    print "XLOCI:"+str(xloci) 
    gender_dict=dict() 
    for sample in samples:
        
        numheter=0 
        for locus in xloci:
            if locus in snp_dict[sample]: 
                maf=snp_dict[sample][locus][0] 
                total=snp_dict[sample][locus][1]
                forward=snp_dict[sample][locus][2] 
                rev=total-forward
                if maf >=Params.min_1_ma and maf <=Params.max_1_ma: 
                    if min([forward,rev])>=Params.min_calls: 
                        numheter+=1 
        if numheter >0: 
            gender_dict[sample]="f" 
        else: 
            gender_dict[sample]="m" 
    return gender_dict 
            
def get_pair_features(samples,snp_dict,loci,cur,gender_dict): 
    #also create a Data Frame for a straight-forward interface with Joe's machine learning module 
    origins,origins_string=get_origins(samples,cur) 
    gender_dict_named=dict()
    origins_named=dict() 
    df=pd.DataFrame(columns=['ID1','ID2','marker','IBS0','KinC','mashared','nSharedLoci','x00','x01','x02','x11','x12','x22','relationship','degree','expectedshareddna','origins'],index=range(int((len(samples)-1)*len(samples)*.5)))
    H,H2=get_H_H2(snp_dict,loci,samples) 
    #print "H:"+str(H) 
    #print "H2:"+str(H2) 
    comparison_index=-1
    for i in range(len(samples)): 
        s1=samples[i]
        query="select person_id from person_samples where sample_id="+str(s1)+";"
        cur.execute(query) 
        person1=cur.fetchone()[0]
        query="select id_code from people where id="+str(person1)+";" 
        cur.execute(query) 
        person1name=cur.fetchone()[0]
        gender_dict_named[person1name]=gender_dict[s1] 
        origins_named[person1name]=origins_string[s1] 
        person1origin=origins[s1]
        for j in range(i+1,len(samples)): 
            comparison_index+=1 
            s2=samples[j]
            key=tuple([s1,s2]) 
            query="select person_id from person_samples where sample_id="+str(s2)+";" 
            cur.execute(query) 
            person2=cur.fetchone()[0] 
            query="select id_code from people where id="+str(person2)+";" 
            cur.execute(query) 
            person2name=cur.fetchone()[0] 
            gender_dict_named[person2name]=gender_dict[s2] 
            origins_named[person2name]=origins_string[s2] 
            mashared=0 
            maperson1total=0 
            maperson2total=0 
            nsharedloci=0 
            ma00=0 
            ma01=0 
            ma02=0 
            ma11=0 
            ma12=0 
            ma22=0 
            N_Aa_i=0 #number of heterozygous loci for subject 1 
            N_aa_i=0 #number of homozygous minor loci for subject 1
            N_Aa_j=0 #number of heterozygous loci for subject 2 
            N_aa_j=0 #number of homozygous minor loci for subject 2 
            #get truth information about relationship 
            query="select relation,degree,expected_shared_alleles from relationships where person_id="+str(person1)+" and person2_id="+str(person2)+";" 
            #print str(query) 
            cur.execute(query) 
            rel_info=cur.fetchone()
            #print "rel_info:"+str(rel_info) 
            if rel_info==None: 
                #unrelated
                relationship="unrelated" 
                expected_shared_alleles=0 
                degree='-1' 
            else:
                relationship=rel_info[0] 
                degree=str(rel_info[1]) 
                expected_shared_alleles=rel_info[2]
            #print "total:"+str(len(loci))
            for locus in loci: 
                if locus not in snp_dict[s1]: 
                    #print "s1 missing:"+str(locus) 
                    continue 
                if locus not in snp_dict[s2]: 
                    #print "s2 missing:"+str(locus) 
                    continue 
                #ignore cases where either sample has low count, strand-biased, ambiguous snp 
                if snp_dict[s2][locus][2]<Params.min_calls: 
                    #print "s2 forward strand :"+str(snp_dict[s2][locus][2])
                    continue 
                if (snp_dict[s2][locus][1]-snp_dict[s2][locus][2]) < Params.min_calls: 
                    #print "s2 rev strand:"+str(snp_dict[s2][locus][1]-snp_dict[s2][locus][2]) 
                    continue 
                if snp_dict[s1][locus][2]< Params.min_calls: 
                    #print "s1 forward strand:"+str(snp_dict[s1][locus][2]) 
                    continue 
                if (snp_dict[s1][locus][1]-snp_dict[s1][locus][2])< Params.min_calls: 
                    #print "s1 rev strand :"+str(snp_dict[s1][locus][1]-snp_dict[s1][locus][2])
                    continue 
                if  (snp_dict[s1][locus][0]> Params.max_0_ma) and (snp_dict[s1][locus][0] < Params.min_1_ma): 
                    continue 
                if (snp_dict[s1][locus][0]> Params.max_1_ma) and (snp_dict[s1][locus][0] < Params.min_2_ma): 
                    continue 
                if  (snp_dict[s2][locus][0]> Params.max_0_ma) and (snp_dict[s2][locus][0] < Params.min_1_ma): 
                    continue 
                if (snp_dict[s2][locus][0] > Params.max_1_ma) and (snp_dict[s2][locus][0] < Params.min_2_ma): 
                    continue 
                nsharedloci+=1 
                ma_s1=count_ma(snp_dict[s1][locus][0]) 
                ma_s2=count_ma(snp_dict[s2][locus][0]) 
                maperson1total+=ma_s1
                maperson2total+=ma_s2
                if ma_s1==1: 
                    N_Aa_i+=1
                if ma_s1==2: 
                    N_aa_i+=1 
                if ma_s2==1: 
                    N_Aa_j+=1 
                if ma_s2==2: 
                    N_aa_j+=1 
                if ma_s1==0 and ma_s2==0: 
                    ma00+=1                     
                elif ma_s1==0 and ma_s2==1: 
                    ma01+=1 
                    #print "ma01:"+str(ma01) 
                elif ma_s1==0 and ma_s2==2: 
                    ma02+=1 
                elif ma_s1==2 and ma_s2==0: 
                    ma02+=1 
                elif ma_s1==1 and ma_s2==0: 
                    ma01+=1 
                elif ma_s1==1 and ma_s2==1: 
                    ma11+=1 
                    mashared+=1 
                elif ma_s1==1 and ma_s2==2: 
                    ma12+=1 
                    mashared+=1 
                elif ma_s1==2 and ma_s2==1: 
                    ma12+=1 
                    mashared+=1 
                elif ma_s1==2 and ma_s2==2: 
                    ma22+=1 
                    mashared+=2 
            #print "person1name:"+str(person1name) 
            #print "person2name:"+str(person2name) 
            #print "nsharedloci:"+str(nsharedloci) 
            #print "N_Aa_i:"+str(N_Aa_i) 
            #print "N_Aa_j:"+str(N_Aa_j) 
            #print "N_aa_i:"+str(N_aa_i) 
            #print "N_aa_j:"+str(N_aa_j) 
            person2origin=origins[s2] 
            combined_origins=(person1origin+person2origin)
            combined_origins.sort(reverse=True)    
            print "combined_origins:"+str(combined_origins) 
            combined_origins=int(''.join([str(i) for i in combined_origins]))
            #KinCoef, heterogeneous formula with correction 
            if min(N_Aa_i,N_Aa_j)==0: 
                tScore=-1 
            else: 
                tScore = (ma11-2*ma02)/float(2*min(N_Aa_i,N_Aa_j))+.5-.25*((N_Aa_i+N_Aa_j)/float(min(N_Aa_i,N_Aa_j)))
                sScore = (ma11-2*ma02)/float(2*H)+.5-(N_Aa_i+N_Aa_j)/float(4*H)
            #Pr(IBS=0)
            pScore = (ma02)/float(H2)
            phi_t=tScore
            
            #phi=(ma11+ma12+ma22)/((N_Aa_i+N_aa_i+N_Aa_j+N_aa_j)/2.0)
            pi0=pScore 
            #mashared=2*mashared/float((N_Aa_i+2*N_aa_i+N_Aa_j+2*N_aa_j))
            #mashared=float((2*ma11)+(2*ma12)+(4*ma22))/((2*ma02+3*ma12+ 2*ma11+ ma01+4*ma22))
            #mashared=float(2*ma22+ma12+ma11)/(ma01+ma02+ma11+ma12+ma22)
            #print "maperson1total:"+str(maperson1total) 
            #print "maperson2total:"+str(maperson2total) 
            if maperson1total==0: 
                mashared=0 
            elif maperson2total==0: 
                mashared=0 
            else: 
                mashared=((mashared/float(maperson1total))+(mashared/float(maperson2total)))/2.0
            
            if float(degree) <4:
                if relationship in Params.relationToMarker:
                    pmark=Params.relationToMarker[relationship] 
                else: 
                    pmark=Params.relationToMarker[Params.equivalence[relationship]]
            else: 
                pmark=Params.relationToMarker[str(degree)] 
            
            df['ID1'][comparison_index]=person1name
            df['ID2'][comparison_index]=person2name
            df['marker'][comparison_index]=pmark 
            df['IBS0'][comparison_index]=pScore
            df['KinC'][comparison_index]=tScore 
            df['x22'][comparison_index]=ma22
            df['x11'][comparison_index]=ma11
            df['x02'][comparison_index]=ma02
            df['x01'][comparison_index]=ma01
            df['x00'][comparison_index]=ma00 
            df['x12'][comparison_index]=ma12 
            df['nSharedLoci'][comparison_index]=nsharedloci
            df['mashared'][comparison_index]=mashared 
            if relationship in Params.equivalence: 
                relationship=Params.equivalence[relationship] 
            df['relationship'][comparison_index]=relationship 
            df['degree'][comparison_index]=degree 
            df['expectedshareddna'][comparison_index]=expected_shared_alleles 
            df['origins'][comparison_index]=combined_origins
    #print "PAIR FEATURES DATAFRAME:"+str(df)
    return df,gender_dict_named,origins_named


def get_maf(samples,cur,locus_group_snps,globally_bad): 
    snp_dict=dict() 
    loci=set([]) 
    for sample in samples: 
        query="select locus_id,minor_allele_frequency,total_count,forward_count from calls where sample_id="+str(sample)+";" 
        cur.execute(query) 
        calls=cur.fetchall() 
        snp_dict[sample]=dict() 
        for call in calls: 
            locus_id=call[0]
            if locus_group_snps!="All": 
                if locus_id not in locus_group_snps: 
                    continue 
            if locus_id in globally_bad: 
                continue 
            loci.add(locus_id) 
            maf=call[1] 
            total=call[2] 
            forward_count=call[3] 
            snp_dict[sample][locus_id]=[float(maf),int(total),int(forward_count)] 
            
    return snp_dict ,loci 

def usage(): 
    print "Usage: python computeKinship.py -h <host ip> -db <database> -u <database user> -p <database password> -id_user <id of user running the analysis> -id_folder <id of folder where analysis results are to be stored> -samples [samples to analyze]"
def check_if_exists(cur,samples,locus_group,training_module):
    param_hash=str(Params.max_0_ma_id)+str(Params.min_1_ma_id)+str(Params.max_1_ma_id)+str(Params.min_2_ma_id)+str(Params.min_calls_id)+str(Params.ambiguous_thresh_id)+str(Params.strand_bias_thresh_id)+str(Params.max_impossible_id)+str(locus_group)+str(training_module)+ str(time.strftime("%H:%M:%S")) 
    existing_ids=[] 
    samples.sort() 
    kin_name=param_hash 
    for sample in samples: 
        kin_name=kin_name+"_"+sample
    kin_name_image="kin"+kin_name
    print str(kin_name_image) 
    kin_name_image=hash(kin_name_image) 
    
    query="select id from images where internal_hash ="+str(kin_name_image)+";"
    print str(query) 
    cur.execute(query) 
    id_kin=cur.fetchone()
    print "id_kin_image:"+str(id_kin) 
    if id_kin==None: 
        return [] 
    else: 
        existing_ids.append(id_kin[0]) 
    
    kin_coef_file="kin"+kin_name
    kin_coef_file=hash(kin_coef_file) 
    query="select id from attachments where internal_hash="+str(kin_coef_file)+";"
    cur.execute(query) 
    id_kin=cur.fetchone()
    print "id_kin_excel:"+str(id_kin)
    if id_kin==None: 
        return [] 
    else: 
        existing_ids.append(id_kin[0]) 

    return existing_ids 
    
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
    training_module=None 
    locus_group=0
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
            locus_group=sys.argv[i+1] 
            if locus_group=='0': 
                locus_group=0 
        elif entry.__contains__('-training_module'): 
            training_module=sys.argv[i+1] 
            if len(training_module)==0: 
                print "-5: Please specify the name of the training module to use for kinship" 
                sys.exit(0) 

      
    #make sure all the necessary arguments have been supplied 
    if host==None or db==None or user==None or password==None or len(samples)==0 or user_id==None or folder_id==None: 
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
        usage() 
        print "-1 Incorrect parameters specified. Must be:"+usage() 
        sys.exit(0) 
    else: 
        return host,db,user,password,samples,user_id,folder_id,parameter_group,quality,locus_group,training_module 

def getBayesian(cur,snp_dict,pair_dict,loci): 
    #print "len(loci):"+str(len(loci)) 
    confusion=dict()
    outf=[] 
    gens=range(1,Params.smax_degree_bayes+1)
    gens.append("unrelated") 
    for i in gens: 
        confusion[i]=dict() 
        for j in gens: 
            confusion[i][j]=0 
    rel_names=dict()
    rel_names['unrelated']='unrelated'
    rel_names[1]='parent' 
    rel_names[2]='grandparent' 
    rel_names[3]='great grandparent' 
    rel_names[4]='great great grandparent' 
    for gen in range(5,len(gens)): 
        rel_names[gen]=gen 
    max_impossible=Params.max_impossible
    maf_dict=dict() 
    query="select id from ethnicities where name=\"global\";" 
    cur.execute(query) 
    global_id=cur.fetchone()[0] 
    query="select locus_id,allele_frequency from frequencies where ethnicity_id="+str(global_id)+";"
    cur.execute(query) 
    freqvals=cur.fetchall() 
    for y in freqvals: 
        maf_dict[y[0]]=y[1] 
    for sample in snp_dict: 
        for sample2 in snp_dict: 
            if sample2==sample: 
                continue
            query="select person_id from person_samples where sample_id="+str(sample)+";"; 
            cur.execute(query) 
            person_id=cur.fetchall() 
            person1_id=person_id[0][0] 
            query="select id_code from people where id="+str(person1_id)+";" 
            cur.execute(query) 
            person1_name=cur.fetchone()[0] 
            
            query="select person_id from person_samples where sample_id="+str(sample2)+";"; 
            cur.execute(query) 
            person_id=cur.fetchall() 
            person2_id=person_id[0][0] 
            query="select id_code from people where id="+str(person2_id)+";" 
            cur.execute(query) 
            person2_name=cur.fetchone()[0]  
            query="select relation from relationships where person_id="+str(person1_id) +" and person2_id="+str(person2_id)+";" 
            cur.execute(query) 
            truth=cur.fetchone()
            if truth==None: 
                truth="unrelated" 
            else: 
                truth=truth[0] 
            if truth in Params.equivalence: 
                truth=Params.equivalence[truth] 
            if truth not in ['parent','grandparent','great grandparent','great great grandparent','great great great grandparent','unrelated']:
                continue 
            ref_tallies=dict() 
            target_tallies=dict() 
            #print str(snp_dict[sample])
            #print "size snp_dict[sample]:"+str(len(snp_dict[sample]))
            for snp in loci: 
                if snp not in snp_dict[sample]: 
                    #print "skipping sample" 
                    continue 
                if snp not in snp_dict[sample2]: 
                    #print "skipping sample2" 
                    continue
                maf_ref=snp_dict[sample][snp][0] 
                maf_target=snp_dict[sample2][snp][0] 
                #print "maf_ref:"+str(maf_ref) 
                #print "maf_target:"+str(maf_target) 
                ref_count=-1 
                target_count=-1 
                if maf_ref <= Params.max_0_ma: 
                    ref_count=0 
                elif (maf_ref >= Params.min_2_ma): 
                    ref_count=2
                elif (maf_ref >=Params.min_1_ma) and (maf_ref<=Params.max_1_ma): 
                    ref_count=1 
                
                if maf_target <= Params.max_0_ma: 
                    target_count=0 
                elif (maf_target > Params.min_2_ma): 
                    target_count=2
                elif (maf_target >=Params.min_1_ma) and (maf_target <=Params.max_1_ma):
                    target_count=1
                #print "ref_count:"+str(ref_count) 
                #print "target_count:"+str(target_count) 
                if (ref_count > -1): 
                    ref_tallies[snp]=ref_count 
                else: 
                    ref_tallies[snp]="NoCall" 
                if target_count>-1: 
                    target_tallies[snp]=target_count
                else: 
                    target_tallies[snp]="NoCall" 
            gen_ma_freq=dict() 
            gen_genotypes=dict() 
            p_target=dict() 
            for gen in gens:
                #print "gen:"+str(gen) 
                #print "ref_tallies:"+str(ref_tallies) 
                #print "len(ref_tallies):"+str(len(ref_tallies))
                gen_ma_freq[gen]=dict()
                gen_genotypes[gen]=dict() 
                p_target[gen]=dict() 
                for snp in ref_tallies: 
                    maf=maf_dict[snp] 
                    #print "ref_tallies[snp]:"+str(ref_tallies[snp]) 
                    #print "target tallies[snp]:"+str(target_tallies[snp]) 
                    if ref_tallies[snp]=="NoCall":
                        #print "case 1" 
                        gen_ma_freq[gen][snp]=False
                        gen_genotypes[gen][snp]=False 
                        p_target[gen][snp]=0                 
                        continue
                    else: 
                        #print "case 2" 
                        gen_ma_freq[gen][snp]=maf_freq(maf,gen,ref_tallies[snp])
                        gen_genotypes[gen][snp]=get_genotype(maf,gen,ref_tallies[snp]) 
                    if target_tallies[snp]=="NoCall": 
                        #print "case 3" 
                        p_target[gen][snp]=0 
                        continue
                    elif target_tallies[snp]==0 and ref_tallies[snp]==2: 
                        #print "FOUND IMPOSSIBLE CASE" 
                        #print "gen:"+str(gen)
                        #print "case 4" 
                        if gen==1:
                            p_target[gen][snp]="X" 
                        elif gen_genotypes[gen][snp]==False: 
                            p_target[gen][snp]=0 
                        elif gen_genotypes[gen][snp][0]==0: 
                            p_target[gen][snp]=0 
                        else: 
                            p_target[gen][snp]=log(gen_genotypes[gen][snp][0],10) 
                    elif ref_tallies[snp]==0 and target_tallies[snp]==2: 
                        #print "FOUND IMPOSSIBLE CASE"
                        #print "gen:"+str(gen) 
                        #print "case 5" 
                        if gen==1: 
                            p_target[gen][snp]="X"
                        elif gen_genotypes[gen][snp]==False: 
                            p_target[gen][snp]=0 
                        elif gen_genotypes[gen][snp][2] <=0: 
                            p_target[gen][snp]=0 
                        else:
                            p_target[gen][snp]=log(gen_genotypes[gen][snp][2],10) 
                    elif target_tallies[snp]==0:
                        #print "case 6" 
                        if gen_genotypes[gen][snp][0]==0: 
                            p_target[gen][snp]=0 
                        else: 
                            p_target[gen][snp]=log(gen_genotypes[gen][snp][0],10)
                    elif target_tallies[snp]==1: 
                        #print "case 7" 
                        if gen_genotypes[gen][snp][1]==0: 
                            p_target[gen][snp]=0 
                        else: 
                            p_target[gen][snp]=log(gen_genotypes[gen][snp][1],10) 
                    elif target_tallies[snp]==2: 
                        #print "case 8" 
                        if gen_genotypes[gen][snp][2]==0: 
                            p_target[gen][snp]=0 
                        else: 
                            p_target[gen][snp]=log(gen_genotypes[gen][snp][2],10) 
            #Sum the logarithmic values and keep track of impossible snps 
            gensum=dict() 
            for gen in gens: 
                gensum[gen]=0
            gen1impossible=0 
            for snp in target_tallies: 
                for gen in gens: 
                    if gen==1 and p_target[1][snp]=="X": 
                        gen1impossible+=1 
                        #print "gen1impossible:"+str(gen1impossible) 
                    else: 
                        gensum[gen]+=p_target[gen][snp] 

            #summarize the output
            sum_ref_ma_ma=0 
            sum_ref_ma_MA=0 
            sum_ref_MA_MA=0 
            sum_target_ma_ma=0 
            sum_target_ma_MA=0 
            sum_target_MA_MA=0 
            sum_gen_genotypes=dict() 
            for gen in gens: 
                sum_gen_genotypes[gen]=[0,0,0] 

            for snp in ref_tallies: 
                if ref_tallies[snp]==2: 
                    sum_ref_ma_ma+=1 
                elif ref_tallies[snp]==1: 
                    sum_ref_ma_MA+=1 
                elif ref_tallies[snp]==0: 
                    sum_ref_MA_MA+=1 
                if target_tallies[snp]==2:
                    sum_target_ma_ma+=1 
                elif target_tallies[snp]==1: 
                    sum_target_ma_MA+=1 
                elif target_tallies[snp]==0: 
                    sum_target_MA_MA+=1
                for gen in gens:
                    if gen_genotypes[gen][snp]!=False: 
                        sum_gen_genotypes[gen][0]+=gen_genotypes[gen][snp][0] 
                        sum_gen_genotypes[gen][1]+=gen_genotypes[gen][snp][1] 
                        sum_gen_genotypes[gen][2]+=gen_genotypes[gen][snp][2] 
            
            out_line=[person1_name,person2_name,truth,str(sum_ref_ma_ma),str(sum_ref_ma_MA),str(sum_ref_MA_MA),str(sum_gen_genotypes['unrelated'][2]),str(sum_gen_genotypes['unrelated'][1]),str(sum_gen_genotypes['unrelated'][0])]
            for gen in gens: 
                if gen=='unrelated': 
                    continue 
                out_line=out_line+[str(sum_gen_genotypes[gen][2]),str(sum_gen_genotypes[gen][1]),str(sum_gen_genotypes[gen][0])]
            out_line=out_line+[str(sum_target_ma_ma),str(sum_target_ma_MA),str(sum_target_MA_MA),str(gen1impossible)]
            for gen in gens: 
                out_line=out_line+[str(gensum[gen])]
            degree_rel=Params.degree[truth][0] 
            if degree_rel not in confusion: 
                confusion[degree_rel]=dict() 
            if gen1impossible> Params.max_impossible: 
                gensum[1]=float("-inf") 
            for gen in gens:
                if gen=='unrelated': 
                    continue 
                if gensum[gen]==0: 
                    gensum[gen]=float("-inf") 
                gensum[gen]=gensum[gen]-gensum['unrelated'] 
            gensum['unrelated']=0 
    
            maxval=max(gensum.values())
            for gen in gens: 
                if gensum[gen]==maxval: 
                    confusion[gen][degree_rel]+=1 
                    out_line=out_line+[str(rel_names[gen])]
                    if truth in Params.degree: 
                        #print "degree truth bayes:"+str(Params.degree[truth])
                        #print "degree rel_names[gen]:"+str(rel_names[gen]) 
                        if Params.degree[truth][0]==gen:
                            out_line=out_line+['True'] 
                        else: 
                            out_line=out_line+['False']
                    else: 
                        #print "truth bayes:"+str(truth) 
                        #print "rel_names[gen]:"+str(rel_names[gen])
                        if str(truth)==str(rel_names[gen]):
                            out_line=out_line+['True'] 
                        else: 
                            out_line=out_line+['False'] 
                            
            outf.append(tuple(out_line))
    out_confusion=[]
    out_cline=["","",'Truth']
    out_confusion.append(tuple(out_cline))
    out_cline=[""] 
    for gen in gens: 
        out_cline=out_cline+[str(rel_names[gen])]
    out_confusion.append(tuple(out_cline))
    out_cline=["Predicted"]
    out_confusion.append(out_cline) 
    for i in gens:
        out_cline=[] 
        out_cline=out_cline+[str(i)] 
        for j in gens: 
            out_cline=out_cline+[str(confusion[i][j])]
        out_confusion.append(tuple(out_cline))
    #print "outf:"+str(outf) 
    #print "out_confusion:"+str(out_confusion) 
    return outf,out_confusion

def main():
    #failure
    host,db,user,password, samples, user_id,folder_id,parameter_group,quality,locus_group,training_module=parseInputs()
    #need at least 2 samples for kinship analysis 
    if len(samples) <2: 
        print "-2 More than 1 sample must be specified for kinship analysis" 
        sys.exit(0) 
    
    con,cur=connect(host,user,password,db); 
    getParameters(cur,user_id,parameter_group) 
    locus_group_name=""
    if locus_group!=0: 
        query="select name from loci_groups where id="+str(locus_group)+";" 
        cur.execute(query) 
        locus_group_name=cur.fetchone() 
        if locus_group_name!=None: 
            locus_group_name=locus_group_name[0] 
    for sample in samples: 
        query="select experiment_id from samples where id="+str(sample)+";" 
        cur.execute(query) 
        exp_id=cur.fetchone()[0] 
        query="select primer_panel_id from experiments where id="+str(exp_id)+";" 
        cur.execute(query) 
        panel_id=cur.fetchone()[0] 
        query="select description from panels where id="+str(panel_id)+";" 
        cur.execute(query) 
        panel_description=cur.fetchone()[0].lower() 
        '''
        if panel_description.__contains__('kinship')==False: 
            print "-4 All samples must be from the Kinship panel to perform kinship analysis."
            disconnect(con,cur) 
            sys.exit(0)  
        '''
    query="select description from panels where id="+str(panel_id)+";" 
    cur.execute(query) 
    panel_name=cur.fetchone()[0] 
    if locus_group_name=="":
        locus_group_name=panel_name 
    #existing_ids=check_if_exists(cur,samples,locus_group,training_module)
    existing_ids=[] 
    if len(existing_ids)>0:
        print "already exists!" 
        output_string=str(existing_ids[0])
        for i in range(1,len(existing_ids)): 
            output_string=output_string+" "+str(existing_ids[i])
        print str(output_string) 
        sys.exit(0) 
    #get the list of SNPs to use from the specific locus group 
    if locus_group !=0: 
        query="select locus_id from loci_loci_groups where loci_group_id="+str(locus_group)+";"
        cur.execute(query) 
        locus_group_snps=cur.fetchall()
        locus_group_snps=[i[0] for i in locus_group_snps]; 
    else: 
        locus_group_snps='All' 
    print "locus_group_snps:"+str(locus_group_snps) 

    #get the set of globally bad snps 
    query="select locus_id from panel_loci where quality_thresh="+str(quality)+" and ((ambiguous/total_count >="+str(Params.ambiguous_thresh)+") or (strand_bias/total_count >="+str(Params.strand_bias_thresh)+"));"
    cur.execute(query) 
    globally_bad_loci=set([i[0] for i in cur.fetchall()]) 
    print "globally_bad_loci:"+str(globally_bad_loci) 
    #get the full set of minor alleles for each sample 
    snp_dict,loci=get_maf(samples,cur,locus_group_snps,globally_bad_loci) 
    print "got maf" 
    #assign gender to subjects, or label unknown 
    gender_dict=get_gender(samples,snp_dict,loci,cur) 
    
    #keep track of features that will be used for further computation and the machine learning step 
    pair_dict,gender_dict,ancestry_dict=get_pair_features(samples,snp_dict,loci,cur,gender_dict)
    cPickle.dump(gender_dict,open('/usr/local/mitll/dev_backend/kinship_2.0/genderdict.pkl','wb'))
    print "got pair features" 
    #print "pair_dict:"+str(pair_dict) 
    details_degree,allele_combos_degree,confusionMatrix_degree,header_degree,labels_degree=getConfusionMatrix(pair_dict,'degree',training_module,cur) 
    cPickle.dump(details_degree,open('/usr/local/mitll/dev_backend/kinship_2.0/dictionary.pkl','wb'))
    cPickle.dump(allele_combos_degree,open('/usr/local/mitll/dev_backend/kinship_2.0/allelecombos.pkl','wb')) 
    
    pedigree_im_id,fam_tree_im_id=generatePedigreeGraph(details_degree,cur,samples,user_id,folder_id,training_module,quality,locus_group_name,allele_combos_degree,gender_dict,ancestry_dict) 

    print "labels degree:"+str(labels_degree) 
    print "got confusion matrix degree" 
    details_rel,allele_combos_rel,confusionMatrix_rel,header_rel,labels_rel=getConfusionMatrix(pair_dict,'relationship',training_module,cur) 
    print "labels rel:"+str(labels_rel) 
    print "got confusion matrix relationship" 
    #get the Bayesian relationship probability calculations
    #bayes_details,bayes_confusion=getBayesian(cur,snp_dict,pair_dict,loci) 
    bayes_details=None 
    bayes_confusion=None 
    image_id=plotKinCoef(pair_dict,cur,samples,user_id,folder_id,training_module,quality,locus_group_name)
    excel_id=excelOutput(pair_dict,cur,samples,user_id,folder_id,confusionMatrix_degree,header_degree,details_degree,labels_degree,confusionMatrix_rel,details_rel,header_rel,labels_rel,parameter_group,bayes_details,bayes_confusion,training_module,quality,locus_group_name,locus_group_snps) 
    #set the associated image id for the pedigree graph and the king plot 
    query="update images set associated_image_id="+str(pedigree_im_id)+",associated_image2_id="+str(fam_tree_im_id)+", associated_attachment_id="+str(excel_id)+ " where id="+str(image_id)+";" 
    cur.execute(query) 
    query="update images set associated_image_id="+str(image_id)+",associated_image2_id="+str(fam_tree_im_id)+", associated_attachment_id="+str(excel_id)+" where id="+str(pedigree_im_id)+";" 
    cur.execute(query) 
    query="update images set associated_image_id="+str(image_id)+",associated_image2_id="+str(pedigree_im_id)+",associated_attachment_id="+str(excel_id) + " where id="+str(fam_tree_im_id)+";" 
    cur.execute(query) 
    #query="update images set associated_attachment_id="+str(excel_id) +" where id="+str(image_id)+";" 
    #cur.execute(query)
    query="select id from kinship_training_modules where name=\""+str(training_module)+"\";" 
    cur.execute(query) 
    training_module_id=cur.fetchone()[0]
    recordAttachmentParameterMappings(cur,excel_id,training_module_id) 
    disconnect(con,cur) 
    print str(image_id)+" " +str(excel_id) 

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
        print "-3 "+error_message
        sys.exit(0) 
    

#close connection to the database                                                                                
def disconnect(con,cur):
    try:
        con.commit(); 
        cur.close(); 
        con.close(); 
    except mdb.Error,e:
        error_message=e.__str__(); 
        print "-3 "+error_message
        sys.exit(0) 




if __name__=="__main__":
    main() 
