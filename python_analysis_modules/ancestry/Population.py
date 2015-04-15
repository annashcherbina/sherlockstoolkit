from math import log; 

class Population: 
    def __init__(self): 
        self.contributors = []; #list of Population objects, TODO: this field may be redundant        
        self.allancestors = []; #all contributing ancestries 
        self.fitness = None; 
        self.probs = dict() ; #Dictionary: locus-> probability of genotype  
    def toString(self): 
        return "contributors: " + str(self.contributors)+\
            "\n all ancestors: " + str(self.allancestors)+\
            "\n fitness: " + str(self.fitness)+\
            "\n probs: " + str(self.probs)+"\n" 
    #if more than 1/4 of loci have p=0, the fitness of the entire population assignment gets set to 0 
    def findFitness(self): 
        logfitness = 0; 
        for p in self.probs.values():
            if p==0: 
                p=0.001
            logfitness+=log(p,10);
        self.fitness=logfitness; 

'''
    #if more than 1/4 of loci have p=0, the fitness of the entire population assignment gets set to 0 
    def findFitness(self): 
        logfitness = 0; 
        numzeros=0 
        numtotal=len(self.probs.values())
        for p in self.probs.values():
            if p==0: 
                numzeros+=1 
            else:
                logfitness+=log(p,10);
        if numzeros > (0.25*numtotal):
            self.fitness=0 
        else: 
            self.fitness=logfitness; 

'''
