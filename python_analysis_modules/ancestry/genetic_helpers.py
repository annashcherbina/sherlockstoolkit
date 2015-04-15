#helper functions for running genetic algorithm 
from Population import *; 
from math import ceil; 
from random import random; 
from itertools import chain; 
import Params; 

#returns dictionary: fitness -> list of populations with that fitness 
def findMostFitPopulations(population_pool,percenttokeep): 
    numPops = 0; 
    for key in population_pool: 
        numPops+=len(population_pool[key]); 
    tokeep = int(ceil(numPops*float(percenttokeep))); 
    mostfit=dict(); 
    popKeys = population_pool.keys()
    popKeys.sort(reverse=True); 
    added = 0; 
    for key in popKeys: 
        if added > tokeep: 
            break; 
        else: 
            for pop in population_pool[key]: 
                if mostfit.__contains__(key): 
                    mostfit[key].append(pop); 
                else: 
                    mostfit[key]= [pop]; 
                added+=1; 
    return mostfit; 

#find the change in probability of observing the given profile for the population 
def getImprovement(topPops,nextGen):
    #print "topPops: " +str(topPops)+"\n"
    #print "nextGen: " +str(nextGen)+"\n" 
    topPopKeys = topPops.keys(); 
    topPopKeys.sort(reverse=True); 
    nextGenKeys = nextGen.keys(); 
    nextGenKeys.sort(reverse=True); 
    #print "topPopKeys: "+str(topPopKeys)+"\n" 
    #print "nextGenKeys: "+str(nextGenKeys)+"\n" 

    oldmax = topPopKeys[0];#these are log base 10 scores.  
    newmax = nextGenKeys[0]; 
    #oldmaxProb = pow(10,oldmax); 
    #newmaxProb = pow(10,newmax);
    #improvement = newmaxProb-oldmaxProb; 
    #print "improvement: " + str(improvement)+"\n"  
    improvement = newmax-oldmax; 
    print "improvement: " +str(improvement)+"\n" 
    return improvement; 


#sets crossover probabilities according to the relative fitness of the two populations. 
def find_crossover_probs(pop1,pop2): 
    #print "finding crossover probs" 
    #logdiff = -1*abs(pop1.fitness - pop2.fitness);
    logdiff=pop1.fitness - pop2.fitness 
    #print "pop1 fitness:"+str(pop1.fitness) 
    #print "pop2 fitness:"+str(pop2.fitness) 
    prob2 = float(1)/float(1+pow(10,logdiff)); 
    prob1 = 1-prob2; 
    #print "prob2:"+str(prob2) 
    #print "prob1:"+str(prob1) 
    
    return prob1,prob2; 


def mate(pop1,pop2,loci):
    #print "mating\n"
    offspring = Population(); 
    #fill in fields that identify the offspring's contributing ancestor populations. 
    offspring.contributors = [pop1,pop2]
    offspring.allancestors = pop1.allancestors + pop2.allancestors; 
    offspring.probs=dict() 
    prob1,prob2 = find_crossover_probs(pop1,pop2); 
    #print "prob1:" + str(prob1)+"\n" 
    #print "prob2: "+ str(prob2)+"\n" 
    #print "pop1 probs:"+str(len(pop1.probs)) 
    #print "pop2 probs:"+str(len(pop2.probs)) 
    for l in loci: 
        if (l not in pop1.probs.keys()) or (l not in pop2.probs.keys()): 
            continue
        randfloat = random(); 
        mutationprob=random(); 
        if randfloat < prob1:
            offspring.probs[l]=pop1.probs[l]; 
            if mutationprob < Params.mutation_rate: 
                offspring.probls[l]=1-offspring.probs[l] #mutate to the other allele 
        else: 
            offspring.probs[l]=pop2.probs[l]; 
            if mutationprob < Params.mutation_rate: 
                offspring.probs[l]=1-offspring.probls[l] 
    offspring.findFitness(); 
    #print "offspring: " +offspring.toString()+"\n" 
    #print "done mating" 
    return offspring; 


#create the next generation by mating the most fit populations with each other. 
#toppops is a dictionary of fitness->[Pops with fitness] 
def getNextGen(topPops,loci): 
    print "getting next generation\n"
    nextGen = dict(); # fitness value --> populations in the next generation 
    topPopKeys =list(topPops.keys()); 
    topPopValues=[]; 
    for k in topPopKeys:
        topPopValues.append(topPops[k]); 
    topPopValues = list(chain.from_iterable(topPopValues)); 
    for i in range(len(topPopValues)): 
        for j in range(i+1,len(topPopValues)):
            pop1= topPopValues[i];  #pop1 and pop2 are both lists of populations
            pop2 = topPopValues[j];
            #print "pop1: " + pop1.toString()+"\n" 
            #print "pop2: " + pop2.toString()+"\n" 

            offspring = mate(pop1,pop2,loci); 
            offspring_fitness= offspring.fitness; 
            #print "offspring fitness: " + str(offspring_fitness)+"\n" 
            if nextGen.__contains__(offspring_fitness): 
                nextGen[offspring_fitness].append(offspring); 
            else: 
                nextGen[offspring_fitness]=[offspring]
            #print "nextGenKeys:"+str(nextGen.keys())+"\n" 
    #print "next gen size: " + str(len(nextGen.keys()))+"\n" 
    return nextGen; 
    
#modify the population pool by adding new fitter populations and removing the least fit populations. 
def selectForFitness(population_pool,nextGen): 
    newPop = dict(); 
    
#get the size of the original population pool. This should not change across generations. 
    popsize_to_maintain = 0; 
    fitness_vals = []; 
    for fitness in population_pool: 
        popsize_to_maintain+=len(population_pool[fitness]); 
        fitness_vals.append(fitness); 
    fitness_vals = fitness_vals+ list(nextGen.keys()); 
    fitness_vals.sort(reverse=True); 
    
    added = 0; 
    for v in fitness_vals: 
        if population_pool.__contains__(v) and added < popsize_to_maintain: 
            newPop[v]=[]; 
            for pop in population_pool[v]: 
                newPop[v].append(pop); 
                added+=1;
                if added > popsize_to_maintain: 
                    break; 
        elif nextGen.__contains__(v) and added < popsize_to_maintain: 
            newPop[v]=[]; 
            for pop in nextGen[v]: 
                newPop[v].append(pop); 
                added+=1; 
                if added > popsize_to_maintain: 
                    break; 
        else: 
            break; 
    return newPop; 


#chooses the ancestry assignment that results in the highest probability of observing the given dataset allele profile. 
def assignAncestry(population_pool): 
    highest_fitness = max(list(population_pool.keys()))
    return population_pool[highest_fitness]; 


#finds the fraction taht each ancestral population contributes to a person's overall ancestry assignment     
def getAncestorWeights(pop): 
    ancestorpool = pop.allancestors; 
    ancestorweights = dict();
    ancestorweights_reversed = dict(); 
    
    total_ancestry = len(ancestorpool); 
    for ancestor in ancestorpool: 
        if ancestorweights.__contains__(ancestor): 
            ancestorweights[ancestor]+=float(1); 
        else: 
            ancestorweights[ancestor]=float(1); 
    for ancestor in ancestorweights:
        fract = ancestorweights[ancestor]/total_ancestry; 
        if ancestorweights_reversed.__contains__(fract): 
            ancestorweights_reversed[fract].append(ancestor); 
        else: 
            ancestorweights_reversed[fract]=[ancestor];
        ancestorweights[ancestor]=fract; 
    #return ancestorweights_reversed; 
    return ancestorweights; 
