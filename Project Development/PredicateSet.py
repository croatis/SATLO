import os
import sys
import optparse
import inspect
from random import randrange

# class PredicateSet:

#---------- longestTimeWaitedToProceedStaight predicate set ----------#
def longestTimeWaitedToProceedStraight_0(time):
    if time == 0:
        return True
    else:
        return False 

def longestTimeWaitedToProceedStraight_0_15(time):
    if 0 < time <= 15:
        return True
    else:
        return False

def longestTimeWaitedToProceedStraight_15_30(time):
    if 15 < time <= 30:
        return True
    else:
        return False

def longestTimeWaitedToProceedStraight_30_45(time):
    if 30 < time <= 45:
        return True
    else:
        return False

def longestTimeWaitedToProceedStraight_45_60(time):
    if 45 < time <= 60:
        return True
    else:
        return False

def longestTimeWaitedToProceedStraight_60_90(time):
    if 60 < time <= 90:
        return True
    else:
        return False

def longestTimeWaitedToProceedStraight_90_120(time):
    if 90 < time <= 120:
        return True
    else:
        return False

def longestTimeWaitedToProceedStraight_120_150(time):
    if 120 < time <= 150:
        return True
    else:
        return False

def longestTimeWaitedToProceedStraight_150_180(time):
    if 150 < time <= 180:
        return True
    else:
        return False

def longestTimeWaitedToProceedStraight_180_210(time):
    if 180 < time <= 210:
        return True
    else:
        return False

def longestTimeWaitedToProceedStraight_210_240(time):
    if 210 < time <= 240:
        return True
    else:
        return False

def longestTimeWaitedToProceedStraight_240_270(time):
    if 240 < time <= 270:
        return True
    else:
        return False

def longestTimeWaitedToProceedStraight_270_300(time):
    if 270 < time <= 300:
        return True
    else:
        return False

def longestTimeWaitedToProceedStraight_300(time):
    if time > 300:
        return True
    else:
        return False
#----------------------------- end -----------------------------#


#---------- longestTimeWaitedToTurnLeft predicate set ----------#
def longestTimeWaitedToTurnLeft_0(time):
    if time == 0:
        return True
    else:
        return False 

def longestTimeWaitedToTurnLeft_0_15(time):
    if 0 < time <= 15:
        return True
    else:
        return False

def longestTimeWaitedToTurnLeft_15_30(time):
    if 15 < time <= 30:
        return True
    else:
        return False

def longestTimeWaitedToTurnLeft_30_45(time):
    if 30 < time <= 45:
        return True
    else:
        return False

def longestTimeWaitedToTurnLeft_45_60(time):
    if 45 < time <= 60:
        return True
    else:
        return False

def longestTimeWaitedToTurnLeft_60_90(time):
    if 60 < time <= 90:
        return True
    else:
        return False

def longestTimeWaitedToTurnLeft_90_120(time):
    if 90 < time <= 120:
        return True
    else:
        return False

def longestTimeWaitedToTurnLeft_120_150(time):
    if 120 < time <= 150:
        return True
    else:
        return False

def longestTimeWaitedToTurnLeft_150_180(time):
    if 150 < time <= 180:
        return True
    else:
        return False

def longestTimeWaitedToTurnLeft_180_210(time):
    if 180 < time <= 210:
        return True
    else:
        return False

def longestTimeWaitedToTurnLeft_210_240(time):
    if 210 < time <= 240:
        return True
    else:
        return False

def longestTimeWaitedToTurnLeft_240_270(time):
    if 240 < time <= 270:
        return True
    else:
        return False

def longestTimeWaitedToTurnLeft_270_300(time):
    if 270 < time <= 300:
        return True
    else:
        return False

def longestTimeWaitedToTurnLeft_300(time):
    if time > 300:
        return True
    else:
        return False
#----------------------------- end -----------------------------#


#-------- NumCarsWaitingToProceedStraight predicate set --------#
def numCarsWaitingToProceedStraight_0(carCount):
    if carCount == 0:
        return True
    else:
        return False  

def numCarsWaitingToProceedStraight_0_5(carCount):
    if 0 < carCount <= 5:
        return True
    else:
        return False

def numCarsWaitingToProceedStraight_5_10(carCount):
    if 5 < carCount <= 10:
        return True
    else:
        return False

def numCarsWaitingToProceedStraight_10_15(carCount):
    if 10 < carCount <= 15:
        return True
    else:
        return False

def numCarsWaitingToProceedStraight_15_25(carCount):
    if 15 < carCount <= 25:
        return True
    else:
        return False

