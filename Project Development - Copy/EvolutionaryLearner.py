import os
import sys
import PredicateSet as PredicateSet
import CoopPredicateSet as CoopPredicateSet
import numpy.random as npr
import random

from Rule import Rule
from Individual import Individual
from random import randrange
from random import randint

    #  EVOLUTIONARY LEARNER ALGORITHM
# class EvolutionaryLearner:

    # Best runtime in seconds by the SUMO traffic light algorithm
global bestSUMORuntime
bestSUMORuntime = 1999
    # How many of the top individuals to breed for new generation
global maxMutations
global percentOfLastGenerationBred
maxMutations = 7
percentOfLastGenerationBred = .5

    # Specifications for making Individuals and Rules
global maxRulePredicates
global maxRules
global maxIndividuals
global newGenerationPoolSize

maxRulePredicates = 5
maxRules = 10
maxIndividuals = 30
maxRulesInNewGenerationSet = 25

    # How much runtime and rule weights matter when determining fitness of a simulation run
global runtimeFactor        
global ruleWeightFactor

runtimeFactor = 1
ruleWeightFactor = 1
    
    # FITNESS FUNCTION FOR AN INDIVIDUAL AFTER ONE SIMULATION RUN/EPISODE
def rFit(individual, simTime, aggregateVehicleWaitTime):    
        # If Individual's simulation time is less than the best time, its fitness is the difference between those two values
    if simTime < bestSUMORuntime:
        return simTime - bestSUMORuntime
    else:
        bestIndivAggregateVehWaitTime = individual.getAgentPool().getBestIndividualAggregateVehWaitTime()
        indivAggrVehWaitTime = individual.getAggregateVehicleWaitTime()

            # If Individual's simulation time is more than the best time, multiply it relative to how much worse it is
        if indivAggrVehWaitTime < (bestIndivAggregateVehWaitTime * 1.1):
            return indivAggrVehWaitTime*10

        elif indivAggrVehWaitTime < (bestIndivAggregateVehWaitTime * 1.2):
            return indivAggrVehWaitTime*20
        
        elif indivAggrVehWaitTime < (bestIndivAggregateVehWaitTime * 1.3):
            return indivAggrVehWaitTime*30
        
        else: 
            return indivAggrVehWaitTime*40

    # FITNESS FUNCTION FOR ONE GENERATION
def fit(simTime, agentPools):
    ruleWeights = getSumRuleWeights(agentPools)
    fit = runtimeFactor*(1/simTime) + ruleWeightFactor*(1-(1/ruleWeights))

    return fit

    # CREATES NEW GENERATION AFTER A SIMULATION RUN AND UPDATES AGENT POOLS' INDIVIDUAL SET WITH NEW GEN
def createNewGeneration(agentPools):
    print("Creating a new Generation.")
    for ap in agentPools:
        individuals = ap.getIndividualsSet()
        individuals.sort(key=lambda x: x.getNormalizedFitness(), reverse = True)
        #individuals.len() # An error trip for the program to stop for testing

        lastIndex = int(len(individuals)*percentOfLastGenerationBred)
        newGeneration = individuals[0:lastIndex]

            # Create new generation
        while len(newGeneration) < maxIndividuals:
            print("New generation has length", len(newGeneration), ". Creating a new individual.")
            parent1 = chooseFirstParent(newGeneration)
            parent2 = chooseSecondParent(newGeneration, parent1)
            print("Generation includes", newGeneration)
            newGeneration.append(crossover(parent1, parent2))
            print("Added a child. Length is now", len(newGeneration))
            print("Generation includes", newGeneration)

            # Randomly mutate a random number of the children
        for i in range(randint(1, maxMutations)):
            print("Randomly mutating children!")
            individualToMutate = newGeneration[randrange(0, len(newGeneration))]
            newGeneration.append(mutate(individualToMutate))
            newGeneration.remove(individualToMutate)

            # Lines 100 - 130 are file writing lines just for mid-simulation validation
        f = open("newGeneration", "w")
        f.write("New Generation includes these individuals and their rules.\n\n\n")

        individualCount = 1
        for i in newGeneration:           
            ruleCount = 1
            f.write("Individual" + str(individualCount) + "has a fitness of " + str(i.getFitness()) + " and a last runtime of " + str(i.getLastRunTime()) + " and contains the following rules:\n\n") 
            f.write("Rules in RS:\n")
            for rule in i.getRS():
                cond = ""
                for c in rule.getConditions():
                    cond += "," + c + " "
            
                f.write("\nRule" + str(ruleCount) + ": (" + str(rule) + ") <" + cond + ">, <" + str(rule.getAction()) + "> and rule has a weight of" + str(rule.getWeight()) + "\n\n")
                ruleCount += 1

            ruleCount = 1
            f.write("Rules in RSint:\n")
            for rule in i.getRSint():
                cond = ""
                for c in rule.getConditions():
                    cond += "," + c + " "
            
                f.write("\nRule" + str(ruleCount) + ": <" + cond + ">, <" + str(rule.getAction()) + "> and rule has a weight of" + str(rule.getWeight()) + "\n\n")
                ruleCount += 1

            f.write("-------------------\n\n")
            individualCount += 1    

        f.write("\n*************END GENERATION*************\n\n\n")
        ap.updateIndividualsSet(newGeneration)

    # CREATE INDIVIDUALS WITH RANDOM RULES POPULATING THEIR RULE SETS BEFORE FIRST RUN
