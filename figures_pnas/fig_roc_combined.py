#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 21:24:53 2021

Combine individual ROC plots into a single grid, and export to png

@author: tbury
"""


# Import PIL for image tools
from PIL import Image

import numpy as np

# Fileroot to images
fileroot = 'figures/roc_individual/'


#-----------------
# Fig 2 of manuscript: 8-panel figure for all models and empirical data
#-----------------

# Early or late predictions
timing = 'late'

list_filenames = ['roc_may_fold_500',
                  'roc_cr_hopf_500',
                  'roc_cr_trans_500',
                  'roc_seirx_x',
                  'roc_seirx_I',
                  'roc_anoxia',
                  'roc_thermo',
                  'roc_climate',
                  ]
list_filenames = [s+'_{}.png'.format(timing) for s in list_filenames]



list_img = []
for filename in list_filenames:
    img = Image.open(fileroot+filename)
    list_img.append(img)


# Get heght and width of individual panels
ind_height = list_img[0].height
ind_width = list_img[0].width



# Create frame
dst = Image.new('RGB',(4*ind_width, 2*ind_height), (255,255,255))

# Paste in images
i=0
for y in np.arange(2)*ind_height:
    for x in np.arange(4)*ind_width:
        dst.paste(list_img[i], (x,y))
        i+=1


dpi=96*8 # (default dpi) * (scaling factor)
dst.save('figures/fig_roc_80_100.png',
          dpi=(dpi,dpi))








#-----------------
# Supp. fig 11 : 8-panel figure for all models and empirical data - early predictions
#-----------------

# Early or late predictions
timing = 'early'

list_filenames = ['roc_may_fold_500',
                  'roc_cr_hopf_500',
                  'roc_cr_trans_500',
                  'roc_seirx_x',
                  'roc_seirx_I',
                  'roc_anoxia',
                  'roc_thermo',
                  'roc_climate',
                  ]
list_filenames = [s+'_{}.png'.format(timing) for s in list_filenames]



list_img = []
for filename in list_filenames:
    img = Image.open(fileroot+filename)
    list_img.append(img)


# Get heght and width of individual panels
ind_height = list_img[0].height
ind_width = list_img[0].width



# Create frame
dst = Image.new('RGB',(4*ind_width, 2*ind_height), (255,255,255))

# Paste in images
i=0
for y in np.arange(2)*ind_height:
    for x in np.arange(4)*ind_width:
        dst.paste(list_img[i], (x,y))
        i+=1


dpi=96*8 # (default dpi) * (scaling factor)
dst.save('figures/fig_roc_60_80.png',
          dpi=(dpi,dpi))






