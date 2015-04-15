class Node: 
    def __init__(self,label=None,parents=None,siblings=None,children=None,spouse=None,gender=None): 
        self.name=None
        self.parents=set([])
        self.siblings=set([])  
        self.children=set([]) 
        self.spouse=None 
        self.gender='u'
        self.validated=False 

    def printTree(self,level):
        outputString=str(self.name) +"-"+str(self.gender) +"\n" 
        for child in self.children: 
            outputString+="\t"*level
            outputString+=child.printTree(level+1) 
        return outputString
    '''
    def toString(self): 
        selfString=str(self.name)+'\t'+str(self.gender)+'\n'+"parents" 
        for node in self.parents: 
            selfString = selfString+'\t'+str(node.name) 
        selfString=selfString+"\nchildren:"
        for node in self.children: 
            selfString=selfString+'\t'+str(node.name)
        return selfString 
    '''
    def toString(self): 
        selfString=str(self.name)+'\t'+str(self.gender)+'\n'+"parents" 
        for node in self.parents: 
            selfString = selfString+'\t'+str(node) 
        selfString=selfString+"\nchildren:"
        for node in self.children: 
            selfString=selfString+'\t'+str(node)
        return selfString 
