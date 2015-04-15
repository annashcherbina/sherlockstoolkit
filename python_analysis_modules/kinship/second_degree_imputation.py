import Params
from Node import * 
import copy 
import random
#determines relationship between two nodes in the tree 
#p1 is the --- of p2 (i.e. mother, child, son, daughter) 
def get_relationship(p1,p2,p1_ancestors,p2_ancestors):
    #print "entering get_relationship" 
    p1_gen_max=max(p1_ancestors.keys()) 
    p2_gen_max=max(p2_ancestors.keys()) 
    path=None
    for p1_gen in range(p1_gen_max+1): 
        #print "p1_gen:"+str(p1_gen) 
        p1_anc_set=p1_ancestors[p1_gen] 
        for p2_gen in range(p2_gen_max+1):
            #print "p2_gen:"+str(p2_gen) 
            p2_anc_set=p2_ancestors[p2_gen] 
            if len(p1_anc_set.intersection(p2_anc_set))> 0: 
                path=tuple([p1_gen,p2_gen])
                break 
        if path!=None: 
            break 
    if path==None: 
        return "unrelated",-1 
    if path in Params.steps_to_relationship: 
        #print "path:"+str(path) 
        relationship=Params.steps_to_relationship[path][p1.gender]
        degree_rel=int(Params.degree[relationship][0]) 
    else: 
        if int(path[0])==0 or int(path[1])==0: 
            relationship='dir. descent degree '+str(int(path[0])+int(path[1]))
            degree_rel=int(path[0])+int(path[1])
        else: 
            relationship='indir. descent degree '+str(int(path[0])+int(path[1])-1)
            degree_rel=int(path[0])+int(path[1])-1 
    return relationship,degree_rel 


#finds all the ancestors of a node and organizes into dictionary by level. 
def get_ancestors(n,tree):
    encountered=dict()     
    ancestor_dict=dict() 
    ancestor_dict[0]=set([n.name])
    encountered[n.name]=1 
    if len(n.parents)>0: 
        has_parent=True 
    else: 
        has_parent=False
    cur_gen=[n.name] 
    gen=1
    while has_parent:
        new_gen=set([]) 
        for i in cur_gen: 
            encountered[i]=1 
            new_gen=new_gen.union(tree[i].parents)
        ancestor_dict[gen]=new_gen 
        gen+=1 
        cur_gen=new_gen 
        has_parent=False 
        for i in cur_gen: 
            if i in encountered:
                continue
                #print tree[i].toString() 
                #print "FOUND A LOOP!!!" 
                #print str(encountered) 
                #print str(ancestor_dict) 
                #print str(cur_gen) 
                #return None 
            if len(tree[i].parents)>0: 
                has_parent=True 
                break 
    #instead of storing names, store nodes
    ancestor_dict_node=dict() 
    for key in ancestor_dict: 
        ancestor_dict_node[key]=set([tree[i] for i in list(ancestor_dict[key])])
    #print "exiting get ancestors" 
    return ancestor_dict_node

def get_truth_relationships(tree): 
    print "entering get_truth_relationships" 
    ancestors=dict() 
    truth_rel=dict() 
    #get all relationships in the truth tree 
    people=tree.keys() 
    for p in people: 
        ancestors[tree[p]]=get_ancestors(tree[p],tree)
    predicted_people=tree.keys() 
    for p1_index in range(len(predicted_people)): 
        p1=tree[predicted_people[p1_index]]
        #if p1.name.__contains__('Unknown'): 
        #    continue 
        if len(p1.parents)==0 and len(p1.children)==0: 
            continue 
        for p2_index in range(p1_index+1,len(predicted_people)):
            p2=tree[predicted_people[p2_index]] 
            #if p2.name.__contains__('Unknown'): 
            #    continue 
            if len(p2.parents)==0 and len(p2.children)==0: 
                continue 
            rel,degree=get_relationship(p1,p2,ancestors[p1],ancestors[p2])
            truth_rel[tuple([p1.name,p2.name])]=[rel,degree] 
    return truth_rel 

