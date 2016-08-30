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
pl.pcolor(ablation, cmap=pl.get_cmap('seismic'), vmin=-np.max(np.abs(ablation)), vmax=np.max(np.abs(ablation)))
# pl.colorbar()
pl.ylim([0, ablation.shape[1]])
pl.xlim([0, ablation.shape[0]])
# pl.yticks(np.arange(0.5, ablation.shape[1]+0.5), range(0,ablation.shape[1]))
# pl.xticks(np.arange(0.5, ablation.shape[0]+0.5), range(0, ablation.shape[0]))
dpi = pl.gcf().dpi
pl.gcf().set_size_inches(ablation.shape[0] / dpi, ablation.shape[1] / dpi)
a = pl.gcf().gca()
a.invert_yaxis()
a.set_frame_on(False)
a.set_xticks([])
a.set_yticks([])
pl.axis('off')
pl.gcf().savefig(os.path.splitext(os.path.basename(sys.argv[1]))[0]+'.pdf', transparent=True, bbox_inches='tight', pad_inches=0)
pl.gcf().savefig(os.path.splitext(os.path.basename(sys.argv[1]))[0]+'.png', transparent=True, bbox_inches='tight', pad_inches=0)
# pl.show()
