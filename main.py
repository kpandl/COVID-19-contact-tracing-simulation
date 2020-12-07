# -*- coding: utf-8 -*-

from ConstantsAndRandom import ConstantsAndRandom
from SimulationEnvironment import SimulationEnvironment
import pickle
import time as tm
import cProfile
import pstats
import sys

sys.setrecursionlimit(10000)

def simulateWithSeed(seed):
    constantsAndRandom = ConstantsAndRandom(0)
    constantsAndRandom.description = "QR code"
    constantsAndRandom.simulationTimeStepInMillisecond = 1000
    if(seed == 0):
        constantsAndRandom.contactTracingAdoptionPercentage = 60
        constantsAndRandom.contactTracingStopProbabilityForPersonAfterFalsePositive = 1
        constantsAndRandom.proximityBasedContactTracing = False
        
    se = SimulationEnvironment(constantsAndRandom)
    i=0
    while(not se.simulationEndingCondition):
        se.simulateDay()
        i=i+1
        dayString = str(se.day)
        if(se.day< 10):
            dayString = "0" + str(se.day)
        with open("SimulationStates/main_simulationResult_" + str(seed) + "_" + dayString + ".pickle", 'wb') as f:
            pickle.dump(se, f)

start = tm.time()
for i in range(0,1):
    simulateWithSeed(i)

end = tm.time()
print(end - start)