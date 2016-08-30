#!/usr/bin/python

import numpy as np
import sys
import os

ablation = np.load(sys.argv[1])
np.savetxt(os.path.splitext(sys.argv[1])[0]+".csv", ablation, delimiter=",")
