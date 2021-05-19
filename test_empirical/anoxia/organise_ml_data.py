#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 10:49:34 2020

Organise ML data output into a single dataframe

@author: Thomas M. Bury
"""


import numpy as np
import pandas as pd

import glob
import re
import os



# Make export directory if doens't exist
try:
    os.mkdir('data/ml_preds/parsed/')
except:
    print('Path already exists')
    

# Import EWS data (need time values for plot)
df_ews_forced = pd.read_csv('data/ews/df_ews_forced.csv')

# Import all ML predictions
path = 'data/ml_preds/'

# Get all file names of null time series
all_files = glob.glob(path + '*.csv')
# Don't include df files
all_files = [file for file in all_files if file.find('ensemble')!=-1]
all_files_null = [s for s in all_files if s.find('null')!=-1]
all_files_forced = [s for s in all_files if s.find('null')==-1]


#----------------
# Organise data for forced trajectories
#-----------------

# Collect ML data for forced trajectories
list_df_ml = []
for filename in all_files_forced:
    df = pd.read_csv(filename, 
                     header = None,
                     names = ['fold_prob','hopf_prob','branch_prob','null_prob','bif_prob'])
    
    filename_split = re.split('_',filename)
    tsid = int(filename_split[-3])
    var_label = filename_split[-4]

    # Add info to dataframe
    df['tsid'] = tsid  
    df['Variable label'] = var_label.capitalize()
    
    # Get time values for this transition
    tVals = df_ews_forced[(df_ews_forced['tsid']==tsid)&\
                          (df_ews_forced['Variable label']==var_label.capitalize())\
                          ]['Time'].values
    
    # Get ML time points
    # 500 point classifier used
    # Take last 500 time points of data
    # Take every other 10 (we have 50 ML points)
    tVals500 = tVals[-500:]
    # If shorter than 500 points, pad with Nan
    if len(tVals500)<500:
        tVals500 = np.pad(tVals500, (500-len(tVals500),0), constant_values=np.nan)
    # ML time points are spaced 10 apart
    ml_time_vals = tVals500[::10]

    # 30 time series points per ML data point
    df['Time']=ml_time_vals
        
    # Append dataframe to list
    list_df_ml.append(df)


# Concatenate dfs
df_ml_forced = pd.concat(list_df_ml)
# sort by type, then latitude
df_ml_forced.sort_values(['Variable label','tsid', 'Time'],inplace=True,na_position='first')

# # Export ML dataframe
filepath = 'data/ml_preds/parsed/'
df_ml_forced.to_csv(filepath+'df_ml_forced.csv', index=False)





#----------------
# Organise data for null trajectories
#-----------------

# Collect ML data for null trajectories
list_df_ml = []
for filename in all_files_null:
    df = pd.read_csv(filename, 
                      header = None,
                      names = ['fold_prob','hopf_prob','branch_prob','null_prob','bif_prob'])
    
    
    filename_split = re.split('_',filename)
    tsid = int(filename_split[-3])
    var_label = filename_split[-4]
    
    
    # Add info to dataframe
    df['tsid'] = tsid  
    df['Variable label'] = var_label.capitalize()
   
    
    # Get time values for this transition
    tVals = df_ews_forced[(df_ews_forced['tsid']==tsid)&\
                          (df_ews_forced['Variable label']==var_label.capitalize())\
                          ]['Time'].values
     
    # Get ML time points
    # 500 point classifier used
    # Take last 500 time points of data
    # Take every other 10 (we have 50 ML points)
    tVals500 = tVals[-500:]
    # If shorter than 500 points, pad with Nan
    if len(tVals500)<500:
        tVals500 = np.pad(tVals500, (500-len(tVals500),0), constant_values=np.nan)
    # ML time points are spaced 10 apart
    ml_time_vals = tVals500[::10]

    # 30 time series points per ML data point
    df['Time']=ml_time_vals
        
    # Append dataframe to list
    list_df_ml.append(df)


# Concatenate dfs
df_ml_null = pd.concat(list_df_ml)
# sort by type, then latitude
df_ml_null.sort_values(['Variable label','tsid', 'Time'],inplace=True,na_position='first')

# # Export ML dataframe
filepath = 'data/ml_preds/parsed/'
df_ml_null.to_csv(filepath+'df_ml_null.csv', index=False)






