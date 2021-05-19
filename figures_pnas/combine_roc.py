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
fileroot = '../figures/ind_roc/'


# #-----------------
# # 8-panel figure for all models and empirical data
# #-----------------

# # Early or late predictions
# timing = 'late'

# list_filenames = ['roc_may_fold_1500_500ml',
#                   'roc_cr_hopf_1500_500ml',
#                   'roc_cr_branch_1500_500ml',
#                   'roc_seirx_x',
#                   'roc_seirx_I',
#                   'roc_anoxia',
#                   'roc_thermo',
#                   'roc_climate',
#                   ]
# list_filenames = [s+'_{}.png'.format(timing) for s in list_filenames]



# list_img = []
# for filename in list_filenames:
#     img = Image.open(fileroot+filename)
#     list_img.append(img)


# # Get heght and width of individual panels
# ind_height = list_img[0].height
# ind_width = list_img[0].width



# # Create frame
# dst = Image.new('RGB',(4*ind_width, 2*ind_height), (255,255,255))

# # Paste in images
# i=0
# for y in np.arange(2)*ind_height:
#     for x in np.arange(4)*ind_width:
#         dst.paste(list_img[i], (x,y))
#         i+=1


# dpi=96*8 # (default dpi) * (scaling factor)
# dst.save('../figures/nature_draft/fig_roc_80_100.png',
#           dpi=(dpi,dpi))




# #-----------------
# # 6-panel figure for eco models at early and late times - using last 500 points
# #-----------------


# list_filenames = ['roc_may_fold_1500_500ml_early',
#                   'roc_cr_hopf_1500_500ml_early',
#                   'roc_cr_branch_1500_500ml_early',
#                   'roc_may_fold_1500_500ml_late',
#                   'roc_cr_hopf_1500_500ml_late',
#                   'roc_cr_branch_1500_500ml_late',
#                   ]

# list_filenames = [s+'.png' for s in list_filenames]


# list_img = []
# for filename in list_filenames:
#     img = Image.open(fileroot+filename)
#     list_img.append(img)


# # Get heght and width of individual panels
# ind_height = list_img[0].height
# ind_width = list_img[0].width



# # Create frame
# dst = Image.new('RGB',(3*ind_width, 2*ind_height), (255,255,255))

# # Paste in images
# i=0
# for y in np.arange(2)*ind_height:
#     for x in np.arange(3)*ind_width:
#         dst.paste(list_img[i], (x,y))
#         i+=1


# dpi=96*8 # (default dpi) * (scaling factor)
# dst.save('../figures/nature_draft/fig_roc_models1500_500ml.png',
#           dpi=(dpi,dpi))







#-----------------
# 6-panel figure for eco models at early and late times - using full 1500 time series
#-----------------


list_filenames = ['roc_may_fold_early',
                  'roc_cr_hopf_early',
                  'roc_cr_branch_early',
                  'roc_may_fold_late',
                  'roc_cr_hopf_late',
                  'roc_cr_branch_late',
                  ]

list_filenames = [s+'.png' for s in list_filenames]


list_img = []
for filename in list_filenames:
    img = Image.open(fileroot+filename)
    list_img.append(img)


# Get heght and width of individual panels
ind_height = list_img[0].height
ind_width = list_img[0].width



# Create frame
dst = Image.new('RGB',(3*ind_width, 2*ind_height), (255,255,255))

# Paste in images
i=0
for y in np.arange(2)*ind_height:
    for x in np.arange(3)*ind_width:
        dst.paste(list_img[i], (x,y))
        i+=1


dpi=96*8 # (default dpi) * (scaling factor)
dst.save('../figures/nature_draft/fig_roc_models1500.png',
          dpi=(dpi,dpi))




