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
  
def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        axs[plotCol].annotate('{:.1f}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', rotation=90)

sys.setrecursionlimit(10000)

path = "finishedSimulationStatesConsolidated/"

fileNameList = os.listdir(path)
simulationEnvironmentList = []
legendList = []

i = 0


for fileName in fileNameList:
    if fileName=="_description.txt" or fileName=="other" or fileName=="figure_1.png" or fileName=="figure_2.png" or fileName=="figure_3.png" or fileName=="figure_3b.png" or fileName=="figure_3c.png" or fileName=="figure_3d.png" or fileName=="figure_3e.png" or fileName=="figure_4.png" or fileName=="result_file.csv":
        continue
    se = pickle.load( open( path+fileName, "rb" ) )
    simulationEnvironmentList.append(se)

Main_populationSize = 10000

resultValuesPandemicDuration = {}
resultValuesPandemicDurationCI = {}
resultValuesQuarantineTime = {}
resultValuesQuarantineTimeCI = {}
resultValuesShareSusceptibleAtEnd = {}
resultValuesShareSusceptibleAtEndCI = {}
resultValuesQuotient = {}
resultValuesQuotientCI = {}
resultValuesShareQuarantineTimeSusceptible = {}
resultValuesQuarantineTimeSusceptible = {}
resultValuesQuarantineTimeSusceptibleCI = {}

for simulationEnvironment in simulationEnvironmentList:
    adoption = simulationEnvironment.contactTracingAdoptionPercentage
    valuePandemicDuration = simulationEnvironment.ci_timeOfPandemic.mean
    valuePandemicDurationCI = simulationEnvironment.ci_timeOfPandemic.halfInterval
    valueQuarantineTime = simulationEnvironment.ci_averageTimeOfQuarantinePerPerson.mean
    valueQuarantineTimeCI = simulationEnvironment.ci_averageTimeOfQuarantinePerPerson.halfInterval
    valueShareSusceptibleAtEnd = 100 * simulationEnvironment.ci_shareOfSusceptiblePeopleAtTheEnd.mean
    valueShareSusceptibleAtEndCI = 100 * simulationEnvironment.ci_shareOfSusceptiblePeopleAtTheEnd.halfInterval
    valueQuotient = 100 * simulationEnvironment.ci_quotient.mean
    valueQuotientCI = 100 * simulationEnvironment.ci_quotient.halfInterval
    valueShareQuarantineTimeSusceptible = 100 * simulationEnvironment.ci_shareDaysSpentInQuarantineOfPeopleSusceptibleByTotalQuarantineDays.mean
    valueQuarantineTimeSusceptible = simulationEnvironment.ci_totalDaysSpentInQuarantineOfPeopleSusceptible.mean / 10000
    valueQuarantineTimeSusceptibleCI = simulationEnvironment.ci_totalDaysSpentInQuarantineOfPeopleSusceptible.halfInterval / 10000
    a = 0

    if(simulationEnvironment.contactTracingOn == False):
        adoption = 0

    if(simulationEnvironment.firstID% 46 < 26):
        resultValuesPandemicDuration.setdefault(adoption, []).append(valuePandemicDuration)
        resultValuesPandemicDurationCI.setdefault(adoption, []).append(valuePandemicDurationCI)
        resultValuesQuarantineTime.setdefault(adoption, []).append(valueQuarantineTime)
        resultValuesQuarantineTimeCI.setdefault(adoption, []).append(valueQuarantineTimeCI)
        resultValuesShareSusceptibleAtEnd.setdefault(adoption, []).append(valueShareSusceptibleAtEnd)
        resultValuesShareSusceptibleAtEndCI.setdefault(adoption, []).append(valueShareSusceptibleAtEndCI)
        resultValuesQuotient.setdefault(adoption, []).append(valueQuotient)
        resultValuesQuotientCI.setdefault(adoption, []).append(valueQuotientCI)
        resultValuesShareQuarantineTimeSusceptible.setdefault(adoption, []).append(valueShareQuarantineTimeSusceptible)
        resultValuesQuarantineTimeSusceptible.setdefault(adoption, []).append(valueQuarantineTimeSusceptible)
        resultValuesQuarantineTimeSusceptibleCI.setdefault(adoption, []).append(valueQuarantineTimeSusceptibleCI)
        