def numCarsWaitingToProceedStraight_25_35(carCount):
    if 25 < carCount <= 35:
        return True
    else:
        return False

def numCarsWaitingToProceedStraight_35_45(carCount):
    if 35 < carCount <= 45:
        return True
    else:
        return False

def numCarsWaitingToProceedStraight_45(carCount):
    if carCount > 45:
        return True
    else:
        return False

#----------------------------- end -----------------------------#


#------------ NumCarsWaitingToTurnLeft predicate set ------------#
def numCarsWaitingToTurnLeft_0(carCount):
    if carCount == 0:
        return True
    else:
        return False 

def numCarsWaitingToTurnLeft_0_3(carCount):
    if 0 < carCount <= 3:
        return True
    else:
        return False

def numCarsWaitingToTurnLeft_3_6(carCount):
    if 3 < carCount <= 6:
        return True
    else:
        return False

def numCarsWaitingToTurnLeft_6_9(carCount):
    if 6 < carCount <= 9:
        return True
    else:
        return False

def numCarsWaitingToTurnLeft_9_12(carCount):
    if 9 < carCount <= 12:
        return True
    else:
        return False

def numCarsWaitingToTurnLeft_12_15(carCount):
    if 12 < carCount <= 15:
        return True
    else:
        return False

def numCarsWaitingToTurnLeft_15(carCount):
    if carCount > 15:
        return True
    else:
        return False                                                               
#----------------------------- end -----------------------------#


#-------- TimeSpentInCurrentPhase predicate set --------#
def timeSpentInCurrentPhase_0(time):
    if carCount == 0:
        return True
    else:
        return False

def timeSpentInCurrentPhase_0_15(time):
    if 0 < time <= 15:
        return True
    else:
        return False

def timeSpentInCurrentPhase_15_30(time):
    if 15 < time <= 30:
        return True
    else:
        return False     

def timeSpentInCurrentPhase_30_45(time):
    if 30 < time <= 45:
        return True
    else:
        return False 

def timeSpentInCurrentPhase_45_60(time):
    if 45 < time <= 60:
        return True
    else:
        return False 

def timeSpentInCurrentPhase_60_90(time):
    if 60 < time <= 90:
        return True
    else:
        return False 

def timeSpentInCurrentPhase_90_120(time):
    if 90 < time <= 120:
        return True
    else:
        return False 

def timeSpentInCurrentPhase_120_150(time):
    if 120 < time <= 150:
        return True
    else:
        return False

def timeSpentInCurrentPhase_150_180(time):
    if 150 < time <= 180:
        return True
    else:
        return False     

def timeSpentInCurrentPhase_180_210(time):
    if 180 < time <= 210:
        return True
    else:
        return False 

def timeSpentInCurrentPhase_210_240(time):
    if 210 < time <= 250:
        return True
    else:
        return False 

def timeSpentInCurrentPhase_240_270(time):
    if 240 < time <= 270:
        return True
    else:
        return False 

def timeSpentInCurrentPhase_270_300(time):
    if 270 < time <= 300:
        return True
    else:
        return False 

def timeSpentInCurrentPhase_300(time):
    if time > 300:
        return True
    else:
        return False                                                   
#----------------------------- end -----------------------------#

#-------------------- Standalone predicates --------------------#
def verticalPhaseIsGreen(phase):
    print(phase)
#----------------------------- end -----------------------------#

    # RETURN LIST OF PREDICATE FUNCTIONS
def getPredicateList():
    thisModule = sys.modules[__name__] # Get reference to this module for next operation
    methodsDict = dict(inspect.getmembers(thisModule, predicate=inspect.isfunction)) # Get a dictionary with all methods (predicates) in this module
        # Remove all methods that are not predicates from dictionary 
    methodsDict.pop("getPredicateList")
    methodsDict.pop("getRandomPredicate") 
    methodsDict.pop("run")

        # Seperate methods/predicates from rest of data in dictionary into a list
    predicateList = []
    for predicate in methodsDict:
        predicateList.append(predicate)
    
    print("The list has a length of", len(predicateList), "and contains: ", predicateList)
    return predicateList

    # RETURN RANDOM PREDICATE FROM LIST OF PREDICATE FUNCTIONS
def getRandomPredicate(predicateList):
    return (predicateList[randrange(len(predicateList)-1)])


def run():
    print("\nThe random predicate chosen is:", getRandomPredicate(getPredicateList()))

if __name__ == "__main__":
    run()