#counts up errors between the known truth and a proposed addition to the tree 
def get_errors(truth_relationships,tree_proposed,rel_dict):         
    print "entering get_errors" 
    predicted_rel=dict() 
    ancestors=dict()

    relationship_errors=0 
    #degree_errors=0 

    #get all the relationships in the predicted tree 
    people=tree_proposed.keys() 
    for p in people: 
        ancestors[p]=get_ancestors(tree_proposed[p],tree_proposed)
        if ancestors[p]==None: 
            #there is a loop! 
            return float("inf") 
    predicted_people=tree_proposed.keys() 
    for p1_index in range(len(predicted_people)): 
        p1=predicted_people[p1_index]
        #if p1.__contains__('Unknown'): 
        #    continue 
        if len(tree_proposed[p1].children)==0 and len(tree_proposed[p1].parents)==0: 
            continue 
        for p2_index in range(p1_index+1,len(predicted_people)):
            p2=predicted_people[p2_index] 
            #if p2.__contains__('Unknown'): 
            #    continue 
            if len(tree_proposed[p2].children)==0 and len(tree_proposed[p2].parents)==0: 
                continue 
            entry=tuple([p1,p2])
            if entry in truth_relationships: 
                truth_rel=truth_relationships[entry][0] 
                truth_degree=truth_relationships[entry][1]
                if truth_degree <4: 
                    #check for a contradiction
                    rel,degree=get_relationship(tree_proposed[p1],tree_proposed[p2],ancestors[p1],ancestors[p2])
                    if truth_rel!=rel: 
                        if truth_degree==-1: 
                            continue
                            #relationship_errors+=0.1
                        else:
                            diff=max([degree,truth_degree])-min([degree,truth_degree])
                            relationship_errors+=1/float(diff) 
                            print "p1:"+str(p1) 
                            print "p2:"+str(p2) 
                            print "truth_degree:"+str(truth_degree) 
                            print "predicted_degree:"+str(degree) 
                        
            else: 
                entry=tuple([p2,p1]) 
                rel,degree=get_relationship(tree_proposed[p2],tree_proposed[p1],ancestors[p2],ancestors[p1]) 
                if entry in truth_relationships: 
                    truth_rel=truth_relationships[entry][0] 
                    truth_degree=truth_relationships[entry][1] 
                    if truth_degree < 4: 
                        rel,degree=get_relationship(tree_proposed[p2],tree_proposed[p1],ancestors[p2],ancestors[p1])
                        if rel!=truth_rel:
                            if truth_degree==-1:
                                #relationship_errors+=0.1
                                continue 
                            else: 
                                diff=max([degree,truth_degree])-min([degree,truth_degree])
                                relationship_errors+=1/float(diff) 
                                print "p2:"+str(p2) 
                                print "p1:"+str(p1) 
                                print "truth_degree:"+str(truth_degree) 
                                print "predicted_degree:"+str(degree)
                else: 
                    #the combination of p1 and p2 is not in the truth tree. Check the degree of relationship from machine learning 
                    if degree < 4: #we won't count errors in 4th degree and higher relationships since these are predicted 
                        if entry in rel_dict: 
                            truth_degree=int(rel_dict[entry][1]) 
                            if truth_degree != degree: 
                                print "truth_degree:"+str(truth_degree) 
                                print "degree:"+str(degree) 
                                diff=max([degree,truth_degree])-min([degree,truth_degree])
                                relationship_errors+=1/float(diff) 
                                print "p2:"+str(p2) 
                                print "p1:"+str(p1) 
                                print "truth_degree:"+str(truth_degree) 
                                print "predicted_degree:"+str(degree)                                 
    return relationship_errors
    

