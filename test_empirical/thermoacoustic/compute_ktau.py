#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 13:27:44 2020

Compute rolling ktau values from EWS dataframe

@author: Thomas M. Bury
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn.metrics as metrics
import scipy.stats as stats


# Length of ML classifier
classifier_length = 1500
ml_spacing = int(classifier_length/50)

# Import EWS from forced thermoacoustic transitions
df_ews_forced = pd.read_csv('data/ews/df_ews_forced.csv')
df_ews_forced.set_index(['tsid','Time'], inplace=True)

# Import EWS from null Dakos climate transitions
df_ews_null = pd.read_csv('data/ews/df_ews_null.csv')
df_ews_null.set_index(['tsid','Null number','Time'], inplace=True)


# Function to compute kendall tau for time seires data up to point t_fin
def ktau_compute(series,t_fin):
    # selected data in series where from point where measured variable
    # is defined, up to t_fin
    t_start=series[pd.notnull(series)].index[1]
    
    series_reduced = series.loc[t_start:t_fin]
    x1 = series_reduced.index.values
    x2 = series_reduced.values
    ktau, pval = stats.kendalltau(x1,x2)
    return ktau

# Compute kendall tau values along time series at points with fixed spacing
def ktau_series(series, spacing=ml_spacing):
    tVals = series.index[::spacing]
    ktauVals = []
    for t in tVals:
        ktau = ktau_compute(series,t)
        ktauVals.append(ktau)
    
    # Return series
    ktauSeries = pd.Series(ktauVals,index=tVals)
    return ktauSeries



#-------------
# Compute kendall tau for forced simulations
#------------

# Store list of dfs with kendall tau values from each simulation
list_df = []

# Loop through each time series ID
tsid_vals = df_ews_forced.index.unique(level='tsid')
for tsid in tsid_vals:

    series_var = df_ews_forced.loc[tsid]['Variance']
    series_ac = df_ews_forced.loc[tsid]['Lag-1 AC']
    
    # Compute kendall tau series
    series_ktau_var = ktau_series(series_var)
    series_ktau_var.name = 'ktau_variance'
    series_ktau_ac = ktau_series(series_ac)
    series_ktau_ac.name = 'ktau_ac'

    
    # Put into temporary dataframe
    df_temp = pd.concat([series_ktau_var, series_ktau_ac], axis=1).reset_index()
    df_temp['tsid'] = tsid
    list_df.append(df_temp)
    print('K tau done for tsid {}'.format(tsid))
        

# Concatenate kendall tau dataframes
df_ktau_forced = pd.concat(list_df).set_index(['tsid','Time'])

# Export dataframe
df_ktau_forced.to_csv('data/ews/df_ktau_forced.csv')




#-------------
# Compute kendall tau for null simulations
#------------

# Store list of dfs with kendall tau values from each simulation
list_df = []


tsid_vals = df_ews_null.index.unique(level='tsid')
null_number_vals = df_ews_null.index.unique(level='Null number')
# Loop through each time series ID
for tsid in tsid_vals:
    for null_number in null_number_vals:
    
        series_var = df_ews_null.loc[tsid, null_number]['Variance']
        series_ac = df_ews_null.loc[tsid, null_number]['Lag-1 AC']
        
        # Compute kendall tau series
        series_ktau_var = ktau_series(series_var)
        series_ktau_var.name = 'ktau_variance'
        series_ktau_ac = ktau_series(series_ac)
        series_ktau_ac.name = 'ktau_ac'
    
        
        # Put into temporary dataframe
        df_temp = pd.concat([series_ktau_var, series_ktau_ac], axis=1).reset_index()
        df_temp['tsid'] = tsid
        df_temp['Null number'] = null_number
        list_df.append(df_temp)
        print('K tau done for tsid {}'.format(tsid))
            

# Concatenate kendall tau dataframes
df_ktau_null = pd.concat(list_df).set_index(['tsid','Null number','Time'])

# Export dataframe
df_ktau_null.to_csv('data/ews/df_ktau_null.csv')












