# -*- coding: utf-8 -*-

import time as tm
import sys
import time
import math
import shutil
import os
import time

sys.setrecursionlimit(10000)

idInitial = 0

IDs = []

for i in range(0,60):
    IDs.append(idInitial + i)

for id in IDs:
    time.sleep(1)
    os.system(f"scancel {id}")
    print(f"cancelled {id}")
