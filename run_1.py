# -*- coding: utf-8 -*-

import time as tm
import sys
import time
import math
import shutil
import os
import time

sys.setrecursionlimit(10000)

numberOfSimulations = 30*46
coresPerSimulation = 40

numberOfFolders = math.ceil(numberOfSimulations/coresPerSimulation)

if not os.path.exists(os.path.join(os.getcwd(), "1")):
    os.makedirs(os.path.join(os.getcwd(), "1"))

for i in range(numberOfFolders):
    shutil.copytree(os.path.join(os.getcwd(), "baseInitial"),os.path.join(os.getcwd(), "1",str(i)))
    text_file = open(os.path.join(os.getcwd(), "1",str(i))+"/computeStartPosition.txt", "w")
    text_file.write(str(i*coresPerSimulation))
    text_file.close()

os.chdir(os.path.join(os.getcwd(), "1"))

time.sleep(1)

parentPath = os.getcwd()

for i in range(numberOfFolders):
    os.chdir(os.path.join(parentPath, str(i)))
    time.sleep(1)
    os.system("sbatch -p single --export=ALL,OMP_NUM_THREADS=80 -N 1 -c 40 -t 72:00:00 --mem=20000 job_parallel_initial.sh")
    #os.system("sbatch -p gpu_8 --export=ALL,OMP_NUM_THREADS=80 -N 1 -c 40 -t 48:00:00 --mem=20000 job_parallel_initial.sh")
    time.sleep(1)
