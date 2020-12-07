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
import pickle
import numpy as np

class ConfidenceInterval:
    def __init__(self,array):
        if(len(array)>0):
            self.mean = sum(array) / len(array)
            self.std = np.std(array)
            self.numberOfSamples = len(array)
            self.halfInterval = 1.645 * self.std / math.sqrt(len(array)) # 90 % confidence intervals
            self.lowerBound = self.mean - self.halfInterval
            self.upperBound = self.mean + self.halfInterval