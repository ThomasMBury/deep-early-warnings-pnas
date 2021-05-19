#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 10:49:34 2020

Organise ML data output into a single dataframe

@author: Thomas M. Bury
"""


import numpy as np
import pandas as pd

import os


# length of classifier
classifier_length=1500
# Spacing between ML data points
ml_spacing = int(classifier_length/150)

# Import EWS data for variable x (required for time values of original data)
df_ews = pd.read_csv('data/ews/df_ews_forced.csv')
df_ews = df_ews[df_ews['Variable']=='x']


# Get all file names of ML predictions
all_files = os.listdir('data/ml_preds/')
all_files = [f for f in all_files if f.split('_')[0]=='ensemble']

# Get null and forced filenames
all_files_null = [s for s in all_files if s.find('null')!=-1]
all_files_forced = [s for s in all_files if s.find('forced')!=-1]



#----------------
# Organise data for forced trajectories
#-----------------

list_df_ml = []
for filename in all_files_forced:
    df = pd.read_csv('data/ml_preds/{}'.format(filename), 
                     header = None,
                     names = ['fold_prob','hopf_prob','branch_prob','null_prob','bif_prob'])
    
    # Get tsid from filename
    filename_split = filename.split('_')
    tsid = int(filename_split[-2])
    df['tsid'] = tsid
    
    
    # Get time values up to the transition point
    tVals = df_ews[(df_ews['tsid']==tsid)][['Time','Residuals']].dropna()['Time'].values
     
    # Take last 'classifier_length' time points of data
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
df_ml = pd.concat(list_df_ml)
# sort by type, then latitude
df_ml.sort_values(['tsid','Time'],inplace=True)

# Export ML dataframe
df_ml.to_csv('data/ml_preds/df_ml_forced.csv', index=False)





#----------------
# Organise data for null trajectories
#-----------------

list_df_ml = []
for filename in all_files_null:
    df = pd.read_csv('data/ml_preds/{}'.format(filename), 
                     header = None,
                     names = ['fold_prob','hopf_prob','branch_prob','null_prob','bif_prob'])
    
    # Get tsid from filename
    filename_split = filename.split('_')
    tsid = int(filename_split[-2])
    df['tsid'] = tsid
    
    
    # Get time values for this transition
    tVals = df_ews[(df_ews['tsid']==tsid)]['Time'].values
    
    # Take last 'classifier_length' time points of data
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
df_ml = pd.concat(list_df_ml)
# sort by type, then latitude
df_ml.sort_values(['tsid','Time'],inplace=True)

# Export ML dataframe
df_ml.to_csv('data/ml_preds/df_ml_null.csv', index=False)