def initIndividuals(agentPool):
    individuals = []
    for x in range(maxIndividuals):    
        RS = []     # RS is a rule set with no shout-ahead predicates
        RSint = []  # RSint is a rule set with shout-ahead predicates
            # Populate a rule set
        for i in range(maxRules):
            RS.append(createRandomRule(agentPool, 0))
            RSint.append(createRandomRule(agentPool, 1))
        
        individuals.append(Individual(x+1, agentPool, RS, RSint))
    
    return individuals
    
    # CREATE A RANDOM RULE USING RANDOM PREDICATES AND AN AGENT POOL RELATED ACTION
def createRandomRule(agentPool, ruleType):
    conditions = [] # Conditions for a rule
        
        # RS rule
    if ruleType == 0:
            # Set conditions of rules as a random amount of random predicates
        for i in range(randint(1, maxRulePredicates)):
            newCond = PredicateSet.getRandomPredicate()
            if checkValidCond(newCond, conditions):
                conditions.append(newCond)
        
        # RSint rule
    elif ruleType == 1:
            # Set conditions of rules as a random amount of random predicates
        for i in range(randint(1, maxRulePredicates)):
            newCond = agentPool.getRandomRSintPredicate()
            if checkValidCond(newCond, conditions):
                conditions.append(newCond)

        # Get index of possible action. SUMO changes phases on indexes
    action = randrange(0, len(agentPool.getActionSet()))     # Set rule action to a random action from ActionSet pertaining to Agent Pool being serviced
    #print("The action set is:", agentPool.getActionSet())
    rule = Rule(ruleType, conditions, action, agentPool)

    return rule   
    
    # CREATE A CHILD RULE BY BREEDING TWO PARENT RULES