def test_second_tree_rels(tree,p1,p2,rel_dict,combo_dict,married_in,connectivity):
    print "entering test_second_tree_rels" 
    truth_rel=get_truth_relationships(tree)
    if tuple([p1,p2]) in truth_rel and truth_rel[tuple([p1,p2])][0]!="unrelated": 
        print "ALREADY EXISTS!:"+str(truth_rel[tuple([p1,p2])])  
        return tree,0 
    if tuple([p2,p1]) in truth_rel and truth_rel[tuple([p2,p1])][0]!="unrelated": 
        print "ALREADY EXISTS!:"+str(truth_rel[tuple([p2,p1])])  
        return tree,0 
    #check if it's a cousin 
    combo_nums=[float(i) for i in combo_dict[tuple([p1,p2])]] 
    combo_dict_total=sum(combo_nums)
    ma00=combo_nums[0]/combo_dict_total 
    ma01=combo_nums[1]/combo_dict_total
    ma11=combo_nums[3]/combo_dict_total 
    if (ma00 < 0.7) and (ma01>0.21) and (ma11 < 0.5): 
        #cousin! 
        print "COUSIN!!: ma00:"+str(ma00)+",ma01:"+str(ma01)+",ma11:"+str(ma11) 
        t_cousin,errors_cousin=test_cousin(tree,p2,p1,rel_dict,truth_rel,married_in) 
        return t_cousin,errors_cousin
    max_con=max([connectivity[p1],connectivity[p2]]) 
    min_con=min([connectivity[p1],connectivity[p2]])
    avunc=True
    gp=True 
    hs=True  #FOR NOW DON'T FIND HALF-SIBLINGS 
    if min_con > 0 and min_con/max_con <0.7:
        #these are not half siblings 
        hs=False 
    if min_con >0 and (min_con/max_con >0.5): 
        #these are not grandparents 
        gp=False 
    t_avunc1,errors_avunc1,exists_avunc1=test_avuncular(tree,p1,p2,rel_dict,truth_rel,married_in)
    print "errors_avunc1:"+str(errors_avunc1)+",exists:"+str(exists_avunc1)  
    if exists_avunc1: 
        return t_avunc1,errors_avunc1
    t_avunc2,errors_avunc2,exists_avunc2=test_avuncular(tree,p2,p1,rel_dict,truth_rel,married_in) 
    print "errors_avunc2:"+str(errors_avunc2)+",exists:"+str(exists_avunc2) 
    if exists_avunc2: 
        return t_avunc2,errors_avunc2 
    if gp:
        t_gp1,errors_gp1,exists_gp1=test_grandparent(tree,p1,p2,rel_dict,truth_rel,married_in)
        print "errors_gp1:"+str(errors_gp1)+",exists:"+str(exists_gp1) 
        if exists_gp1: 
            return t_gp1,errors_gp1
        t_gp2,errors_gp2,exists_gp2=test_grandparent(tree,p2,p1,rel_dict,truth_rel,married_in) 
        print "errors_gp2:"+str(errors_gp2)+",exists:"+str(exists_gp2) 
        if exists_gp2: 
            return t_gp2,errors_gp2 
    else:
        t_gp1=tree
        errors_gp1=float('Inf') 
        t_gp2=tree
        errors_gp2=float('Inf') 
    if hs: 
        t_hs1,errors_hs1,exists_hs1=test_half_sib(tree,p1,p2,rel_dict,truth_rel,married_in)     
        print "errors_hs1:"+str(errors_hs1)+",exists:"+str(exists_hs1) 
        if exists_hs1: 
            return t_hs1,errors_hs1
    else: 
        t_hs1=tree 
        errors_hs1=float('Inf') 
    errors=[errors_avunc1,errors_avunc2,errors_gp1,errors_gp2,errors_hs1]
    lowest=min(errors) 
    if errors.count(lowest) >1: 
        #tie!
        print "TIE" 
        return tree,-1 
    elif lowest==errors_avunc1: 
        print "AVUNC1" 
        return t_avunc1,errors_avunc1 
    elif lowest==errors_avunc2: 
        print "AVUNC2" 
        return t_avunc2,errors_avunc2 
    elif lowest==errors_gp1: 
        print "GP1" 
        return t_gp1,errors_gp1
    elif lowest==errors_gp2: 
        print "GP2" 
        return t_gp2,errors_gp2 
    elif lowest==errors_hs1: 
        print "HS1" 
        return t_hs1,errors_hs1
    else: 
        print "THIS IS A FAILURE CASE IN TEST_SECOND_TREE_RELS!" 
        return tree,-1 

