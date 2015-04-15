################################
#machine learning functions to train, test and predict pariwise relationships
#given genotypes and (optionally) training labels
#output: prediction model and error statistics (if training is provided)
#################################
import sys 
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import confusion_matrix,f1_score
from sklearn.cross_validation import LeaveOneOut
from sklearn.svm import SVC
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale,StandardScaler, LabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import Lasso
import pandas as pd; 
import numpy as np; 
import cPickle; 
import Params; 
import os.path
####################################################################
def trainModel(df,len_df,X,Y,rel_degree,featClass,training_model,cluster=False):
    #print "TRAINING NEW MODEL!!" 
    #print "len_df:"+str(len_df) 
    #print str(df.values) 
    if cluster:
        param = {'n_clusters':np.arange(1,7)}
        kmcCV = GridSearchCV(KMeans(),param)
        kMeansPredClass = pd.DataFrame(columns=['kmeans'],index=range(len_df))
        A = kmcCV.fit(X,cv=LeaveOneOut(len(X)))
        #print kmcCV.best_estimator_
        kMeansPredClass['kmeans'] = A.best_estimator_.predict(X)
        kMeansPredClass['kmeans']=kMeansPredClass['kmeans']/float(kMeansPredClass['kmeans'].max())
        X=X.join(kMeansPredClass,how='inner')
    #run over parameter space
    param_rbf={'C':np.logspace(-2,5,8),'gamma':np.logspace(-5,-1,5)}
    gsCV = GridSearchCV(SVC(kernel='linear'),param_rbf,score_func=f1_score,n_jobs=-1)

    #Fit the svm
    #print "X:"+str(X) 
    #print "Y:"+str(Y) 
    B = gsCV.fit(X,Y,cv=LeaveOneOut(len_df))
   # cPickle.dump(B.best_estimator_,open('/usr/local/mitll/dev_backend/kinship_2.0/'+training_model+'_best_estimator_'+str(rel_degree)+".pkl",'wb'))
   # cPickle.dump(featClass,open('/usr/local/mitll/dev_backend/kinship_2.0/'+training_model+'_featClass_'+str(rel_degree)+".pkl",'wb'))
    #print SVM performance
    #print B
    #print B.best_score_
    #print B.best_params_
    #print B.best_estimator_
    return B.best_estimator_
####################################################################


def extractFeatures(df,features,classColumn,means,maxes):
    cval=-1
    featClass = dict()
    y=pd.DataFrame(columns=['class'],index=range(len(df)))
    for row in df.index:
        if df[classColumn][row] in featClass:
            y['class'][row]=featClass[df[classColumn][row]]
        else:
            cval+=1
            featClass[df[classColumn][row]]=cval
            y['class'][row]=cval
    df=df.join(y,how='inner')
    #grab feature vector from dataFrame
    fv = df[features]
    #print str(fv) 
    #normalize features

    if (len(means)==0 and len(maxes)==0):
        for col in fv:
            means.append(fv[col].mean()) 
            maxes.append(fv[col].abs().max())
            fv[col]=(fv[col]-fv[col].mean())/fv[col].abs().max()
    else: 
        ind=-1
        for col in fv:
            ind+=1 
            fv[col]=(fv[col]-means[ind])/maxes[ind]

    #invert feature class and return object
    featClassi=dict()
    for k in featClass.keys():
        featClassi[featClass[k]]=k
    #print str(fv) 
    return fv,df,featClassi,means,maxes


