#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 18:29:22 2014

@author: yani
"""

import numpy as np
import os
import sys
import matplotlib

matplotlib.use('Agg')
import pylab as pl

maxstd = 0
minstd = 0

ablation = []
for fname in sys.argv[1:]:
    ablation.append(np.load(fname).astype(np.float).flatten())
    maxstd = max(maxstd, np.std(ablation[-1]))

pl.hist(ablation, bins=30, normed=True)
#pl.xlim([-0.1,3*maxstd])
pl.gca().set_xscale("log")

pl.gcf().savefig('hist.pdf', transparent=True, bbox_inches='tight', pad_inches=0)
pl.gcf().savefig('hist.png', transparent=True, bbox_inches='tight', pad_inches=0)
# pl.show()