#cousin relationship between p1 and p2 
def test_cousin(tree,p1,p2,rel_dict,truth_rel,married_in): 
    married_in=set(married_in.keys()) 
    #p1 and p2 share a grandparent 
    p1_node=tree[p1] 
    p2_node=tree[p2]
    p1_parents=p1_node.parents 
    p2_parents=p2_node.parents 
    p1_gp=set([])
    p2_gp=set([]) 
    for p1_parent in p1_parents: 
        p1_gp=p1_gp.union((tree[p1_parent].parents)) 
    for p2_parent in p2_parents: 
        p2_gp=p2_gp.union((tree[p2_parent].parents)) 
    if len(p1_gp.intersection(p2_gp))>0: 
        print "COUSIN REL EXISTS !!" 
        return tree, 0 
    if len(p1_node.parents)==0 or len(p1_node.parents-married_in)==0: 
        #create a p1_parent node 
        print "CREATING p1 parent" 
        print "p2_node_parents:"+str(p2_node.parents) 
        print "married_in:"+str(married_in) 
        
        p1_parent=Node() 
        index=1
        while "Unknown"+str(index) in tree: 
            index+=1 
        p1_parent.name="Unknown"+str(index) 
        tree[p1_parent.name]=p1_parent
        p1_node.parents.add(p1_parent.name) 
        p1_parent.children.add(p1_node.name) 
        for s in p1_node.siblings: 
            p1_parent.children.add(s) 
            tree[s].parents.add(p1_parent.name)
    if len(p2_node.parents)==0 or len(p2_node.parents-married_in)==0: 
        print "CREATING P2 parent" 
        print "p2_node_parents:"+str(p2_node.parents) 
        print "married_in:"+str(married_in) 
        p2_parent=Node() 
        index=1
        while "Unknown"+str(index) in tree: 
            index+=1 
        p2_parent.name="Unknown"+str(index) 
        tree[p2_parent.name]=p2_parent 
        p2_parent.children.add(p2_node.name)
        p2_node.parents.add(p2_parent.name) 
        for s in p2_node.siblings: 
            p2_parent.children.add(s) 
            tree[s].parents.add(p2_parent.name)

    no_grandparents_p1=[] 
    no_grandparents_p2=[] 
    for parent in p1_node.parents: 
        if len(tree[parent].parents)==0:
            if parent not in married_in: 
                no_grandparents_p1.append(parent) 
    for parent in p2_node.parents: 
        if len(tree[parent].parents)==0: 
            if parent not in married_in: 
                no_grandparents_p2.append(parent) 
    print "no_grandparents_p1:"+str(no_grandparents_p1) 
    print "no_grandparents_p2:"+str(no_grandparents_p2) 

    if len(no_grandparents_p1)>0 and len(no_grandparents_p2)>0: 
        gp_node=Node() 
        index=1
        while "Unknown"+str(index) in tree: 
            index+=1 
        gp_node.name="Unknown"+str(index) 
        tree[gp_node.name]=gp_node 
        gp_node.children.add(no_grandparents_p1[0]) 
        gp_node.children.add(no_grandparents_p2[0]) 
        tree[no_grandparents_p1[0]].parents.add(gp_node.name) 
        tree[no_grandparents_p2[0]].parents.add(gp_node.name) 
        for s in tree[no_grandparents_p1[0]].siblings: 
            gp_node.children.add(s) 
            tree[s].parents.add(gp_node.name) 
        for s in tree[no_grandparents_p2[0]].siblings: 
            gp_node.children.add(s) 
            tree[s].parents.add(gp_node.name)
        errors=get_errors(truth_rel,tree,rel_dict) 
        return tree,errors

    elif len(no_grandparents_p1)>0: 
        for parent_2 in p2_node.parents: 
            if len(tree[parent_2].parents)>0 and parent_2 not in married_in: 
                for grandparent_2 in tree[parent_2].parents: 
                    if grandparent_2.__contains__('Unknown'): 
                        #this is the one to use! 
                        for parent_1 in p1_parents: 
                            if (parent_1 not in married_in) and len(tree[parent_1].parents)==0: 
                                tree[grandparent_2].children.add(parent_1) 
                                tree[parent_1].parents.add(grandparent_2) 
                                for s in tree[parent_1].siblings: 
                                    tree[s].parents.add(grandparent_2) 
                                    tree[grandparent_2].children.add(s) 
                                errors=get_errors(truth_rel,tree,rel_dict) 
                                return tree,errors
        errors=get_errors(truth_rel,tree,rel_dict) 
        return tree,errors
    elif len(no_grandparents_p2)>0: 
        for parent_1 in p1_node.parents: 
            if len(tree[parent_1].parents)>0 and parent_1 not in married_in: 
                for grandparent_1 in tree[parent_1].parents: 
                    print "GOT TO HERE, grandparent_1:"+str(grandparent_1) 
                    if grandparent_1.__contains__('Unknown'): 
                        #this is the one to use! 
                        print "GOT TO HERE!" 
                        for parent_2  in p2_parents: 
                            if(parent_2 not in married_in) and len(tree[parent_2].parents)==0: 
                                tree[grandparent_1].children.add(parent_2) 
                                tree[parent_2].parents.add(grandparent_1) 
                                for s in tree[parent_2].siblings: 
                                    tree[s].parents.add(grandparent_1) 
                                    tree[grandparent_1].children.add(s) 
                                errors=get_errors(truth_rel,tree,rel_dict) 
                                return tree,errors 
        errors=get_errors(truth_rel,tree,rel_dict) 
        return tree,errors
    else: 
        #both have grandparents, need to merge an unknown node 
        print "BOTH COUSIN NODES HAVE GRANDPARENTS!!" 
        errors=get_errors(truth_rel,tree,rel_dict) 
        return tree,errors 
                
 
        
        
    