def getConfusionMatrix(df,degree_or_rel,training_module,cur): 
    print "in get confusion matrix" 
    means=[] 
    maxes=[] 
    norm_exists=False 
    query="select normalization from kinship_training_modules where name = \""+training_module+"\";"
    cur.execute(query) 
    normalization=cur.fetchone()[0] 
    #print "normalization:"+str(normalization) 
    if normalization!=None:       
        print "normalization is not none!" 
        norm_pickle=cPickle.loads(normalization)
        means=norm_pickle[0] 
        maxes=norm_pickle[1]
        norm_exists=True 
    fv_rel,df_rel,featClass_rel,means,maxes = extractFeatures(df,['mashared','KinC','x00','x01','x02','x11','x12','x22','nSharedLoci','origins'],degree_or_rel,means,maxes)
    print "got features" 
    if norm_exists==False: 
        norm_pickle=cPickle.dumps(tuple([means,maxes]))
        query="Update kinship_training_modules set normalization=%s;"
        cur.execute(query,norm_pickle) 
    best_estimator_rel=None 
    featClass_rel_pickle=None 
    #print "degree_or_rel:"+str(degree_or_rel) 
    if degree_or_rel=="degree": 
        query="select estimator_degree,feature_class_degree  from kinship_training_modules where name=\""+str(training_module)+"\";"
        cur.execute(query) 
        trainvals=cur.fetchone()
        #print "trainvals:"+str(trainvals) 
        if trainvals[0]!=None: 
            best_estimator_rel=cPickle.loads(trainvals[0]) 
            featClass_rel_pickle=cPickle.loads(trainvals[1]) 
    elif degree_or_rel=="relationship": 
        query="select estimator_relationship,feature_class_relationship from kinship_training_modules where name=\""+str(training_module)+"\";" 
        cur.execute(query) 
        trainvals=cur.fetchone()
        if trainvals[0]!=None: 
            best_estimator_rel=cPickle.loads(trainvals[0]) 
            featClass_rel_pickle=cPickle.loads(trainvals[1]) 

    if best_estimator_rel==None: 
        print "estimator is none!" 
        if len(df_rel)<10: 
            print "-6: Not enough samples selected to train a new SVM classifier. Please select at least 10 samples to train a new model" 
            sys.exit(0) 
    if best_estimator_rel==None: 
        #train a new estimator!
        print "estimator is none: training new module" 
        best_estimator_rel=trainModel(df_rel,len(df_rel),fv_rel,df_rel['class'],degree_or_rel,featClass_rel,training_module) 
        featClass_rel_pickle=featClass_rel 
        #store the estimator that was generate 
        estimator_pickle=cPickle.dumps(best_estimator_rel) 
        featclass_pickle=cPickle.dumps(featClass_rel_pickle) 
        if degree_or_rel=="degree": 
            query="Update kinship_training_modules set estimator_degree=%s;"
            query2="Update kinship_training_modules set feature_class_degree=%s;"
        elif degree_or_rel=="relationship": 
            query="Update kinship_training_modules set estimator_relationship=%s;" 
            query2="Update kinship_training_modules set feature_class_relationship=%s;"
        cur.execute(query,estimator_pickle) 
        cur.execute(query2,featclass_pickle) 
    #print "featClass_rel:"+str(featClass_rel) 
    #print "featClass_rel_pickle:"+str(featClass_rel_pickle)
    #print "fv_rel:"+str(fv_rel) 
    predClass_rel = best_estimator_rel.predict(fv_rel)
    print "predClass_rel:"+str(predClass_rel)
    predClassToText=[] 
    for rel in predClass_rel:
        predClassToText.append(featClass_rel_pickle[rel])
    print "predClassToText:"+str(predClassToText) 
    person1=df_rel.ID1
    person2=df_rel.ID2
    truth_rel=df_rel.relationship    

    ma_shared=df_rel.mashared
    expectedShared=df_rel.expectedshareddna    
    ma00=df_rel.x00
    ma01=df_rel.x01 
    ma02=df_rel.x02
    ma11=df_rel.x11
    ma12=df_rel.x12
    ma22=df_rel.x22
    ibs0=df_rel.IBS0
    kinc=df_rel.KinC
    details_rel=dict() 
    allele_combos=dict() 
    header_rel=['Person1','Person2','TrueRelationship','PredictedRelationship','Correct Prediction?','Minor Alleles Shared','Expected Minor Alleles Shared']
    for i in range(len(person1)): 
        #num_ma_shared=float(ma_numerator[i])/float(ma_denominator[i])
        ismatch=False 
        if degree_or_rel=="relationship":
            if str(truth_rel[i])==str(predClassToText[i]): 
                ismatch=True 
        elif str(truth_rel[i]).__contains__('unrelated') and str(predClassToText[i])=="-1": 
            ismatch=True
        else:
            if str(Params.degree[truth_rel[i]][0])==str(predClassToText[i]): 
                ismatch=True 
        details_rel[i]=[str(person1[i]),str(person2[i]),str(truth_rel[i]),str(predClassToText[i]),str(ismatch),str(ma_shared[i]),str(float(expectedShared[i])/100.0)]
        allele_combos[i]=[str(person1[i]),str(person2[i]),str(ma00[i]),str(ma01[i]) ,str(ma02[i]), str(ma11[i]),str(ma12[i]),str(ma22[i]),str(ibs0[i]),str(kinc[i])]
    featClass_rel_pickle_rev=dict() 
    for i in featClass_rel_pickle: 
        v=featClass_rel_pickle[i] 
        featClass_rel_pickle_rev[v]=i 
    max_pickle_index=max(featClass_rel_pickle.keys()) 
    used_indices=[] 
    for i in range(len(df_rel['class'])): 
        v=featClass_rel[df_rel['class'][i]]
        if v not in featClass_rel_pickle_rev: 
            df_rel['class'][i]=max_pickle_index+1 
            used_indices.append(max_pickle_index+1) 
            featClass_rel_pickle[max_pickle_index+1]=v 
            featClass_rel_pickle_rev[v]=max_pickle_index+1 
            max_pickle_index+=1 
        else: 
            df_rel['class'][i]=featClass_rel_pickle_rev[v] 
            used_indices.append(featClass_rel_pickle_rev[v]) 
    print "df_rel[class] remapped:"+str(df_rel['class']) 
    cf_m=confusion_matrix(df_rel['class'],predClass_rel) 
    used_indices=set(used_indices) 
    extra_keys=[] 
    for k in featClass_rel_pickle.keys(): 
        if (k not in used_indices) and (k not in predClass_rel): 
            extra_keys.append(k) 
    for k in extra_keys: 
        featClass_rel_pickle.__delitem__(k) 
    order = np.sort(featClass_rel_pickle.keys())
    print "order:"+str(order) 
    dflabels=list()
    for k in order:
        dflabels.append(featClass_rel_pickle[k])
    print str(cf_m) 
    cf_df_rel = pd.DataFrame(cf_m,columns=dflabels,index=dflabels)
    return details_rel,allele_combos,cf_df_rel,header_rel,dflabels
