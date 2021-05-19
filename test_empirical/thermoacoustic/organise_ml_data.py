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


# ML model number
ml_number = 'protocol3'
# 500 or 1500 point classifier used
classifier_length=1500
# Spacing between ML data points
ml_spacing = int(classifier_length/150)


# Make export directory if doens't exist
try:
    os.mkdir('data/ml_preds/{}/parsed/'.format(ml_number))
except:
    print('Path already exists')



# Import EWS data (need time values for plot)
df_ews_forced = pd.read_csv('data/ews/df_ews_forced.csv')
df_ews_null = pd.read_csv('data/ews/df_ews_null.csv')


# Import all ML predictions
path = 'data/ml_preds/{}/'.format(ml_number)


# Get all filenames of data
all_files = glob.glob(path + '*.csv')
all_files_null = [s for s in all_files if s.find('null')!=-1]
all_files_forced = [s for s in all_files if s.find('null')==-1]


#--------------
# Organise forced trajecotry data
#---------------

# Collect ML data for forced trajectories
list_df_ml = []
for filename in all_files_forced:
    df = pd.read_csv(filename, 
                     header = None,
                     names = ['fold_prob','hopf_prob','branch_prob','null_prob','bif_prob'])
    
    # Get tsid from filename
    filename_split = re.split('_', filename)
    
    tsid = int(filename.split('_')[-2])
    # Add info to dataframe
    df['tsid'] = tsid  

    # Get time values for this transition
    tVals = df_ews_forced[df_ews_forced['tsid']==tsid]['Time'].values
    

    # Take last classifier_length time points of data spaced 10 apart
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
df_ml_forced.sort_values(['tsid','Time'],inplace=True,na_position='first')

# Export ML dataframe
df_ml_forced.to_csv('data/ml_preds/{}/parsed/df_ml_forced.csv'.format(ml_number), 
                    index=False)



#--------------
# Organise null trajecotry data
#---------------

# Collect ML data for null trajectories
list_df_ml = []
for filename in all_files_null:
    df = pd.read_csv(filename, 
                     header = None,
                     names = ['fold_prob','hopf_prob','branch_prob','null_prob','bif_prob'])
    
    filename_split = re.split('_', filename)
    
    tsid = int(filename_split[-2])
    null_number = int(filename_split[-3])
    # Add info to dataframe
    df['tsid'] = tsid  
    # Add info on null sim number
    df['Null number'] = null_number
    
    # Get time values for this transition
    tVals = df_ews_null[(df_ews_null['tsid']==tsid)&\
                        (df_ews_null['Null number']==null_number)]['Time'].values

    # Take last classifier_length time points of data spaced 10 apart
    tValsLast = tVals[-classifier_length:]
    # If shorter than classifier_length points, pad with Nan (this is done prior to using ML)
    if len(tValsLast)<classifier_length:
        tValsLast = np.pad(tValsLast, (classifier_length-len(tValsLast),0), constant_values=np.nan)
    # ML time points are spaced 10 apart
    ml_time_vals = tValsLast[::ml_spacing]
    
    # Assign to df
    df['Time']=ml_time_vals         
    
    # Append dataframe to list
    list_df_ml.append(df)


# Concatenate dfs
df_ml_null = pd.concat(list_df_ml)
# sort by type, then latitude
df_ml_null.sort_values(['tsid','Null number','Time'],inplace=True,
                       na_position='first')


# Export ML dataframe
df_ml_null.to_csv('data/ml_preds/{}/parsed/df_ml_null.csv'.format(ml_number), 
                  index=False)