#p1 is the uncle/aunt of p2 
def test_avuncular(tree,p1,p2,rel_dict,truth_rel,married_in): 
    exists=False 
    print "entering test_avuncular" 
    tree_test=copy.deepcopy(tree)
    p1_node=tree_test[p1] 
    p2_node=tree_test[p2] 
    p1_parents=p1_node.parents 
    p2_parents=p2_node.parents
    p2_grandparents=set([]) 
    if len(p2_parents)>0: 
        for p2_parent in p2_parents: 
            p2_grandparents=p2_grandparents.union(tree_test[p2_parent].parents) 
    common_grandparents=p1_parents.intersection(p2_grandparents) 
    if len(common_grandparents)> 0: 
        #relationships exists! 
        exists=True 
        return tree,0,exists 
    #add the minimum number of nodes needed to make the avuncular relationship work 
    
    #p1 parent candidates:
    p1_parent=None 
    p1_parent_candidates=[] 
    for p1_parent in p1_parents: 
        if p1_parent not in married_in: 
            if p1_parent.__contains__('Unknown'): 
                break
            p1_parent_candidates.append(p1_parent) 
    if p1_parent==None and len(p1_parent_candidates)>0: 
        p1_parent=p1_parent_candidates[0] 
    if p1_parent!=None: 
        p1_parent=tree_test[p1_parent] 

    #p2 parent candidates: 
    p2_parent=None 
    p2_parent_candidates=[] 
    for p2_parent in p2_parents: 
        if p2_parent not in married_in: 
            if p2_parent.__contains__('Unknown'): 
                break 
            p2_parent_candidates.append(p2_parent) 

    if p2_parent==None and len(p2_parent_candidates)>0: 
        p2_parent=p2_parent_candidates[0] 
    if p2_parent!=None: 
        p2_parent=tree_test[p2_parent] 

    if p1_parent==None: 
        #make a new Node
        p1_parent=Node() 
        index=1
        while "Unknown"+str(index) in tree_test: 
            index+=1 
        p1_parent.name="Unknown"+str(index) 
        tree_test[p1_parent.name]=p1_parent 
        p1_parent.children.add(p1_node.name) 
        for s in p1_node.siblings: 
            p1_parent.children.add(s) 
            tree_test[s].parents.add(p1_parent.name) 
    if p2_parent==None: 
        p2_parent=Node()
        index=1 
        while "Unknown"+str(index) in tree_test: 
            index+=1
        p2_parent.name="Unknown"+str(index) 
        tree_test[p2_parent.name]=p2_parent 
        p2_parent.children.add(p2_node.name) 
        p2_node.parents.add(p2_parent.name) 
        for s in p2_node.siblings: 
            tree_test[s].parents.add(p2_parent.name) 
            p2_parent.children.add(s) 
    p1_parent.children.add(p2_parent.name) 
    p2_parent.parents.add(p1_parent.name) 
    for s in p2_parent.siblings: 
        p1_parent.children.add(s) 
        tree_test[s].parents.add(p1_parent.name) 
    errors=get_errors(truth_rel,tree_test,rel_dict) 
    return tree_test,errors,exists  