dataPandemicDuration = [resultValuesPandemicDuration[20], resultValuesPandemicDuration[40], resultValuesPandemicDuration[60], resultValuesPandemicDuration[80], resultValuesPandemicDuration[100]]
dataPandemicDurationCI = [resultValuesPandemicDurationCI[20], resultValuesPandemicDurationCI[40], resultValuesPandemicDurationCI[60], resultValuesPandemicDurationCI[80], resultValuesPandemicDurationCI[100]]
dataQuarantineTime = [resultValuesQuarantineTime[20], resultValuesQuarantineTime[40], resultValuesQuarantineTime[60], resultValuesQuarantineTime[80], resultValuesQuarantineTime[100]]
dataQuarantineTimeCI = [resultValuesQuarantineTimeCI[20], resultValuesQuarantineTimeCI[40], resultValuesQuarantineTimeCI[60], resultValuesQuarantineTimeCI[80], resultValuesQuarantineTimeCI[100]]
dataShareSusceptibleAtEnd = [resultValuesShareSusceptibleAtEnd[20], resultValuesShareSusceptibleAtEnd[40], resultValuesShareSusceptibleAtEnd[60], resultValuesShareSusceptibleAtEnd[80], resultValuesShareSusceptibleAtEnd[100]]
dataShareSusceptibleAtEndCI = [resultValuesShareSusceptibleAtEndCI[20], resultValuesShareSusceptibleAtEndCI[40], resultValuesShareSusceptibleAtEndCI[60], resultValuesShareSusceptibleAtEndCI[80], resultValuesShareSusceptibleAtEndCI[100]]
dataQuotient = [resultValuesQuotient[20], resultValuesQuotient[40], resultValuesQuotient[60], resultValuesQuotient[80], resultValuesQuotient[100]]
dataQuotientCI = [resultValuesQuotientCI[20], resultValuesQuotientCI[40], resultValuesQuotientCI[60], resultValuesQuotientCI[80], resultValuesQuotientCI[100]]
dataShareQuarantineTimeSusceptible = [resultValuesShareQuarantineTimeSusceptible[20], resultValuesShareQuarantineTimeSusceptible[40], resultValuesShareQuarantineTimeSusceptible[60], resultValuesShareQuarantineTimeSusceptible[80], resultValuesShareQuarantineTimeSusceptible[100]]
dataQuarantineTimeSusceptible = [resultValuesQuarantineTimeSusceptible[20], resultValuesQuarantineTimeSusceptible[40], resultValuesQuarantineTimeSusceptible[60], resultValuesQuarantineTimeSusceptible[80], resultValuesQuarantineTimeSusceptible[100]]
dataQuarantineTimeSusceptibleCI = [resultValuesQuarantineTimeSusceptibleCI[20], resultValuesQuarantineTimeSusceptibleCI[40], resultValuesQuarantineTimeSusceptibleCI[60], resultValuesQuarantineTimeSusceptibleCI[80], resultValuesQuarantineTimeSusceptibleCI[100]]

rows = 1
cols = 3
numberOfPlotsPerSubsection = 5

Main_populationSize = 10000

fig, axs = plt.subplots(rows, cols, figsize=(15,6))

for simulationEnvironment in simulationEnvironmentList:
    shareList = [100 * x / Main_populationSize for x in simulationEnvironment.averageNumberOfPeopleInfectious]

X = np.linspace(0,2.5,num=5)
bar_width = 0.1
bar_group_distance = 0.11
colorsBase = ['#dd4d4d', '#d6834f', '#eba639', '#87aa66', '#006400']
colorsLight = ['#E67E7E', '#E1A57F', '#F0BE6F', '#A8C190', '#468E46']

