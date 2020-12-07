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
from ConfidenceInterval import ConfidenceInterval
import pickle
import numpy as np

class SimulationClass:
    
    def __init__(self, firstID, pathToStoreConsolidatedResults):
        self.firstID = firstID
        self.finishedSimulations = []
        self.pathToStoreConsolidatedResults = pathToStoreConsolidatedResults

    def addFinishedSimulation(self, finishedSimulation):
        self.finishedSimulations.append(finishedSimulation)
        if(len(self.finishedSimulations) == 1):
            self.description = finishedSimulation.constantsAndRandom.description
            self.contactTracingOn = finishedSimulation.constantsAndRandom.contactTracingOn
            self.proximityBasedContactTracing = finishedSimulation.constantsAndRandom.proximityBasedContactTracing
            self.contactTracingAdoptionPercentage = finishedSimulation.constantsAndRandom.contactTracingAdoptionPercentage
            self.ContactTracingRadiusMeter = finishedSimulation.constantsAndRandom.ContactTracingRadiusMeter
            self.contactTracingStopProbabilityForPersonAfterFalsePositive = finishedSimulation.constantsAndRandom.contactTracingStopProbabilityForPersonAfterFalsePositive
            self.Main_populationSize = finishedSimulation.constantsAndRandom.Main_populationSize

    def obtainAverageDailyList(self, propertyName):
        averageList = []
        loopCondition = True
        i = 0
        while(loopCondition):
            loopCondition = False
            dailyValues = []
            for finishedSimulation in self.finishedSimulations:
                dailyValue = 0
                if(len(getattr(finishedSimulation, propertyName)) > i):
                    dailyValue = getattr(finishedSimulation, propertyName)[i]
                    loopCondition = True
                else:
                    dailyValue = getattr(finishedSimulation, propertyName)[-1]
                dailyValues.append(dailyValue)
            if(loopCondition):
                averageList.append(sum(dailyValues)/len(dailyValues))
                i += 1
        return(averageList)
        
    def calculateValues(self):
        maximumShareOfPeopleInfectious = []
        timeTillMaximumShareOfInfectious = []
        averageTimeOfQuarantinePerPerson = []
        timeOfPandemic = []
        shareOfSusceptiblePeopleAtTheEnd = []
        r0 = []

        totalDaysSpentInQuarantine = []
        totalDaysSpentInQuarantineOfPeopleSusceptible = []
        totalDaysSpentInQuarantineOfPeopleExposed = []
        totalDaysSpentInQuarantineOfPeopleInfectious = []
        totalDaysSpentInQuarantineOfPeopleRecovered = []
        shareDaysSpentInQuarantineOfPeopleSusceptibleByTotalQuarantineDays = []

        quotient = []
        self.ids = []

        averageSensitivityOfQuarantineMeasures = []
        averageSpecificityOfQuarantineMeasures = []
        averagePrecisionOfQuarantineMeasures = []
        averageFalsePositiveRateOfQuarantineMeasures = []

        simulationTimes = []

        for finishedSimulation in self.finishedSimulations:
            simulationTimes.append(finishedSimulation.timeElapsed)
            local_maxShareOfPeopleInfectious = max(finishedSimulation.numberInfectiousEndOfDay)
            maximumShareOfPeopleInfectious.append(local_maxShareOfPeopleInfectious / finishedSimulation.constantsAndRandom.Main_populationSize)
            local_timeTillMaximumShareOfInfectious = finishedSimulation.numberInfectiousEndOfDay.index(local_maxShareOfPeopleInfectious)
            timeTillMaximumShareOfInfectious.append(local_timeTillMaximumShareOfInfectious)

            local_averageTimeOfQuarantinePerPerson = sum(finishedSimulation.numberInQuarantineEndOfDay)/len(finishedSimulation.personList)

            averageTimeOfQuarantinePerPerson.append(local_averageTimeOfQuarantinePerPerson)
            timeOfPandemic.append(len(finishedSimulation.numberSusceptibleEndOfDay))

            local_numberOfSusceptiblePeopleAtTheEnd=finishedSimulation.numberSusceptibleEndOfDay[-1]
            local_shareOfSusceptiblePeopleAtTheEnd = local_numberOfSusceptiblePeopleAtTheEnd / finishedSimulation.constantsAndRandom.Main_populationSize
            shareOfSusceptiblePeopleAtTheEnd.append(local_shareOfSusceptiblePeopleAtTheEnd)

            local_r0 = finishedSimulation.constantsAndRandom.Main_populationSize / (finishedSimulation.constantsAndRandom.Main_populationSize - local_numberOfSusceptiblePeopleAtTheEnd) * (math.log(finishedSimulation.constantsAndRandom.Main_populationSize - finishedSimulation.constantsAndRandom.numberOfPeopleInitiallyInfectious) - math.log(local_numberOfSusceptiblePeopleAtTheEnd))
            r0.append(local_r0)

            quotient.append(local_shareOfSusceptiblePeopleAtTheEnd / local_averageTimeOfQuarantinePerPerson)
            self.ids.append(finishedSimulation.constantsAndRandom.id)

            totalDaysSpentInQuarantine.append(sum(finishedSimulation.numberInQuarantineEndOfDay))
            totalDaysSpentInQuarantineOfPeopleSusceptible.append(sum(finishedSimulation.numberInQuarantineAndSusceptibleEndOfDay))
            totalDaysSpentInQuarantineOfPeopleExposed.append(sum(finishedSimulation.numberInQuarantineAndExposedEndOfDay))
            totalDaysSpentInQuarantineOfPeopleInfectious.append(sum(finishedSimulation.numberInQuarantineAndInfectiousEndOfDay))
            totalDaysSpentInQuarantineOfPeopleRecovered.append(sum(finishedSimulation.numberInQuarantineAndRecoveredEndOfDay))

            shareDaysSpentInQuarantineOfPeopleSusceptibleByTotalQuarantineDays.append(sum(finishedSimulation.numberInQuarantineAndSusceptibleEndOfDay)/sum(finishedSimulation.numberInQuarantineEndOfDay))


            sensitivityValues = []
            specificityValues = []
            precisionValues = []
            falsePositiveRateValues = []

            for i in range(0,len(finishedSimulation.numberInfectiousEndOfDay)):

                positives = finishedSimulation.numberExposedEndOfDay[i] + finishedSimulation.numberInfectiousEndOfDay[i]
                truePositives = finishedSimulation.numberInQuarantineAndExposedEndOfDay[i] + finishedSimulation.numberInQuarantineAndInfectiousEndOfDay[i]

                negatives = finishedSimulation.numberSusceptibleEndOfDay[i]+finishedSimulation.numberRecoveredEndOfDay[i]
                trueNegatives = finishedSimulation.numberSusceptibleEndOfDay[i]-finishedSimulation.numberInQuarantineAndSusceptibleEndOfDay[i]+finishedSimulation.numberRecoveredEndOfDay[i]-finishedSimulation.numberInQuarantineAndRecoveredEndOfDay[i]

                falsePositives = finishedSimulation.numberInQuarantineAndSusceptibleEndOfDay[i] + finishedSimulation.numberInQuarantineAndRecoveredEndOfDay[i]

                if(positives > 0):
                    sensitivityValue = truePositives / positives
                    sensitivityValues.append(sensitivityValue)

                if(negatives > 0):
                    specificityValue = trueNegatives / negatives
                    specificityValues.append(specificityValue)

                if(truePositives + falsePositives > 0):
                    precisionValue = truePositives / (truePositives + falsePositives)
                    precisionValues.append(precisionValue)

                if(falsePositives + trueNegatives > 0):
                    falsePositiveRateValue = falsePositives / (falsePositives + trueNegatives)
                    falsePositiveRateValues.append(falsePositiveRateValue)
            
            averageSensitivityOfQuarantineMeasures.append(sum(sensitivityValues)/len(sensitivityValues))

            averageSpecificityOfQuarantineMeasures.append(sum(specificityValues)/len(specificityValues))
            averagePrecisionOfQuarantineMeasures.append(sum(precisionValues)/len(precisionValues))
            averageFalsePositiveRateOfQuarantineMeasures.append(sum(falsePositiveRateValues)/len(falsePositiveRateValues))


        self.ci_maximumShareOfPeopleInfectious = ConfidenceInterval(maximumShareOfPeopleInfectious)
        self.ci_timeTillMaximumShareOfInfectious = ConfidenceInterval(timeTillMaximumShareOfInfectious)
        self.ci_averageTimeOfQuarantinePerPerson = ConfidenceInterval(averageTimeOfQuarantinePerPerson)
        self.ci_timeOfPandemic = ConfidenceInterval(timeOfPandemic)
        self.ci_shareOfSusceptiblePeopleAtTheEnd = ConfidenceInterval(shareOfSusceptiblePeopleAtTheEnd)
        self.r0Values = r0
        self.ci_r0 = ConfidenceInterval(r0)
        self.ci_totalDaysSpentInQuarantine = ConfidenceInterval(totalDaysSpentInQuarantine)
        self.ci_totalDaysSpentInQuarantineOfPeopleSusceptible = ConfidenceInterval(totalDaysSpentInQuarantineOfPeopleSusceptible)
        self.ci_totalDaysSpentInQuarantineOfPeopleExposed = ConfidenceInterval(totalDaysSpentInQuarantineOfPeopleExposed)
        self.ci_totalDaysSpentInQuarantineOfPeopleInfectious = ConfidenceInterval(totalDaysSpentInQuarantineOfPeopleInfectious)
        self.ci_totalDaysSpentInQuarantineOfPeopleRecovered = ConfidenceInterval(totalDaysSpentInQuarantineOfPeopleRecovered)
        
        self.ci_shareDaysSpentInQuarantineOfPeopleSusceptibleByTotalQuarantineDays = ConfidenceInterval(shareDaysSpentInQuarantineOfPeopleSusceptibleByTotalQuarantineDays)
        
        self.ci_quotient = ConfidenceInterval(quotient)
        self.quotient = quotient
        self.shareOfSusceptiblePeopleAtTheEnd = shareOfSusceptiblePeopleAtTheEnd
        self.averageTimeOfQuarantinePerPerson = averageTimeOfQuarantinePerPerson
        
        self.ci_averageSensitivityOfQuarantineMeasures = ConfidenceInterval(averageSensitivityOfQuarantineMeasures)
        self.ci_averageSpecificityOfQuarantineMeasures = ConfidenceInterval(averageSpecificityOfQuarantineMeasures)
        self.ci_averagePrecisionOfQuarantineMeasures = ConfidenceInterval(averagePrecisionOfQuarantineMeasures)
        self.ci_averageFalsePositiveRateOfQuarantineMeasures = ConfidenceInterval(averageFalsePositiveRateOfQuarantineMeasures)

        self.averageNumberOfPeopleInfectious = []
        self.ciArray_averageNumberOfPeopleInfectious = []
        loopCondition = True
        i = 0
        while(loopCondition):
            loopCondition = False
            dailyValues = []
            for finishedSimulation in self.finishedSimulations:
                dailyValue = 0
                if(len(finishedSimulation.numberInfectiousEndOfDay) > i):
                    dailyValue = finishedSimulation.numberInfectiousEndOfDay[i]
                    loopCondition = True
                else:
                    dailyValue = finishedSimulation.numberInfectiousEndOfDay[-1]
                dailyValues.append(dailyValue)
            if(loopCondition):
                self.averageNumberOfPeopleInfectious.append(sum(dailyValues)/len(dailyValues))
                self.ciArray_averageNumberOfPeopleInfectious.append(ConfidenceInterval(dailyValues))
                i += 1

        self.averageNumberOfPeopleInQuarantineEndOfDay = self.obtainAverageDailyList("numberInQuarantineEndOfDay")
        self.averageNumberOfPeopleInQuarantineAndSusceptibleEndOfDay = self.obtainAverageDailyList("numberInQuarantineAndSusceptibleEndOfDay")
        self.averageNumberOfPeopleInQuarantineAndExposedEndOfDay = self.obtainAverageDailyList("numberInQuarantineAndExposedEndOfDay")
        self.averageNumberOfPeopleInQuarantineAndInfectiousEndOfDay = self.obtainAverageDailyList("numberInQuarantineAndInfectiousEndOfDay")
        self.averageNumberOfPeopleInQuarantineAndRecoveredEndOfDay = self.obtainAverageDailyList("numberInQuarantineAndRecoveredEndOfDay")


        del(self.finishedSimulations)
        a = 0
        
        nullString = ""
        if(self.firstID < 10):
            nullString="0"

        with open(os.path.join(self.pathToStoreConsolidatedResults,nullString + str(self.firstID) + ".pickle"), 'wb') as f:
            pickle.dump(self, f)

        return (0==0)