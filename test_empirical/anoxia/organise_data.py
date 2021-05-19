#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 10:40:22 2020

Organise anoxia data into transition sections (Hennekam et al. 2020)

@author: Thomas M. Bury
"""


import numpy as np
import pandas as pd

# Raw data (excel file)
xls = pd.ExcelFile('data/data_anoxia.xlsx')

# Columns of dataset to keep
cols = ['Age [ka BP]','Mo [ppm]','U [ppm]']

# Import each sheet individually (different cores)
df_ms21 = pd.read_excel(xls, 'XRF-CS MS21', usecols=cols)
df_ms66 = pd.read_excel(xls, 'XRF-CS MS66', usecols=cols)
df_64pe = pd.read_excel(xls, 'XRF-CS 64PE406E1', usecols=cols)


# Get transition data from Hennekam et al. 2020 Figure 3
# Tuple of form (ID, tmin, t_transition_end, t_transition_start, tmax)
list_tup = [
    ('S1', 8,     9.7,     10.5,     20.5),
    ('S3', 83.7,  85.1,    85.8,     95.8),
    ('S4', 106.0, 107.2,   107.8,    117.8),
    ('S5', 125.0, 127.5,   128.35,   138.35),
    ('S6', 175.0, 176.5,   177.25,   187.25),
    ('S7', 195.0, 197.8,   198.5,    208.5),
    ('S8', 222.0, 223.6,   224.9,    234.9),
    ('S9', 238.0, 239.6,   240.3,    250.3),
]

df_transition_loc = pd.DataFrame(
    {'ID':[tup[0] for tup in list_tup],
     'tmin':[tup[1] for tup in list_tup],
     't_transition_end':[tup[2] for tup in list_tup],
     't_transition_start':[tup[3] for tup in list_tup],
     'tmax':[tup[4] for tup in list_tup]
     })

#--------------------
# For each transition, extract data
#---------------------

id_vals = df_transition_loc['ID'].values

# Transition ID values analysed for each core
id_vals_ms21 = ['S1','S3']
id_vals_ms66 = ['S1','S3','S4','S5']
id_vals_64pe = ['S3','S4','S5','S6','S7','S8','S9']


list_df = []

# Counter to create a tsid for each transition time series
# (13 in total for each variable, U and Mo)

count_tsid=1

for id_val in id_vals:
    
    # Get data for transition ID
    df_temp = df_transition_loc[df_transition_loc['ID']==id_val]
    tmin = df_temp['tmin'].iloc[0]
    tmax = df_temp['tmax'].iloc[0]
    t_transition_start = df_temp['t_transition_start'].iloc[0]
    t_transition_end = df_temp['t_transition_end'].iloc[0]
    
    # Extract time series data within bounds for each core if used
    
    # MS21
    if id_val in id_vals_ms21:
        
        df_extract = df_ms21[(df_ms21['Age [ka BP]']>=tmin)&\
                               (df_ms21['Age [ka BP]']<=tmax)].copy()
        df_extract['ID'] = id_val
        df_extract['Core'] = 'MS21'
        df_extract['t_transition_start'] = t_transition_start
        df_extract['t_transition_end'] = t_transition_end
        df_extract['tsid'] = count_tsid
        count_tsid+=1
        # Append data to list
        list_df.append(df_extract)
        
    # MS66
    if id_val in id_vals_ms66:
        
        df_extract = df_ms66[(df_ms66['Age [ka BP]']>=tmin)&\
                               (df_ms66['Age [ka BP]']<=tmax)].copy()
        df_extract['ID'] = id_val
        df_extract['Core'] = 'MS66'
        df_extract['t_transition_start'] = t_transition_start
        df_extract['t_transition_end'] = t_transition_end
        df_extract['tsid'] = count_tsid
        count_tsid+=1
        # Append data to list
        list_df.append(df_extract)

    # 64PE
    if id_val in id_vals_64pe:
        
        df_extract = df_64pe[(df_64pe['Age [ka BP]']>=tmin)&\
                               (df_64pe['Age [ka BP]']<=tmax)].copy()
        df_extract['ID'] = id_val
        df_extract['Core'] = '64PE'
        df_extract['t_transition_start'] = t_transition_start
        df_extract['t_transition_end'] = t_transition_end
        df_extract['tsid'] = count_tsid
        count_tsid+=1
        # Append data to list
        list_df.append(df_extract)

df_transition_data = pd.concat(list_df, ignore_index=True)

# Export transition data
df_transition_data.to_csv('data/data_transitions.csv',
                          index=False)