[plotRow, plotCol] = [0, 0]
a0=axs[plotCol].bar(-0.15, resultValuesPandemicDuration[0], color = '#000000', width = bar_width, yerr=resultValuesPandemicDurationCI[0], capsize=4)
a1=axs[plotCol].bar(X + 0, dataPandemicDuration[0], color = colorsBase[0], width = bar_width, yerr=dataPandemicDurationCI[0], capsize=4)
a2=axs[plotCol].bar(X + bar_group_distance, dataPandemicDuration[1], color = colorsBase[1], width = bar_width, yerr=dataPandemicDurationCI[1], capsize=4)
a3=axs[plotCol].bar(X + 2 * bar_group_distance, dataPandemicDuration[2], color = colorsBase[2], width = bar_width, yerr=dataPandemicDurationCI[2], capsize=4)
a4=axs[plotCol].bar(X + 3 * bar_group_distance, dataPandemicDuration[3], color = colorsBase[3], width = bar_width, yerr=dataPandemicDurationCI[3], capsize=4)
a5=axs[plotCol].bar(X + 4 * bar_group_distance, dataPandemicDuration[4], color = colorsBase[4], width = bar_width, yerr=dataPandemicDurationCI[4], capsize=4)

axs[plotCol].set_title("A Duration of the epidemic")
axs[plotCol].set_xlabel("Proximity detection range")
axs[plotCol].set_ylabel("Duration of the epidemic, average and 90% CI [days]")
axs[plotCol].set_xticks(X + 2 * bar_group_distance)
axs[plotCol].set_xticklabels(["0.2 m","1 m","2 m","10 m","Site-wide"])
axs[plotCol].legend(labels=['No CT', '20% adoption', '40% adoption', '60% adoption', '80% adoption', '100% adoption'], loc='upper left')

[plotRow, plotCol] = [0, 1]
a0=axs[plotCol].bar(-0.15, resultValuesShareSusceptibleAtEnd[0], color = '#000000', width = bar_width, yerr=resultValuesShareSusceptibleAtEndCI[0], capsize=4)
a1=axs[plotCol].bar(X + 0, dataShareSusceptibleAtEnd[0], color = colorsBase[0], width = bar_width, yerr=dataShareSusceptibleAtEndCI[0], capsize=4)
a2=axs[plotCol].bar(X + bar_group_distance, dataShareSusceptibleAtEnd[1], color = colorsBase[1], width = bar_width, yerr=dataShareSusceptibleAtEndCI[1], capsize=4)
a3=axs[plotCol].bar(X + 2 * bar_group_distance, dataShareSusceptibleAtEnd[2], color = colorsBase[2], width = bar_width, yerr=dataShareSusceptibleAtEndCI[2], capsize=4)
a4=axs[plotCol].bar(X + 3 * bar_group_distance, dataShareSusceptibleAtEnd[3], color = colorsBase[3], width = bar_width, yerr=dataShareSusceptibleAtEndCI[3], capsize=4)
a5=axs[plotCol].bar(X + 4 * bar_group_distance, dataShareSusceptibleAtEnd[4], color = colorsBase[4], width = bar_width, yerr=dataShareSusceptibleAtEndCI[4], capsize=4)

axs[plotCol].set_title("B Susceptible individuals at the end")
axs[plotCol].set_xlabel("Proximity detection range")
axs[plotCol].set_ylabel("Share of susceptible individuals at the end, average and 90% CI [%]")
axs[plotCol].set_xticks(X + 2 * bar_group_distance)
axs[plotCol].set_xticklabels(["0.2 m","1 m","2 m","10 m","Site-wide"])
axs[plotCol].legend(labels=['No CT', '20% adoption', '40% adoption', '60% adoption', '80% adoption', '100% adoption'], loc='upper left')

[plotRow, plotCol] = [0, 2]

