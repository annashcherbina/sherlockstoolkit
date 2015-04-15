from Node import * 
from Params import * 

def buildPedigree(inputfname): 
    pedigree=open(inputfname,'r').read().replace('\r\n','\n').split('\n') 
    pedigree_output=dict() 


    if '' in pedigree: 
        pedigree.remove('') 
    tree=dict() 
    for line in pedigree: 
        line=line.split(',') 
        parent=line[0]
        gender=line[1] 
        #print "person:"+str(parent) +","+str(gender) 

        if len(line)<3: 
            children=[] 
        else:
            children=line[2::]

        #does a node exist for the parent? 
        if parent not in tree: 
            parentNode=Node()
            parentNode.name=parent 
            tree[parent]=parentNode
        tree[parent].gender=gender
        #print tree[parent].toString() 
        for child in children: 
            if child not in tree: 
                childNode=Node() 
                childNode.name=child 
                tree[child]=childNode

        for child in children: 
            tree[child].parents.append(tree[parent]) 
            tree[parent].children.append(tree[child]) 
    for name in tree: 
        if len(tree[name].parents)==0: 
            tree_case=tree[name].printTree(1) 
            print tree_case 

    #get the relationships of each person to all other people 



    for person in tree:
        down=0 
        up=0
        #print person
        #keep track of all relatives we have already accounted for, so no person is recorded > 1 times 
        examined=[person] 

        #1. Get all the direct descendents.
        descendents=tree[person].children

        while len(descendents) >0:
            down+=1
            for descendant in descendents:
                relationship=steps_to_relationship[tuple([up,down])][tree[descendant.name].gender]
                degree_r=str(degree[relationship][0])
                percentdna=str(degree[relationship][1]) 
                pedigree_output[tuple([descendant.name,person])]=[relationship,degree_r,float(percentdna)]
                examined.append(descendant.name) 
            newDescendents=[] 
            for descendent in descendents: 
                newDescendents+=descendent.children 
            descendents=newDescendents
        #print "got descendents"
        #2. Get all ancestors. Store them in a list because we will later examine their descendents. 
        all_ancestors=[] 
        up=0
        down=0 
        ancestors=tree[person].parents
        while len(ancestors)>0: 
            #print "ancestors:"
            up+=1
            for ancestor in ancestors:
                #print str(ancestor.name) 
                relationship=steps_to_relationship[tuple([up,down])][tree[ancestor.name].gender]
                all_ancestors.append([ancestor,up]) 
                degree_r=str(degree[relationship][0])
                percentdna=str(degree[relationship][1]) 
                pedigree_output[tuple([ancestor.name,person])]=[relationship,degree_r,float(percentdna)]

                examined.append(ancestor.name) 
            newAncestors=[] 
            for ancestor in ancestors: 
                newAncestors+=ancestor.parents 
            ancestors=newAncestors 

        #print "got ancestors" 
        #3. Go through the descendants of all other ancestors 
        #print str(all_ancestors) 
        for ancestor_entry in all_ancestors: 
            ancestor=ancestor_entry[0]
            #print ancestor.toString() 
            up=ancestor_entry[1] 
            down=0 
            candidates=ancestor.children
            #print "candidates:" 
            #for candidate in candidates: 
                #print "------"
                #print candidate.toString()
                #print "------"
            while len(candidates) >0: 
                down+=1
                for candidate in candidates: 
                    if candidate.name not in examined:
                       # print "candidate name:"+str(candidate.name) 
                       # print "up:"+str(up) 
                       # print "down:"+str(down) 
                       # print "gender:"+str(tree[candidate.name].gender)
                        relationship=steps_to_relationship[tuple([up,down])][tree[candidate.name].gender]
                        if relationship in ['sibling','sister','brother']: 
                            candidateparents=set(candidate.parents)
                            personparents=set(tree[person].parents)
                            commonparents=personparents.intersection(candidateparents) 
                            if len(commonparents)<2: 
                                relationship="half "+relationship
                        degree_r=str(degree[relationship][0])
                        percentdna=str(degree[relationship][1]) 
                        pedigree_output[tuple([candidate.name,person])]=[relationship,degree_r,float(percentdna)]
                        examined.append(candidate.name) 
                newCandidates=[] 
                for candidate in candidates: 
                    newCandidates+=candidate.children
                candidates=newCandidates 
        #print "got other" 
    return pedigree_output
