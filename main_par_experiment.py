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

numberOfCores = 4

sys.setrecursionlimit(10000)
limit = sys.getrecursionlimit()  

constantsAndRandomList = []

if not os.path.exists(os.path.join(os.getcwd(), "SimulationStates")):
    os.makedirs(os.path.join(os.getcwd(), "SimulationStates"))
if not os.path.exists(os.path.join(os.getcwd(), "SimulationStatesFinished")):
    os.makedirs(os.path.join(os.getcwd(), "SimulationStatesFinished"))

print("running parallel")

carCount = 0

for j in range(1):
    for i in range(46):
        car = ConstantsAndRandom(j)

        car.id = carCount
        carCount = carCount + 1

        if(car.id % 46 == 0):
            car.description = "Without CT"
            car.contactTracingOn = False
        if(car.id % 46 == 1):
            car.description = "0.2 m proximity"
            car.contactTracingAdoptionPercentage = 20
            car.ContactTracingRadiusMeter = 0.2
        if(car.id % 46 == 2):
            car.description = "1 m proximity"
            car.contactTracingAdoptionPercentage = 20
            car.ContactTracingRadiusMeter = 1
        if(car.id % 46 == 3):
            car.description = "2 m proximity"
            car.contactTracingAdoptionPercentage = 20
            car.ContactTracingRadiusMeter = 2
        if(car.id % 46 == 4):
            car.description = "10 m proximity"
            car.contactTracingAdoptionPercentage = 20
            car.ContactTracingRadiusMeter = 10
        if(car.id % 46 == 5):
            car.description = "QR code"
            car.contactTracingAdoptionPercentage = 20
            car.proximityBasedContactTracing = False
        if(car.id % 46 == 6):
            car.description = "0.2 m proximity"
            car.contactTracingAdoptionPercentage = 40
            car.ContactTracingRadiusMeter = 0.2
        if(car.id % 46 == 7):
            car.description = "1 m proximity"
            car.contactTracingAdoptionPercentage = 40
            car.ContactTracingRadiusMeter = 1
        if(car.id % 46 == 8):
            car.description = "2 m proximity"
            car.contactTracingAdoptionPercentage = 40
            car.ContactTracingRadiusMeter = 2
        if(car.id % 46 == 9):
            car.description = "10 m proximity"
            car.contactTracingAdoptionPercentage = 40
            car.ContactTracingRadiusMeter = 10
        if(car.id % 46 == 10):
            car.description = "QR code"
            car.contactTracingAdoptionPercentage = 40
            car.proximityBasedContactTracing = False
        if(car.id % 46 == 11):
            car.description = "0.2 m proximity"
            car.contactTracingAdoptionPercentage = 60
            car.ContactTracingRadiusMeter = 0.2
        if(car.id % 46 == 12):
            car.description = "1 m proximity"
            car.contactTracingAdoptionPercentage = 60
            car.ContactTracingRadiusMeter = 1
        if(car.id % 46 == 13):
            car.description = "2 m proximity"
            car.contactTracingAdoptionPercentage = 60
            car.ContactTracingRadiusMeter = 2
        if(car.id % 46 == 14):
            car.description = "10 m proximity"
            car.contactTracingAdoptionPercentage = 60
            car.ContactTracingRadiusMeter = 10
        if(car.id % 46 == 15):
            car.description = "QR code"
            car.contactTracingAdoptionPercentage = 60
            car.proximityBasedContactTracing = False
        if(car.id % 46 == 16):
            car.description = "0.2 m proximity"
            car.contactTracingAdoptionPercentage = 80
            car.ContactTracingRadiusMeter = 0.2
        if(car.id % 46 == 17):
            car.description = "1 m proximity"
            car.contactTracingAdoptionPercentage = 80
            car.ContactTracingRadiusMeter = 1
        if(car.id % 46 == 18):
            car.description = "2 m proximity"
            car.contactTracingAdoptionPercentage = 80
            car.ContactTracingRadiusMeter = 2
        if(car.id % 46 == 19):
            car.description = "10 m proximity"
            car.contactTracingAdoptionPercentage = 80
            car.ContactTracingRadiusMeter = 10
        if(car.id % 46 == 20):
            car.description = "QR code"
            car.contactTracingAdoptionPercentage = 80
            car.proximityBasedContactTracing = False
        if(car.id % 46 == 21):
            car.description = "0.2 m proximity"
            car.contactTracingAdoptionPercentage = 100
            car.ContactTracingRadiusMeter = 0.2
        if(car.id % 46 == 22):
            car.description = "1 m proximity"
            car.contactTracingAdoptionPercentage = 100
            car.ContactTracingRadiusMeter = 1
        if(car.id % 46 == 23):
            car.description = "2 m proximity"
            car.contactTracingAdoptionPercentage = 100
            car.ContactTracingRadiusMeter = 2
        if(car.id % 46 == 24):
            car.description = "10 m proximity"
            car.contactTracingAdoptionPercentage = 100
            car.ContactTracingRadiusMeter = 10
        if(car.id % 46 == 25):
            car.description = "QR code"
            car.contactTracingAdoptionPercentage = 100
            car.proximityBasedContactTracing = False
        if(car.id % 46 == 26):
            car.description = "0.2 m proximity"
            car.contactTracingAdoptionPercentage = 60
            car.contactTracingStopProbabilityForPersonAfterFalsePositive = 0.25
            car.ContactTracingRadiusMeter = 0.2
        if(car.id % 46 == 27):
            car.description = "1 m proximity"
            car.contactTracingAdoptionPercentage = 60
            car.contactTracingStopProbabilityForPersonAfterFalsePositive = 0.25
            car.ContactTracingRadiusMeter = 1
        if(car.id % 46 == 28):
            car.description = "2 m proximity"
            car.contactTracingAdoptionPercentage = 60
            car.contactTracingStopProbabilityForPersonAfterFalsePositive = 0.25
            car.ContactTracingRadiusMeter = 2
        if(car.id % 46 == 29):
            car.description = "10 m proximity"
            car.contactTracingAdoptionPercentage = 60
            car.contactTracingStopProbabilityForPersonAfterFalsePositive = 0.25
            car.ContactTracingRadiusMeter = 10
        if(car.id % 46 == 30):
            car.description = "QR code"
            car.contactTracingAdoptionPercentage = 60
            car.contactTracingStopProbabilityForPersonAfterFalsePositive = 0.25
            car.proximityBasedContactTracing = False
        if(car.id % 46 == 31):
            car.description = "0.2 m proximity"
            car.contactTracingAdoptionPercentage = 60
            car.contactTracingStopProbabilityForPersonAfterFalsePositive = 0.50
            car.ContactTracingRadiusMeter = 0.2
        if(car.id % 46 == 32):
            car.description = "1 m proximity"
            car.contactTracingAdoptionPercentage = 60
            car.contactTracingStopProbabilityForPersonAfterFalsePositive = 0.50
            car.ContactTracingRadiusMeter = 1
        if(car.id % 46 == 33):
            car.description = "2 m proximity"
            car.contactTracingAdoptionPercentage = 60
            car.contactTracingStopProbabilityForPersonAfterFalsePositive = 0.50
            car.ContactTracingRadiusMeter = 2
        if(car.id % 46 == 34):
            car.description = "10 m proximity"
            car.contactTracingAdoptionPercentage = 60
            car.contactTracingStopProbabilityForPersonAfterFalsePositive = 0.50
            car.ContactTracingRadiusMeter = 10
        if(car.id % 46 == 35):
            car.description = "QR code"
            car.contactTracingAdoptionPercentage = 60
            car.contactTracingStopProbabilityForPersonAfterFalsePositive = 0.50
            car.proximityBasedContactTracing = False
        if(car.id % 46 == 36):
            car.description = "0.2 m proximity"
            car.contactTracingAdoptionPercentage = 60
            car.contactTracingStopProbabilityForPersonAfterFalsePositive = 0.75
            car.ContactTracingRadiusMeter = 0.2
        if(car.id % 46 == 37):
            car.description = "1 m proximity"
            car.contactTracingAdoptionPercentage = 60
            car.contactTracingStopProbabilityForPersonAfterFalsePositive = 0.75
            car.ContactTracingRadiusMeter = 1
        if(car.id % 46 == 38):
            car.description = "2 m proximity"
            car.contactTracingAdoptionPercentage = 60
            car.contactTracingStopProbabilityForPersonAfterFalsePositive = 0.75
            car.ContactTracingRadiusMeter = 2
        if(car.id % 46 == 39):
            car.description = "10 m proximity"
            car.contactTracingAdoptionPercentage = 60
            car.contactTracingStopProbabilityForPersonAfterFalsePositive = 0.75
            car.ContactTracingRadiusMeter = 10
        if(car.id % 46 == 40):
            car.description = "QR code"
            car.contactTracingAdoptionPercentage = 60
            car.contactTracingStopProbabilityForPersonAfterFalsePositive = 0.75
            car.proximityBasedContactTracing = False
        if(car.id % 46 == 41):
            car.description = "0.2 m proximity"
            car.contactTracingAdoptionPercentage = 60
            car.contactTracingStopProbabilityForPersonAfterFalsePositive = 1
            car.ContactTracingRadiusMeter = 0.2
        if(car.id % 46 == 42):
            car.description = "1 m proximity"
            car.contactTracingAdoptionPercentage = 60
            car.contactTracingStopProbabilityForPersonAfterFalsePositive = 1
            car.ContactTracingRadiusMeter = 1
        if(car.id % 46 == 43):
            car.description = "2 m proximity"
            car.contactTracingAdoptionPercentage = 60
            car.contactTracingStopProbabilityForPersonAfterFalsePositive = 1
            car.ContactTracingRadiusMeter = 2
        if(car.id % 46 == 44):
            car.description = "10 m proximity"
            car.contactTracingAdoptionPercentage = 60
            car.contactTracingStopProbabilityForPersonAfterFalsePositive = 1
            car.ContactTracingRadiusMeter = 10
        if(car.id % 46 == 45):
            car.description = "QR code"
            car.contactTracingAdoptionPercentage = 60
            car.contactTracingStopProbabilityForPersonAfterFalsePositive = 1
            car.proximityBasedContactTracing = False
            
        constantsAndRandomList.append(car)