a0=axs[plotCol].bar(-0.15, resultValuesQuarantineTime[0], color = '#000000', width = bar_width, yerr=resultValuesQuarantineTimeCI[0], capsize=4)
a1=axs[plotCol].bar(X + 0, np.array(dataQuarantineTime[0]) - np.array(dataQuarantineTimeSusceptible[0]), bottom=dataQuarantineTimeSusceptible[0], color = colorsBase[0], width = bar_width, yerr=dataQuarantineTimeCI[0], capsize=4)
a2=axs[plotCol].bar(X + bar_group_distance, np.array(dataQuarantineTime[1]) - np.array(dataQuarantineTimeSusceptible[1]), bottom=dataQuarantineTimeSusceptible[1], color = colorsBase[1], width = bar_width, yerr=dataQuarantineTimeCI[1], capsize=4)
a3=axs[plotCol].bar(X + 2 * bar_group_distance, np.array(dataQuarantineTime[2]) - np.array(dataQuarantineTimeSusceptible[2]), bottom=dataQuarantineTimeSusceptible[2], color = colorsBase[2], width = bar_width, yerr=dataQuarantineTimeCI[2], capsize=4)
a4=axs[plotCol].bar(X + 3 * bar_group_distance, np.array(dataQuarantineTime[3]) - np.array(dataQuarantineTimeSusceptible[3]), bottom=dataQuarantineTimeSusceptible[3], color = colorsBase[3], width = bar_width, yerr=dataQuarantineTimeCI[3], capsize=4)
a5=axs[plotCol].bar(X + 4 * bar_group_distance, np.array(dataQuarantineTime[4]) - np.array(dataQuarantineTimeSusceptible[4]), bottom=dataQuarantineTimeSusceptible[4], color = colorsBase[4], width = bar_width, yerr=dataQuarantineTimeCI[4], capsize=4)

a1b=axs[plotCol].bar(X + 0, dataQuarantineTimeSusceptible[0], hatch="//", color = colorsLight[0], width = bar_width, yerr=dataQuarantineTimeSusceptibleCI[0], capsize=4, ecolor='blue')
a2b=axs[plotCol].bar(X + bar_group_distance, dataQuarantineTimeSusceptible[1], hatch="//", color = colorsLight[1], width = bar_width, yerr=dataQuarantineTimeSusceptibleCI[1], capsize=4, ecolor='blue')
a3b=axs[plotCol].bar(X + 2 * bar_group_distance, dataQuarantineTimeSusceptible[2], hatch="//", color = colorsLight[2], width = bar_width, yerr=dataQuarantineTimeSusceptibleCI[2], capsize=4, ecolor='blue')
a4b=axs[plotCol].bar(X + 3 * bar_group_distance, dataQuarantineTimeSusceptible[3], hatch="//", color = colorsLight[3], width = bar_width, yerr=dataQuarantineTimeSusceptibleCI[3], capsize=4, ecolor='blue')
a5b=axs[plotCol].bar(X + 4 * bar_group_distance, dataQuarantineTimeSusceptible[4], hatch="//", color = colorsLight[4], width = bar_width, yerr=dataQuarantineTimeSusceptibleCI[4], capsize=4, ecolor='blue')

axs[plotCol].set_title("C Quarantine time")
axs[plotCol].set_xlabel("Proximity detection range")
axs[plotCol].set_ylabel("Time of quarantine per person, average and 90% CI [days]")
axs[plotCol].set_xticks(X + 2 * bar_group_distance)
axs[plotCol].set_xticklabels(["0.2 m","1 m","2 m","10 m","Site-wide"])
axs[plotCol].legend(labels=['No CT', '20% adoption', '40% adoption', '60% adoption', '80% adoption', '100% adoption', '20% adoption, susceptible', '40% adoption, susceptible', '60% adoption, susceptible', '80% adoption, susceptible', '100% adoption, susceptible'], loc='upper left')

fig.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig(path+"/figure_4.png")
plt.show()