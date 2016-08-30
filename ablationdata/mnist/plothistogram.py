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

ablation = np.load(sys.argv[1]).astype(np.float)

print np.max(ablation), np.min(ablation)
pl.hist(ablation.flatten(), bins=50, color='b')

a = pl.gcf().gca()
pl.gcf().savefig(os.path.splitext(os.path.basename(sys.argv[1]))[0]+'_hist.pdf', transparent=True, bbox_inches='tight', pad_inches=0)
pl.gcf().savefig(os.path.splitext(os.path.basename(sys.argv[1]))[0]+'_hist.png', transparent=True, bbox_inches='tight', pad_inches=0)
# pl.show()