#p1 is the grandparent of p2 
def test_grandparent(tree,p1,p2,rel_dict,truth_rel,married_in): 
    exists=False 
    print "entering test_grandparents" 
    tree_test=copy.deepcopy(tree)
    p1_node=tree_test[p1] 
    p2_node=tree_test[p2] 
    p1_children=p1_node.children
    p2_parents=p2_node.parents
    if len(p1_children.intersection(p2_parents)) > 0: 
        #relationship exists!
        exists=True 
        return tree, 0,exists
    #add the minimum number of nodes needed to make grandparent relationship work 
    p1_child_node=None 
    for p1_child in p1_children: 
        if p1_child.__contains__('Unknown'): 
            p1_child_node=tree_test[p1_child] 
            break 
    p2_parent_node=None 
    for p2_parent in p2_parents: 
        if p2_parent.__contains__('Unknown'): 
            p2_parent_node=tree_test[p2_parent] 
            break 
    if p1_child_node !=None and p2_parent_node!=None: 
        #merge 
        p2_parent_node.parents=p1_child_node.parents.union(p2_parent_node.parents) 
        p2_parent_node.children=p1_child_node.children.union(p2_parent_node.children) 
        for p_name in p1_child_node.parents: 
            tree_test[p_name].children.remove(p1_child_node.name) 
            tree_test[p_name].children.add(p2_parent_node.name) 
        for c_name in p1_child_node.children: 
            tree_test[c_name].parents.remove(p1_child_node.name) 
            tree_test[c_name].parents.add(p2_parent_node.name) 
        tree_test.__delitem__(p1_child_node.name) 
    elif p1_child_node!=None: 
        p1_child_node.children.add(p2_node)
        p2_node.parents.add(p1_child_node.name) 
        for s in p2_node.siblings: 
            p1_child_node.children.add(s) 
            tree_test[s].parents.add(p1_child_node.name) 
    elif p2_parent_node!=None: 
        p2_parent_node.parents.add(p1_node.name) 
        p1_node.children.add(p2_parent_node.name) 
        for s in p2_parent_node.siblings: 
            p1_node.children.add(s) 
            tree_test[s].parents.add(p1_node.name) 
    else: 
        p2_parent=Node() 
        index=1 
        while "Unknown"+str(index) in tree_test: 
            index+=1 
        p2_parent.name="Unknown"+str(index) 
        tree_test[p2_parent.name]=p2_parent 
        p2_parent.children.add(p2_node.name)
        p2_node.parents.add(p2_parent.name) 
        for s in p2_node.siblings: 
            p2_parent.children.add(s) 
            tree_test[s].parents.add(p2_parent.name)     
        p2_parent.parents.add(p1) 
        p1_node.children.add(p2_parent.name) 
    
    errors=get_errors(truth_rel,tree_test,rel_dict) 
    return tree_test,errors,exists 

#p1 and p2 are half-siblings 
def test_half_sib(tree,p1,p2,rel_dict,truth_rel,married_in): 
    exists=False
    print "entering test_half_sib" 
    tree_test=copy.deepcopy(tree)
    p1_node=tree_test[p1] 
    p2_node=tree_test[p2] 
    if len(p1_node.parents.intersection(p2_node.parents)) > 0: 
        #relationship already exists!
        exists=True 
        return tree,0,exists  
    #add the minimum number of nodes needed to make the half-sib relationship work 
    p1_parent=None 
    p1_parent_candidates=[] 
    for p1_parent in p1_node.parents: 
        if p1_parent not in married_in: 
            if p1_parent.__contains__('Unknown'): 
                break
            p1_parent_candidates.append(p1_parent) 
    if p1_parent==None and len(p1_parent_candidates)>0: 
        p1_parent=p1_parent_candidates[0] 
    if p1_parent!=None: 
        p1_parent=tree_test[p1_parent] 

    #p2 parent candidates: 
    p2_parent=None 
    p2_parent_candidates=[] 
    for p2_parent in p2_node.parents: 
        if p2_parent not in married_in: 
            if p2_parent.__contains__('Unknown'): 
                break 
            p2_parent_candidates.append(p2_parent) 

    if p2_parent==None and len(p2_parent_candidates)>0: 
        p2_parent=p2_parent_candidates[0] 
    if p2_parent!=None: 
        p2_parent=tree_test[p2_parent] 
    if p1_parent==None and p2_parent==None: 
        both_parent=Node() 
        index=1 
        while "Unknown"+str(index) in tree_test: 
            index+=1 
        both_parent.name="Unknown"+str(index) 
        tree_test[both_parent.name]=both_parent 
    elif p1_parent!=None: 
        both_parent=p1_parent 
    else: 
        both_parent=p2_parent 
    both_parent.children.add(p2_node.name)
    both_parent.children.add(p1_node.name) 
    for s in p2_node.siblings: 
        tree_test[s].parents.add(both_parent.name) 
        both_parent.children.add(s) 
    
    for s in p1_node.siblings: 
        tree_test[s].parents.add(both_parent.name) 
        both_parent.children.add(s) 
    p2_node.parents.add(both_parent.name) 
    p1_node.parents.add(both_parent.name)
    errors=get_errors(truth_rel,tree_test,rel_dict) 
    return tree_test,errors,exists 