computeStartPosition = 0

with open('computeStartPosition.txt', 'r') as file:
    computeStartPosition = int(file.read().replace('\n', ''))

def simulate(car):
    se = SimulationEnvironment(car)
    start = time.time()
    while(not se.simulationEndingCondition):
        se.simulateDay()
        end = time.time()
        se.timeElapsed = end - start

        finalString = ""
        dirToSave = "SimulationStates/"
        nullString = ""
        if(car.id < 1000):
            nullString="0"
        if(car.id < 100):
            nullString="00"
        if(car.id < 10):
            nullString="000"
        if(se.simulationEndingCondition):
            finalString="final_"
            dirToSave = "SimulationStatesFinished/"
        with open(dirToSave + finalString + "simulationResult_" + nullString + str(car.id) + "_" + str(se.day) + ".pickle", 'wb') as f:
            pickle.dump(se, f)
        if(se.simulationEndingCondition and os.path.exists("SimulationStates/" + "simulationResult_" + nullString + str(car.id) + "_" + str(se.day) + ".pickle")):
            os.remove("SimulationStates/" + "simulationResult_" + nullString + str(car.id) + "_" + str(se.day) + ".pickle")
                
        finalString = ""
        dirToSave = "SimulationStates/"
        if os.path.exists(dirToSave + finalString + "simulationResult_" + nullString + str(car.id) + "_" + str(se.day-1) + ".pickle"):
            os.remove(dirToSave + finalString + "simulationResult_" + nullString + str(car.id) + "_" + str(se.day-1) + ".pickle")

if __name__ == '__main__':
    pool = mp.Pool(numberOfCores)
    results=pool.map(simulate,constantsAndRandomList)