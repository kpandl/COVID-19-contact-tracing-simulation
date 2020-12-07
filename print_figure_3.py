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

rows = 2
cols = 2
numberOfPlotsPerSubsection = 5

Main_populationSize = 10000

graphColors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
titlePrefixList = ['A', 'B', 'C', 'D']
titlePrefixCounter = 0

fig, axs = plt.subplots(rows, cols, figsize=(15,9))
shareListNoCT = np.asarray([100 * x.mean / Main_populationSize for x in simulationEnvironmentList[0].ciArray_averageNumberOfPeopleInfectious])
shareListNoCTHalfInterval = np.asarray([100 * x.halfInterval / Main_populationSize for x in simulationEnvironmentList[0].ciArray_averageNumberOfPeopleInfectious])


for simulationEnvironment in simulationEnvironmentList:
    shareList = np.asarray([100 * x.mean / Main_populationSize for x in simulationEnvironment.ciArray_averageNumberOfPeopleInfectious])
    shareListHalfInterval = np.asarray([100 * x.halfInterval / Main_populationSize for x in simulationEnvironment.ciArray_averageNumberOfPeopleInfectious])
    if(simulationEnvironment.firstID % 46 >= 26):

        if(simulationEnvironment.firstID % 46 == 26):
            
            infoQuarantineMeasures = "with quarantine measures"

            simulationDescriptionString = "R0=2.5 when simulated without CT and " + infoQuarantineMeasures + ". Here simulated with quarantine measures."

        figureNumber = 1 + math.floor((simulationEnvironment.firstID % 46 - 1) / numberOfPlotsPerSubsection) - 6
        plotRow = math.floor(figureNumber/cols)
        plotCol = figureNumber % cols
        plotColorIndex = (simulationEnvironment.firstID - 1) % 5

        x = np.linspace(0,len(shareList),len(shareList))
        axs[plotRow, plotCol].plot(x, shareList, label=str(simulationEnvironment.description.replace(" proximity", "").replace("QR code","Site-wide")))
        axs[plotRow, plotCol].fill_between(x,shareList - shareListHalfInterval, shareList + shareListHalfInterval, color=graphColors[plotColorIndex], alpha=.1)

        print(f"{simulationEnvironment.description}: {simulationEnvironment.ci_r0.mean}")

        a = 0

        if(figureNumber != 1 + math.floor(((simulationEnvironment.firstID+1) % 46 - 1) / numberOfPlotsPerSubsection) - 6):
            x = np.linspace(0,len(shareListNoCT),len(shareListNoCT))
            axs[plotRow, plotCol].plot(x, shareListNoCT, ':', label="No CT", color=graphColors[5])
            axs[plotRow, plotCol].fill_between(x,shareListNoCT - shareListNoCTHalfInterval, shareListNoCT + shareListNoCTHalfInterval, color=graphColors[5], alpha=.1)
            axs[plotRow, plotCol].legend(loc="upper right")
            axs[plotRow, plotCol].set_title("" + titlePrefixList[titlePrefixCounter] + " " + str(int(100*simulationEnvironment.contactTracingStopProbabilityForPersonAfterFalsePositive)) + "% probability of an individual stopping CT\nafter being in quarantine but not having had symptoms")
            titlePrefixCounter += 1
            axs[plotRow, plotCol].set_xlabel("Time [Days]")
            axs[plotRow, plotCol].set_ylabel("Share of infectious individuals,\naverage and 90% CI [%]")

fig.tight_layout()
fig.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig(path+"/figure_2.png")
plt.show()