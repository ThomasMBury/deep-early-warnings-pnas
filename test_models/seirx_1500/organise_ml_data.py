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


# Import EWS data (need time values for plot)
df_ews_forced = pd.read_csv('data/ews/df_ews_forced.csv')

# Import all ML predictions
path_I = 'data/ml_preds/Final_SEIRx_I/'
path_x = 'data/ml_preds/Final_SEIRx_x/'

# Get all file names of null time series
all_files = glob.glob(path_I + '*.csv') + glob.glob(path_x+'*.csv')

# Don't include df files
all_files = [file for file in all_files if file.find('ensemble')!=-1]
all_files_null = [s for s in all_files if s.find('null')!=-1]
all_files_forced = [s for s in all_files if s.find('null')==-1]


# 500 or 1500 point classifier used
classifier_length=1500
# Spacing between ML data points
ml_spacing = int(classifier_length/150)


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
    tsid = int(filename_split[-2])
    var_label = filename_split[-5]

    # Add info to dataframe
    df['tsid'] = tsid  
    df['var'] = var_label
    
    # Get time values for this transition
    tVals = df_ews_forced[(df_ews_forced['tsid']==tsid)&\
                          (df_ews_forced['var']==var_label)\
                          ]['Time'].values
    
    
    
    # Take last classifier_length time points of data
    tValsLast = tVals[-classifier_length:]
    # If shorter than classifier_length points, pad with Nan (this is done prior to using ML)
    if len(tValsLast)<classifier_length:
        tValsLast = np.pad(tValsLast, (classifier_length-len(tValsLast),0), constant_values=np.nan)
    # ML time points spacing
    ml_time_vals = tValsLast[::ml_spacing]
    
    # Assign to df
    df['Time']=ml_time_vals    

        
    # Append dataframe to list
    list_df_ml.append(df)


# Concatenate dfs
df_ml_forced = pd.concat(list_df_ml)
# sort by type, then latitude
df_ml_forced.sort_values(['var','tsid', 'Time'],inplace=True,na_position='first')

# # Export ML dataframe
filepath = 'data/ml_preds/'
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
    tsid = int(filename_split[-2])
    var_label = filename_split[-5]

    # Add info to dataframe
    df['tsid'] = tsid  
    df['var'] = var_label
    
    # Get time values for this transition
    tVals = df_ews_forced[(df_ews_forced['tsid']==tsid)&\
                          (df_ews_forced['var']==var_label)\
                          ]['Time'].values
    
    
    
    # Take last classifier_length time points of data
    tValsLast = tVals[-classifier_length:]
    # If shorter than classifier_length points, pad with Nan (this is done prior to using ML)
    if len(tValsLast)<classifier_length:
        tValsLast = np.pad(tValsLast, (classifier_length-len(tValsLast),0), constant_values=np.nan)
    # ML time points spacing
    ml_time_vals = tValsLast[::ml_spacing]
    
    # Assign to df
    df['Time']=ml_time_vals    

        
    # Append dataframe to list
    list_df_ml.append(df)

# Conptenate dfs
df_ml_null = pd.concat(list_df_ml)
# sort by type, then latitude
df_ml_null.sort_values(['var','tsid', 'Time'],inplace=True,na_position='first')

# # Export ML dataframe
filepath = 'data/ml_preds/'
df_ml_null.to_csv(filepath+'df_ml_null.csv', index=False)





