#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 21:24:53 2021

Combine plots into single png

@author: Thomas M. Bury
"""

import numpy as np
import pandas as pd
   
# Import PIL for image tools
from PIL import Image



#–------------
# Combine plots for forced trajectories
#–--------------

list_img = []
# Import png files in order of increasing RoF
# list_tsid = df_properties.sort_values('rate of forcing (mV/s)')['tsid'].values
# list_tsid_plot = list_tsid[:10]
# list_tsid_plot = list_tsid[10:]

list_tsid = [1,8,7,6,5,2,3]

for tsid in list_tsid:
    img = Image.open('../figures/fig_grid_ind/ind_figs/img_{}.png'.format(tsid))
    list_img.append(img)


# Get heght and width of individlau panels
ind_height = list_img[0].height
ind_width = list_img[0].width

# Creat frame
dst = Image.new('RGB',
                (4*ind_width, 2*ind_height), (255,255,255))

# Pasete in images
dst.paste(list_img[0],(0,0))
dst.paste(list_img[1],(ind_width,0))
dst.paste(list_img[2],(2*ind_width,0))
dst.paste(list_img[3],(3*ind_width,0))
dst.paste(list_img[4],(0,ind_height))
dst.paste(list_img[5],(1*ind_width,ind_height))
dst.paste(list_img[6],(2*ind_width,ind_height))


dst.save('../figures/fig_grid_ind/fig_paleo_forced.png')





#–------------
# Combine plots for null trajectories
#–--------------

list_img = []
# Import png files in order of increasing RoF
# list_tsid = df_properties.sort_values('rate of forcing (mV/s)')['tsid'].values
# list_tsid_plot = list_tsid[:10]
# list_tsid_plot = list_tsid[10:]

list_tsid = [1,8,7,6,5,2,3]

for tsid in list_tsid:
    img = Image.open('../figures/fig_grid_ind/ind_figs_null/img_{}.png'.format(tsid))
    list_img.append(img)


# Get heght and width of individlau panels
ind_height = list_img[0].height
ind_width = list_img[0].width

# Creat frame
dst = Image.new('RGB',
                (4*ind_width, 2*ind_height), (255,255,255))

# Pasete in images
dst.paste(list_img[0],(0,0))
dst.paste(list_img[1],(ind_width,0))
dst.paste(list_img[2],(2*ind_width,0))
dst.paste(list_img[3],(3*ind_width,0))
dst.paste(list_img[4],(0,ind_height))
dst.paste(list_img[5],(1*ind_width,ind_height))
dst.paste(list_img[6],(2*ind_width,ind_height))


dst.save('../figures/fig_grid_ind/fig_paleo_null.png')