def crossover(indiv1, indiv2):
    print("NEW CROSSOVER\n\n\n\n\n")
    identifier = str(indiv1.getID()) + "." + str(indiv2.getID())
    identifier = identifier[-4:] # Memory saving line
    agentPool = indiv1.getAgentPool()

    superRS = indiv1.getRS() + indiv2.getRS()    
    superRS = removeDuplicateRules(superRS)    # Remove duplicate rules from set
    
    while len(superRS) < maxRulesInNewGenerationSet:
        print("Adding a new random rule to superRS. The length of superRS is", len(superRS), "and the max length is")
        superRS.append(createRandomRule(agentPool, 0))

    print("About to sort superRS in crossover")
    superRS.sort(key=lambda x: x.getWeight(), reverse = True)
    print("Sorted superRS in crossover")
    
    superRSint = indiv1.getRSint() + indiv2.getRSint()    
    superRSint = removeDuplicateRules(superRSint)

    while len(superRSint) < maxRulesInNewGenerationSet:
        print("Adding a new random rule to superRS")
        superRSint.append(createRandomRule(agentPool, 1))

    print("About to sort superRSint in crossover")
    superRS.sort(key=lambda x: x.getWeight(), reverse = True)
    print("Sorted superRSint in crossover")

    newRS = superRS[0:maxRules] 
    newRSint = superRSint[0:maxRules]
    
    counter = 1
    for rule in newRS:
        print("Rule", counter, "contains conditions", rule.getConditions(), "and action", rule.getAction(), "\n\n")
        counter += 1
        
        # Ensure duplicate rules (with or without different weights) haven't been added to rule set. If they have, keep the one with the higher weight and mutate the other
    for rule in newRS:
        for r in newRS:
            if rule is not r:
                while set(rule.getConditions()) == set(r.getConditions()) and rule.getAction() == r.getAction():
                    print('Two rules are equal and are being mutated.')
                    if rule.getWeight() < r.getWeight():
                        # print("rule has less weight than r")
                        newRS.append(mutateRule(rule))
                        newRS.remove(rule)
                    else:
                        newRule = mutateRule(r)
                        newRS.append(mutateRule(r))
                        newRS.remove(r)

        # Ensure the same rule with different weights haven't been added to rule set. If they have, keep the one with the higher weight and mutate the other
    for rule in newRSint:
        for r in newRSint:
            if rule is not r:
                while set(rule.getConditions()) == set(r.getConditions()) and rule.getAction() == r.getAction():
                    print('Two rules are equal and are being mutated.')
                    if rule.getWeight() < r.getWeight():
                        # print("rule has less weight than r")
                        newRS.append(mutateRule(rule))
                        newRS.remove(rule)
                    else:
                        newRule = mutateRule(r)
                        newRS.append(mutateRule(r))
                        newRS.remove(r)

        # Both while loops below ensure the rule sets are not identical
    while ruleSetsAreDuplicate(newRS, indiv1.getRS()) or ruleSetsAreDuplicate(newRS, indiv2.getRS()):
        # print("Indiv 1 compare is", ruleSetsAreDuplicate(newRS, indiv1.getRS()))
        # print('Indiv 2 compare is', ruleSetsAreDuplicate(newRS, indiv2.getRS()))
        print("Rule set RS is the same as parent's RS")
        newRS.sort(key=lambda x: x.getWeight(), reverse = True)
        ruleToMutate = newRS[len(newRS)-1]
        print("Last rule in RS acquired.")
        newRS.append(mutateRule(ruleToMutate))
        newRS.remove(newRS[len(newRS)-2])
    
    while ruleSetsAreDuplicate(newRSint, indiv1.getRSint()) or ruleSetsAreDuplicate(newRSint, indiv2.getRSint()):
        print("Indiv 1 compare is", ruleSetsAreDuplicate(newRSint, indiv1.getRSint()))
        print('Indiv 2 compare is', ruleSetsAreDuplicate(newRSint, indiv2.getRSint()))
        print("Rule set RSint is the same as parent's RSint")
        newRSint.sort(key=lambda x: x.getWeight(), reverse = True)
        ruleToMutate = newRS[len(newRSint)-1]
        print("Last rule in RS acquired.")
        newRSint.append(mutateRule(ruleToMutate))
        newRSint.remove(newRSint[len(newRSint)-2])
    
    newIndividual = Individual(identifier, agentPool, newRS, newRSint)
    
    print("\n\n\n***NEW INDIVIDUAL SUCCESSFULLY CREATED***\n\n")
    # counter = 1
    # for rule in newIndividual.getRS():
    #     for r in newIndividual.getRS():
    #         print("Rule", counter, "is", rule, "and contains conditions", rule.getConditions(), "and action", rule.getAction(),"while r is", r, "and contains conditions", r.getConditions(), "and action", r.getAction())
    #         if rule is not r:
    #             print("The two rules are different.\nEqual conditions?", set(rule.getConditions()) == set(r.getConditions()), "\nEqual actions?", rule.getAction() == r.getAction(), "\n\n")
    #         counter += 1
    
    return newIndividual

def mutate(individual):
    chosenRule = individual.getRS()[randrange(0,len(individual.getRS()))]
    newRule = mutateRule(chosenRule)

    individual.getRS().append(newRule)
    individual.getRS().remove(chosenRule)
    
    return individual    
    
    # MUTATES A RULE A RANDOM NUMBER OF TIMES (MAX MUTATIONS IS USER-DEFINED)
def mutateRule(rule):
    maxNumOfMutations = 1 # user defined maximum number of mutations
    ruleCond = rule.getConditions()
    #print("*Rule to be mutated has conditions:", rule.getConditions())                
    #print('Mutating...')
        # Remove a random number of conditions and add a random number of random conditions
    for x in range(randint(1, maxNumOfMutations)):
        print("INSIDE THE MUTATE LOOP")
        
        if len(ruleCond) == 1:
            numCondToRemove = 1
        else:
            numCondToRemove = randrange(1, len(ruleCond))

        for i in range(numCondToRemove):
            # print("Rule is of type", rule.getType(), "conds were", ruleCond)
            ruleCond.remove(ruleCond[randrange(len(ruleCond))])
            # print("Rule conds are NOW:", ruleCond)
            # #print("*Rule to be mutated has conditions:", rule.getConditions())                

        numCondToAdd = randint(1, maxRulePredicates - len(ruleCond))
        #print("Num conds to add are", numCondToAdd)           
            # If rule is from RS
        if rule.getType() == 0:
            #print("Adding conds to type 0")
            for i in range(numCondToAdd):
                newPredicate = PredicateSet.getRandomPredicate()  
                #print("New predicate being added is:", newPredicate)
                    # If new random predicate is valid, append it to the conditions list
                if checkValidCond(newPredicate, ruleCond):
                    #print("New condition is valid and is being added! Old predicate set is:", ruleCond)
                    ruleCond.append(newPredicate)
                    #print("New predicate set is:", ruleCond)

            # If rule is from RSint
        elif rule.getType() == 1:
            print("RSint rule type being modified")
            for i in range(numCondToAdd):
                newPredicate = CoopPredicateSet.getRandomPredicate(rule.getAgentPool())  
                print("New predicate is", newPredicate)
                    # If new random predicate is valid, append it to the conditions list
                if checkValidCond(newPredicate, ruleCond):
                    print("Condition valid. Adding condition.")
                    ruleCond.append(newPredicate)
    
    print("*The rule is now being updated. It previously had conditions:", rule.getConditions())                
    rule.setConditions(ruleCond) # set rule's new conditions
    print("UPDATED RULE now has conditions:", rule.getConditions(), "\n\n")                
    rule.setAction(rule.getAgentPool().getActionSet()[randrange(0, len(rule.getAgentPool().getActionSet()))])
    rule.setWeight(0)

    return rule

    # RETURNS A PARENT TO BE BREED BASED ON FITNESS PROPOTIONAL SELECTION
