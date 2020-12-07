# -*- coding: utf-8 -*-

import time as tm
import sys
import time
import math
import shutil
import os
import time
from os import listdir
from os.path import isfile, join
from shutil import copyfile
from SimulationClass import SimulationClass
from ConfidenceInterval import ConfidenceInterval
import pickle
import numpy as np
import gc

sys.setrecursionlimit(10000)

simulationTypes = 46
simulationsPerSimulationType = 30

listOfFinishedSimulations = []

pathToStoreConsolidatedResults = "finishedSimulationStatesConsolidated/"
if not os.path.exists(os.path.join(os.getcwd(), pathToStoreConsolidatedResults)):
    os.makedirs(os.path.join(os.getcwd(), pathToStoreConsolidatedResults))

path = "finishedSimulationStates/"
fileNameList = os.listdir(path)
pathList = [path + x for x in fileNameList]

classFinishedCounter = 0

for i in range(0,simulationTypes):
    simulationClass = SimulationClass(i, pathToStoreConsolidatedResults)
    print("---------------------------------------")
    print(f"Simulation type: {i}")
    itTexts = []
    filePaths = []

    for filePath in pathList:
        idText = filePath.split("_")[2]
        id = int(idText)
        simulationType = id % simulationTypes

        if(simulationType == i):
            itTexts.append(idText)#
            filePaths.append(filePath)#
            finishedSimulation = pickle.load( open( filePath, "rb" ) )
            simulationClass.addFinishedSimulation(finishedSimulation)
            print(f"loaded {id}")
    
    simulationClass.calculateValues()
    del(simulationClass)
    gc.collect()

print("finished")