#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 21:24:53 2021

Combine plots into single png

@author: Thomas M. Bury
"""


# Import PIL for image tools
from PIL import Image
import os
import numpy as np


# –------------
# Combine plots for anoxia Mo forced
# –--------------

filepath = "../figures/fig_grid_ind/ind_figs_mo/"

list_img = []
list_tsid = np.arange(1, 14)

for tsid in list_tsid:
    img = Image.open(filepath + "img_{}.png".format(tsid))
    list_img.append(img)


# Get heght and width of individlau panels
ind_height = list_img[0].height
ind_width = list_img[0].width
# Creat frame
dst = Image.new("RGB", (5 * ind_width, 3 * ind_height), (255, 255, 255))

# Pasete in images
dst.paste(list_img[0], (0, 0))
dst.paste(list_img[1], (ind_width, 0))
dst.paste(list_img[2], (2 * ind_width, 0))
dst.paste(list_img[3], (3 * ind_width, 0))
dst.paste(list_img[4], (4 * ind_width, 0))
dst.paste(list_img[5], (0, ind_height))
dst.paste(list_img[6], (ind_width, ind_height))
dst.paste(list_img[7], (2 * ind_width, ind_height))
dst.paste(list_img[8], (3 * ind_width, ind_height))
dst.paste(list_img[9], (4 * ind_width, ind_height))
dst.paste(list_img[10], (0 * ind_width, 2 * ind_height))
dst.paste(list_img[11], (1 * ind_width, 2 * ind_height))
dst.paste(list_img[12], (2 * ind_width, 2 * ind_height))

dst.save(filepath + "../fig_anoxia_mo_forced.png")


# –------------
# Combine plots for anoxia Mo null
# –--------------

filepath = "../figures/fig_grid_ind/ind_figs_mo_null/"

list_img = []
list_tsid = np.arange(1, 14)

for tsid in list_tsid:
    img = Image.open(filepath + "img_{}.png".format(tsid))
    list_img.append(img)


# Get heght and width of individlau panels
ind_height = list_img[0].height
ind_width = list_img[0].width
# Creat frame
dst = Image.new("RGB", (5 * ind_width, 3 * ind_height), (255, 255, 255))

# Pasete in images
dst.paste(list_img[0], (0, 0))
dst.paste(list_img[1], (ind_width, 0))
dst.paste(list_img[2], (2 * ind_width, 0))
dst.paste(list_img[3], (3 * ind_width, 0))
dst.paste(list_img[4], (4 * ind_width, 0))
dst.paste(list_img[5], (0, ind_height))
dst.paste(list_img[6], (ind_width, ind_height))
dst.paste(list_img[7], (2 * ind_width, ind_height))
dst.paste(list_img[8], (3 * ind_width, ind_height))
dst.paste(list_img[9], (4 * ind_width, ind_height))
dst.paste(list_img[10], (0 * ind_width, 2 * ind_height))
dst.paste(list_img[11], (1 * ind_width, 2 * ind_height))
dst.paste(list_img[12], (2 * ind_width, 2 * ind_height))

dst.save(filepath + "../fig_anoxia_mo_null.png")


# –------------
# Combine plots for anoxia U forced
# –--------------

filepath = "../figures/fig_grid_ind/ind_figs_u/"

list_img = []
list_tsid = np.arange(1, 14)

for tsid in list_tsid:
    img = Image.open(filepath + "img_{}.png".format(tsid))
    list_img.append(img)


# Get heght and width of individlau panels
ind_height = list_img[0].height
ind_width = list_img[0].width
# Creat frame
dst = Image.new("RGB", (5 * ind_width, 3 * ind_height), (255, 255, 255))

# Pasete in images
dst.paste(list_img[0], (0, 0))
dst.paste(list_img[1], (ind_width, 0))
dst.paste(list_img[2], (2 * ind_width, 0))
dst.paste(list_img[3], (3 * ind_width, 0))
dst.paste(list_img[4], (4 * ind_width, 0))
dst.paste(list_img[5], (0, ind_height))
dst.paste(list_img[6], (ind_width, ind_height))
dst.paste(list_img[7], (2 * ind_width, ind_height))
dst.paste(list_img[8], (3 * ind_width, ind_height))
dst.paste(list_img[9], (4 * ind_width, ind_height))
dst.paste(list_img[10], (0 * ind_width, 2 * ind_height))
dst.paste(list_img[11], (1 * ind_width, 2 * ind_height))
dst.paste(list_img[12], (2 * ind_width, 2 * ind_height))

dst.save(filepath + "../fig_anoxia_u_forced.png")


# –------------
# Combine plots for anoxia U null
# –--------------

filepath = "../figures/fig_grid_ind/ind_figs_u_null/"

list_img = []
list_tsid = np.arange(1, 14)

for tsid in list_tsid:
    img = Image.open(filepath + "img_{}.png".format(tsid))
    list_img.append(img)


# Get heght and width of individlau panels
ind_height = list_img[0].height
ind_width = list_img[0].width
# Creat frame
dst = Image.new("RGB", (5 * ind_width, 3 * ind_height), (255, 255, 255))

# Pasete in images
dst.paste(list_img[0], (0, 0))
dst.paste(list_img[1], (ind_width, 0))
dst.paste(list_img[2], (2 * ind_width, 0))
dst.paste(list_img[3], (3 * ind_width, 0))
dst.paste(list_img[4], (4 * ind_width, 0))
dst.paste(list_img[5], (0, ind_height))
dst.paste(list_img[6], (ind_width, ind_height))
dst.paste(list_img[7], (2 * ind_width, ind_height))
dst.paste(list_img[8], (3 * ind_width, ind_height))
dst.paste(list_img[9], (4 * ind_width, ind_height))
dst.paste(list_img[10], (0 * ind_width, 2 * ind_height))
dst.paste(list_img[11], (1 * ind_width, 2 * ind_height))
dst.paste(list_img[12], (2 * ind_width, 2 * ind_height))

dst.save(filepath + "../fig_anoxia_u_null.png")
