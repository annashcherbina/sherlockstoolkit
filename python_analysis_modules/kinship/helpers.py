from Node import * 

from math import pow
def maf_freq(q,k,parent):
    if k=='unrelated':
        return q

    elif parent==0:
        return (-1.0*q)/pow(2,k)+q
    elif parent==1:
        return (.5-q)/pow(2,k)+q
    else:
        return (1.0-q)/pow(2,k)+q

def get_genotype(q,k,parent):
    genotype=dict()
    if k=='unrelated':
        genotype[0]=(1.0-q)*(1.0-q)
        genotype[1]=2.0*q*(1.0-q)
        genotype[2]=pow(q,2.0)
    elif parent==0:
        genotype[0]=pow(q,2)*(1.0-2.0*pow(.5,k))+q*(2.0*pow(.5,k)-2)+1
        genotype[1]=pow(q,2)*(4.0*pow(0.5,k)-2)+q*(2.0-2*pow(.5,k))
        genotype[2]=pow(q,2)*(1.0-2.0/pow(2,k))
    elif parent==1:
        genotype[0]=pow(q,2)*(1.0-2*pow(.5,k))+q*(3.0*pow(.5,k)-2)+(1.0-pow(.5,k))
        genotype[1]=pow(q,2)*(4.0*pow(.5,k)-2)+q*(2.0-4*pow(0.5,k))+pow(.5,k)
        genotype[2]=pow(q,2)*(1-2.0*pow(0.5,k))+q*pow(0.5,k)
    elif parent==2:
        genotype[0]=pow(q,2)*(1.0-2*pow(0.5,k))+q*(4*pow(0.5,k)-2)+(1.0-2*pow(.5,k))
        genotype[1]=pow(q,2)*(4.0*pow(0.5,k)-2)+q*(2.0-6*pow(0.5,k))+2*pow(.5,k)
        genotype[2]=pow(q,2)*(1.0-2*pow(0.5,k))+q*(2.0*pow(0.5,k))
    return genotype





def getParent(nodes,phid,visited): 
    parentnodes=[] 
    newNodes=[] 
    for node in nodes: 
        parentnodes+=node.parents
        visited+=node.parents 
    if len(parentnodes)==0:
        print "len of parentnodes is 0, making a new node"
        #create a new node if there aren't any so we have a path forward in the pedigree  
        parentNode=Node()
        parentNode.name=str(phid)+"-ph" 
        phid+=1
        parentNode.children.append(nodes[0]) 
        nodes[0].parents.append(parentNode) 
        parentnodes.append(parentNode) 
        newNodes.append(parentNode) 
        visited.append(parentNode) 
    print "parentNodes:"+str([i.toString() for i in parentnodes])
    print "newNodes:"+str([i.toString() for i in newNodes]) 
    print "phid:"+str(phid) 
    return parentnodes,newNodes,phid,visited

def getChild(nodes,phid,visited): 
    childnodes=[] 
    newNodes=[] 
    for node in nodes: 
        for child in node.children: 
            if child not in visited: 
                childnodes.append(child) 
    if len(childnodes)==0: 
        #create a new node if there aren't any so we have a path forward in the pedigree 
        childNode=Node()
        childNode.name=str(phid) +"-ph"
        phid+=1
        nodes[0].children.append(childNode) 
        childNode.parents.append(nodes[0]) 
        childnodes.append(childNode) 
        newNodes.append(childNode) 
        visited.append(childNode) 
    return childnodes,newNodes,phid,visited

def validateNodes(person1_nodes,person2_nodes,up,down): 
    candidatenodes=person2_nodes 
    parents=[]
    for step in range(up): 
        for node in candidatenodes: 
            parents+=node.parents 
        candidatenodes=parents
        parents=[]
    children=[] 
    for step in range(down): 
        for node in candidatenodes: 
            children+=node.children 
        candidatenodes=children 
        children=[] 
    person1_found=False 
    for node in candidatenodes: 
        if node in person1_nodes: 
            person1_found=True 
            break 
    if person1_found==False:
        return False 
