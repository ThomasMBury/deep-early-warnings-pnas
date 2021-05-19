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


# Info on experiments
df_properties = pd.read_csv('../data/processed_data/df_properties.csv')


#–------------
# Combine plots for thermo forced tsid 1-10
#–--------------

list_img = []
# Import png files in order of increasing RoF
list_tsid = df_properties.sort_values('rate of forcing (mV/s)')['tsid'].values
list_tsid_plot = list_tsid[:10]

for tsid in list_tsid_plot:
    img = Image.open('../figures/fig_grid_ind/ind_figs_forced/img_{}.png'.format(tsid))
    list_img.append(img)


# Get heght and width of individlau panels
ind_height = list_img[0].height
ind_width = list_img[0].width

# Create frame
dst = Image.new('RGB', 
                (5*ind_width, 2*ind_height), (255,255,255))

# Pasete in images
dst.paste(list_img[0],(0,0))
dst.paste(list_img[1],(ind_width,0))
dst.paste(list_img[2],(2*ind_width,0))
dst.paste(list_img[3],(3*ind_width,0))
dst.paste(list_img[4],(4*ind_width,0))
dst.paste(list_img[5],(0,ind_height))
dst.paste(list_img[6],(ind_width,ind_height))
dst.paste(list_img[7],(2*ind_width,ind_height))
dst.paste(list_img[8],(3*ind_width,ind_height))
try:
    dst.paste(list_img[9],(4*ind_width,ind_height))
except:
    pass


dst.save('../figures/fig_grid_ind/fig_thermo_forced_1.png')




#–------------
# Combine plots for thermo forced tsid 11-20
#–--------------

list_img = []
# Import png files in order of increasing RoF
list_tsid = df_properties.sort_values('rate of forcing (mV/s)')['tsid'].values
list_tsid_plot = list_tsid[10:]


for tsid in list_tsid_plot:
    img = Image.open('../figures/fig_grid_ind/ind_figs_forced/img_{}.png'.format(tsid))
    list_img.append(img)


# Get heght and width of individlau panels
ind_height = list_img[0].height
ind_width = list_img[0].width

# Create frame
dst = Image.new('RGB', 
                (5*ind_width, 2*ind_height), (255,255,255))

# Pasete in images
dst.paste(list_img[0],(0,0))
dst.paste(list_img[1],(ind_width,0))
dst.paste(list_img[2],(2*ind_width,0))
dst.paste(list_img[3],(3*ind_width,0))
dst.paste(list_img[4],(4*ind_width,0))
dst.paste(list_img[5],(0,ind_height))
dst.paste(list_img[6],(ind_width,ind_height))
dst.paste(list_img[7],(2*ind_width,ind_height))
dst.paste(list_img[8],(3*ind_width,ind_height))
try:
    dst.paste(list_img[9],(4*ind_width,ind_height))
except:
    pass


dst.save('../figures/fig_grid_ind/fig_thermo_forced_2.png')





#–------------
# Combine plots for thermo null tsid 1-10
#–--------------

# Recall that there are 10 null experiments
# We took two random section of 1500 points to provide 20 nulls.

list_img = []

# # List of tsid for nulls
list_tsid_plot = np.arange(1,11)

for tsid in list_tsid_plot:
    img = Image.open('../figures/fig_grid_ind/ind_figs_null/img_{}.png'.format(tsid))
    list_img.append(img)


# Get heght and width of individlau panels
ind_height = list_img[0].height
ind_width = list_img[0].width

# Create frame
dst = Image.new('RGB', 
                (5*ind_width, 2*ind_height), (255,255,255))

# Pasete in images
dst.paste(list_img[0],(0,0))
dst.paste(list_img[1],(ind_width,0))
dst.paste(list_img[2],(2*ind_width,0))
dst.paste(list_img[3],(3*ind_width,0))
dst.paste(list_img[4],(4*ind_width,0))
dst.paste(list_img[5],(0,ind_height))
dst.paste(list_img[6],(ind_width,ind_height))
dst.paste(list_img[7],(2*ind_width,ind_height))
dst.paste(list_img[8],(3*ind_width,ind_height))
try:
    dst.paste(list_img[9],(4*ind_width,ind_height))
except:
    pass


dst.save('../figures/fig_grid_ind/fig_thermo_null.png')



