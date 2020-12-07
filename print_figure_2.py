# -*- coding: utf-8 -*-

from ConstantsAndRandom import ConstantsAndRandom
from SimulationEnvironment import SimulationEnvironment
import pickle
import time as tm
import cProfile
import pstats
import sys
import os
import matplotlib.pyplot as plt
import math
from SimulationClass import SimulationClass
from ConfidenceInterval import ConfidenceInterval
import csv
import numpy as np
  
sys.setrecursionlimit(10000)

path = "finishedSimulationStatesConsolidated/"

fileNameList = os.listdir(path)
simulationEnvironmentList = []
legendList = []

i = 0


for fileName in fileNameList:
    if fileName=="_description.txt" or fileName=="other" or fileName=="figure_1.png" or fileName=="figure_2.png" or fileName=="figure_3.png" or fileName=="figure_3b.png" or fileName=="figure_3c.png" or fileName=="figure_3d.png" or fileName=="figure_4.png" or fileName=="result_file.csv":
        continue
    se = pickle.load( open( path+fileName, "rb" ) )
    simulationEnvironmentList.append(se)

rows = 3
cols = 2
numberOfPlotsPerSubsection = 5

Main_populationSize = 10000

fig, axs = plt.subplots(rows, cols, figsize=(15,9))
shareListNoCT = np.asarray([100 * x.mean / Main_populationSize for x in simulationEnvironmentList[0].ciArray_averageNumberOfPeopleInfectious])
shareListNoCTHalfInterval = np.asarray([100 * x.halfInterval / Main_populationSize for x in simulationEnvironmentList[0].ciArray_averageNumberOfPeopleInfectious])

graphColors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
titlePrefixList = ['A', 'B', 'C', 'D', 'E', 'F']
titlePrefixCounter = 0

with open(path+'result_file.csv', mode='w', newline='') as result_file:
    csv_writer = csv.writer(result_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    csv_writer.writerow(['Adoption [%]', 'Deadoption probability [%]', 'PDR', 'Maximum share of infectious individuals [%]', 'Time till maximums share of individuals infectious [days]', 'Duration of the epidemic [days]', 'Average time of quarantine per individual [days]', 'Susceptible share of the quarantine [%]', 'Share of susceptible individuals at the end [%]', 'R0'])

    for simulationEnvironment in simulationEnvironmentList:
        shareList = np.asarray([100 * x.mean / Main_populationSize for x in simulationEnvironment.ciArray_averageNumberOfPeopleInfectious])
        shareListHalfInterval = np.asarray([100 * x.halfInterval / Main_populationSize for x in simulationEnvironment.ciArray_averageNumberOfPeopleInfectious])
        figureNumber = 0
        if(simulationEnvironment.firstID % 46 == 0):

            infoQuarantineMeasures = "with quarantine measures"
            simulationDescriptionString = "R0=2.5 when simulated without CT and " + infoQuarantineMeasures + ". Here simulated with quarantine measures."

            x = np.linspace(0,len(shareList),len(shareList))
            axs[0, 0].plot(x, shareList, color=graphColors[5])
            axs[0, 0].fill_between(x,shareList - shareListHalfInterval, shareList + shareListHalfInterval, color=graphColors[5], alpha=.1)
            axs[0, 0].set_title(titlePrefixList[titlePrefixCounter] + " " + simulationEnvironment.description)
            titlePrefixCounter += 1
            axs[0, 0].set_xlabel("Time [Days]")
            axs[0, 0].set_ylabel("Share of infectious individuals,\n average and 90% CI [%]")
        else:
            figureNumber = 1 + math.floor((simulationEnvironment.firstID % 46 - 1) / numberOfPlotsPerSubsection)

        adoptionPercentage = simulationEnvironment.contactTracingAdoptionPercentage
        if(not simulationEnvironment.contactTracingOn):
            adoptionPercentage = 0

        a = simulationEnvironment.ci_r0.mean
        csv_writer.writerow([f"{adoptionPercentage}", f"{100*simulationEnvironment.contactTracingStopProbabilityForPersonAfterFalsePositive}", simulationEnvironment.description.replace(" proximity","").replace("QR code","Site-wide"), f"{100*simulationEnvironment.ci_maximumShareOfPeopleInfectious.mean:.3f} ± {100*simulationEnvironment.ci_maximumShareOfPeopleInfectious.halfInterval:.3f}", f"{simulationEnvironment.ci_timeTillMaximumShareOfInfectious.mean:.3f} ± {100*simulationEnvironment.ci_timeTillMaximumShareOfInfectious.halfInterval:.3f}", f"{simulationEnvironment.ci_timeOfPandemic.mean:.3f} ± {simulationEnvironment.ci_timeOfPandemic.halfInterval:.3f}", f"{simulationEnvironment.ci_averageTimeOfQuarantinePerPerson.mean:.3f} ± {simulationEnvironment.ci_averageTimeOfQuarantinePerPerson.halfInterval:.3f}", f"{100*simulationEnvironment.ci_shareDaysSpentInQuarantineOfPeopleSusceptibleByTotalQuarantineDays.mean:.3f} ± {100*simulationEnvironment.ci_shareDaysSpentInQuarantineOfPeopleSusceptibleByTotalQuarantineDays.halfInterval:.3f}", f"{100*simulationEnvironment.ci_shareOfSusceptiblePeopleAtTheEnd.mean:.3f} ± {100*simulationEnvironment.ci_shareOfSusceptiblePeopleAtTheEnd.halfInterval:.3f}", f"{simulationEnvironment.ci_r0.mean:.3f} ± {simulationEnvironment.ci_r0.halfInterval:.3f}"])

        if(simulationEnvironment.firstID % 46 > 0 and simulationEnvironment.firstID % 46 <= 25):
            plotRow = math.floor(figureNumber/cols)
            plotCol = figureNumber % cols

            plotColorIndex = (simulationEnvironment.firstID - 1) % 5
            
            x = np.linspace(0,len(shareList),len(shareList))
            axs[plotRow, plotCol].plot(x, shareList, label=str(simulationEnvironment.description.replace(" proximity","").replace("QR code","Sites-wide")), color=graphColors[plotColorIndex])
            axs[plotRow, plotCol].fill_between(x,shareList - shareListHalfInterval, shareList + shareListHalfInterval, color=graphColors[plotColorIndex], alpha=.1)

            if(figureNumber != 1 + math.floor((simulationEnvironment.firstID % 46) / numberOfPlotsPerSubsection)):
                x = np.linspace(0,len(shareListNoCT),len(shareListNoCT))
                axs[plotRow, plotCol].plot(x, shareListNoCT, ':', label="No CT", color=graphColors[5])
                axs[plotRow, plotCol].fill_between(x,shareListNoCT - shareListNoCTHalfInterval, shareListNoCT + shareListNoCTHalfInterval, color=graphColors[5], alpha=.1)
                axs[plotRow, plotCol].legend(loc="upper right")
                axs[plotRow, plotCol].set_title(titlePrefixList[titlePrefixCounter] + " " + str(simulationEnvironment.contactTracingAdoptionPercentage) + "% adoption")
                titlePrefixCounter += 1
                axs[plotRow, plotCol].set_xlabel("Time [Days]")
                axs[plotRow, plotCol].set_ylabel("Share of infectious individuals,\n average and 90% CI [%]")

fig.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig(path+"/figure_1.png")
plt.show()