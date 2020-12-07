# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 21:53:05 2020

@author: an7651
"""

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

sys.setrecursionlimit(10000)

class File:
    def __init__(self, fileName, totalPath):
        self.fileName = fileName
        self.totalPath = totalPath

coresPerSimulation = 40
parentFolderFinished = "1"
parentFolderNew = "2"

if not os.path.exists(os.path.join(os.getcwd(), "finishedSimulationStates")):
    os.makedirs(os.path.join(os.getcwd(), "finishedSimulationStates"))

listOfFinishedSimulationStates = []
listOfNotFinishedSimulationStates = []

subFolders = [x[0] for x in os.walk(os.path.join(os.getcwd(), parentFolderFinished))]
del subFolders[0]

for subfolder in subFolders:
    if os.path.exists(os.path.join(subfolder, "SimulationStates")):
        for fileName in [f for f in listdir(os.path.join(subfolder, "SimulationStates")) if isfile(join(os.path.join(subfolder, "SimulationStates"), f))]:
            file = File(fileName,os.path.join(subfolder, "SimulationStates", fileName))
            listOfNotFinishedSimulationStates.append(file)
    if os.path.exists(os.path.join(subfolder, "SimulationStatesFinished")):
        for fileName in [f for f in listdir(os.path.join(subfolder, "SimulationStatesFinished")) if isfile(join(os.path.join(subfolder, "SimulationStatesFinished"), f))]:
            file = File(fileName,os.path.join(subfolder, "SimulationStatesFinished", fileName))
            listOfFinishedSimulationStates.append(file)

numberOfCopiedNotFinishedSimulationStates = 0
currentCopyDirectory = 0

for file in listOfNotFinishedSimulationStates:
    # copy
    if not os.path.exists(os.path.join(os.getcwd(), parentFolderNew,str(currentCopyDirectory),"SimulationStatesToResume")):
        shutil.copytree(os.path.join(os.getcwd(), "baseResume"),os.path.join(os.getcwd(), parentFolderNew,str(currentCopyDirectory)))
        os.makedirs(os.path.join(os.getcwd(), parentFolderNew,str(currentCopyDirectory),"SimulationStatesToResume"))
        
    copyfile(file.totalPath, os.path.join(os.getcwd(), parentFolderNew,str(currentCopyDirectory),"SimulationStatesToResume",file.fileName))

    numberOfCopiedNotFinishedSimulationStates += 1
    if(numberOfCopiedNotFinishedSimulationStates % coresPerSimulation == 0):
        currentCopyDirectory += 1

for file in listOfFinishedSimulationStates:
    copyfile(file.totalPath, os.path.join(os.getcwd(), "finishedSimulationStates",file.fileName))

# now start new Simulations

if(numberOfCopiedNotFinishedSimulationStates > 0):
    print("copied files. now starting simulations")
    numberOfFolders = math.ceil(numberOfCopiedNotFinishedSimulationStates/coresPerSimulation)
    time.sleep(3)
    os.chdir(os.path.join(os.getcwd(), parentFolderNew))
    time.sleep(3)
    parentPath = os.getcwd()

    for i in range(numberOfFolders):
        os.chdir(os.path.join(parentPath, str(i)))
        time.sleep(3)
        #os.system("sbatch -p single --export=ALL,OMP_NUM_THREADS=80 -N 1 -c 40 -t 72:00:00 --mem=300000 job_parallel_resume.sh")
        os.system("sbatch -p gpu_4 --export=ALL,OMP_NUM_THREADS=80 -N 1 -c 40 -t 48:00:00 --mem=300000 job_parallel_resume.sh")
        time.sleep(3)
print("finished")