def chooseFirstParent(breedingPopulation):
    print("Choosing parent from population", breedingPopulation)
    totalFitness = sum([i.getNormalizedFitness() for i in breedingPopulation]) # Adjust fitnesses to benefit the smallest
    if totalFitness != 0:
        selection_probs = [i.getNormalizedFitness()/totalFitness for i in breedingPopulation]
        print("Max fitness is not 0. Choosing individual via roulette wheel.")
        print("The selection probabilities are", selection_probs)
        return breedingPopulation[npr.choice(len(breedingPopulation), p=selection_probs)]
    else:
        print("Max fitness is 0. Choosing random individual.")
        return random.choice(breedingPopulation)

    # RETURNS A PARENT TO BE BREED BASED ON FITNESS PROPOTIONAL SELECTION
def chooseSecondParent(breedingPopulation, parent1):
    print('Breeding population is', breedingPopulation)
    adjustedPopulation = breedingPopulation.copy()
    adjustedPopulation.remove(parent1)
    totalFitness = sum([i.getNormalizedFitness() for i in adjustedPopulation])
    if totalFitness != 0:
        selection_probs = [i.getNormalizedFitness()/totalFitness for i in adjustedPopulation]
        print("Max fitness is not 0. Choosing individual via roulette wheel.")
        print("The selection probabilities are", selection_probs)
        return adjustedPopulation[npr.choice(len(adjustedPopulation), p=selection_probs)]
    else:
        print("Max fitness is 0. Choosing random individual.")
        return random.choice(breedingPopulation)


    # ENSURE UNIQUE PREDICATE TYPES IN CONDITIONS 
def checkValidCond(cond, conditions):        
    predicateType = cond.split("_")
        
        #If predicate type already exists in conditions, return false
    if predicateType[0] in conditions:
        return False 
    else:
        return True

def removeDuplicateRules(ruleSet):
    for rule in ruleSet:
        for otherRule in ruleSet:
            if rulesAreDuplicate(rule, otherRule):    
                ruleSet.remove(otherRule)
                print("Removed duplicate rule!")
    return ruleSet

    # CHECK IF TWO RULES ARE DUPLICATES OF EACH OTHER
def rulesAreDuplicate(rule1, rule2):
    conds1 = rule1.getConditions()
    conds2 = rule2.getConditions()

    act1 = rule1.getAction()
    act2 = rule2.getAction()

    if rule1 is rule2 or (set(conds1) == set(conds2) and act1 == act2):
        return True
    else:
        return False
    
    # CHECK IF TWO RULE SETS ARE DUPLICATES OF EACH OTHER
def ruleSetsAreDuplicate(rs1, rs2):
    print("Ruleset 1 is", rs1)
    print("Ruleset 2 is", rs2)
    print("\n\nDifference between rs1 and rs2 is", set(rs1) - set(rs2))
    for rule in rs1:
        for r in rs2:
            if set(rs1) == set(rs2):
                print("RS1 rule has conds", rule.getConditions(), "and RS2 rule is", r.getConditions(), "and the condition equality is", rule.getConditions() == r.getConditions(), "\n")
                print("Difference between rs2 and rs1 is", set(rs1) - set(rs2))
    return set(rs1) == set(rs2)  

    # RETURN SUM OF ALL WEIGHTS IN A RULE SET
def getSumRuleWeights(agentPools):
    weightSum = 0

    for ap in agentPools:
        individuals = ap.getIndividualsSet()    
        # For each individual, sum all their rule weights
        for i in individuals:
            ruleSet = i.getRS()    
            weightSum += sum(rule.getWeight() for rule in ruleSet)
    
    if weightSum == 0:
        weightSum = 2.2250738585072014e-308

    return weightSum

