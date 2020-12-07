# -*- coding: utf-8 -*-

import multiprocessing as mp
from ConstantsAndRandom import ConstantsAndRandom
from SimulationEnvironment import SimulationEnvironment
import pickle
import time as tm
import cProfile
import pstats
import sys
import time
import os

numberOfCores = 40

print("hello")

sys.setrecursionlimit(10000)

if not os.path.exists(os.path.join(os.getcwd(), "SimulationStates")):
    os.makedirs(os.path.join(os.getcwd(), "SimulationStates"))
if not os.path.exists(os.path.join(os.getcwd(), "SimulationStatesFinished")):
    os.makedirs(os.path.join(os.getcwd(), "SimulationStatesFinished"))

pathStartData = "SimulationStatesToResume/"
pathStoreData = "SimulationStates/"

fileNameList = os.listdir(pathStartData)
simulationEnvironmentList = []

i = 0

for fileName in fileNameList:
    if fileName=="_description.txt" or fileName=="other":
        continue
    se = pickle.load( open( pathStartData+fileName, "rb" ) )
    simulationEnvironmentList.append(se)

def simulate(se):
    se.constantsAndRandom.setRandomState()
    while(not se.simulationEndingCondition):
        se.simulateDay()
        finalString = ""
        dirToSave = "SimulationStates/"
        nullString = ""
        if(se.constantsAndRandom.id < 1000):
            nullString="0"
        if(se.constantsAndRandom.id < 100):
            nullString="00"
        if(se.constantsAndRandom.id < 10):
            nullString="000"
        if(se.simulationEndingCondition):
            finalString="final_"
            dirToSave = "SimulationStatesFinished/"
        with open(dirToSave + finalString + "simulationResult_" + nullString + str(se.constantsAndRandom.id) + "_" + str(se.day) + ".pickle", 'wb') as f:
            pickle.dump(se, f)
                
        if(se.simulationEndingCondition and os.path.exists("SimulationStates/" + "simulationResult_" + nullString + str(se.constantsAndRandom.id) + "_" + str(se.day) + ".pickle")):
            os.remove("SimulationStates/" + "simulationResult_" + nullString + str(se.constantsAndRandom.id) + "_" + str(se.day) + ".pickle")
                
        finalString = ""
        dirToSave = "SimulationStates/"
        if os.path.exists(dirToSave + finalString + "simulationResult_" + nullString + str(se.constantsAndRandom.id) + "_" + str(se.day-1) + ".pickle"):
            os.remove(dirToSave + finalString + "simulationResult_" + nullString + str(se.constantsAndRandom.id) + "_" + str(se.day-1) + ".pickle")

if __name__ == '__main__':
    pool = mp.Pool(numberOfCores)
    results=pool.map(simulate,simulationEnvironmentList)