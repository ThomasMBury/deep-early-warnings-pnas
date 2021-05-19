#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 16:41:47 2018

@author: Thomas M. Bury

Compute EWS in SEIRX model simulation
"""


# import python libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import ewstools

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go


# import model simulation data
filenames = os.listdir('data/sims_chris/')
filenames = [f for f in filenames if f[:4]=='time']
col_names = ['time','omega','S','E','I','R','x']
list_df = []

for filename in filenames:
    tsid = int(filename[-5])
    if tsid==0:
        tsid=10
    
    forcing = 'forced' if 'forced' in filename else 'null'
    df_temp = pd.read_csv('data/sims_chris/{}'.format(filename),
                          names=col_names)
    df_temp['tsid'] = tsid
    df_temp['forcing'] = forcing
    list_df.append(df_temp)
    
df_traj = pd.concat(list_df)
df_traj.sort_values(['forcing','tsid'], inplace=True)

# Export
df_traj.to_csv('data/sims_chris/df_traj.csv',
               index=False)


# parameters for ews computation
rw = 0.25 # rolling window
span = 0.2 # bandwidth
lags = [1] # autocorrelation lag times
ews = ['var','ac']

# Eyeballed transition time
t_transition = 25


# plot of forced trajectories: x
fig = px.line(df_traj[df_traj['forcing']=='forced'],
              x='time',
              y='x',
              color='tsid')
fig.write_html('figures/traj_forced_x.html')

# plot of forced trajectories: I
fig = px.line(df_traj[df_traj['forcing']=='forced'],
              x='time',
              y='I',
              color='tsid')
fig.write_html('figures/traj_forced_I.html')

# plot of null trajectoreis: x
fig = px.line(df_traj[df_traj['forcing']=='null'],
              x='time',
              y='x',
              color='tsid')
fig.write_html('figures/traj_null_x.html')

# plot of null trajectories: I
fig = px.line(df_traj[df_traj['forcing']=='null'],
              x='time',
              y='I',
              color='tsid')
fig.write_html('figures/traj_null_I.html')



#----------------------
# compute ews for forced trajectories
#---------------------

# initialise list for dataframes
list_df = []

# loop through realisation number
print('\nBegin EWS computation\n')
tsid_vals = df_traj['tsid'].unique()

for tsid in tsid_vals:
    for var in ['x','I']:
        
        # Get 1500 points of data prior to transition
        df_temp = df_traj[(df_traj['tsid']==tsid)&\
                          (df_traj['forcing']=='forced')&\
                          (df_traj['time']<=t_transition)
                          ].iloc[-1500:].set_index('time')
        
        # Make series for ewstools
        series = df_temp[var]
          
        ews_dic = ewstools.core.ews_compute(
                          series,
                          roll_window = rw,
                          smooth='Lowess',
                          span = span,
                          lag_times = lags, 
                          ews = ews,
                          )
        
        # The DataFrame of EWS
        df_ews_temp = ews_dic['EWS metrics']
        # Include a column in the DataFrames for realisation number and variable
        df_ews_temp['tsid'] = tsid
        df_ews_temp['var'] = var
        
        # Export residuals for ML
        df_ews_temp[['Residuals']].reset_index().to_csv('data/resids/resids_seirx_forced_{}_{}.csv'.format(var,tsid),index=False)
                
                
        # Add DataFrames to list
        list_df.append(df_ews_temp)
        
    # Print status every realisation
    print('EWS for tsid '+str(tsid)+' complete')


# Construct EWS dataframe
df_ews_forced = pd.concat(list_df).reset_index()

# export
df_ews_forced.to_csv('data/ews/df_ews_forced.csv',index=False)





#----------------------
# compute ews for null trajectories
#---------------------

# initialise list for dataframes
list_df = []

# loop through realisation number
print('\nBegin EWS computation\n')
tsid_vals = df_traj['tsid'].unique()

for tsid in tsid_vals:
    for var in ['x','I']:
        
        # Get 1500 points of data prior to transition
        df_temp = df_traj[(df_traj['tsid']==tsid)&\
                          (df_traj['forcing']=='null')&\
                          (df_traj['time']<=t_transition)
                          ].iloc[-1500:].set_index('time')
        
        # Make series for ewstools
        series = df_temp[var]
          
        ews_dic = ewstools.core.ews_compute(
                          series,
                          roll_window = rw,
                          smooth='Lowess',
                          span = span,
                          lag_times = lags, 
                          ews = ews,
                          )
        
        # The DataFrame of EWS
        df_ews_temp = ews_dic['EWS metrics']
        # Include a column in the DataFrames for realisation number and variable
        df_ews_temp['tsid'] = tsid
        df_ews_temp['var'] = var
        
        # Export residuals for ML
        df_ews_temp[['Residuals']].reset_index().to_csv('data/resids/resids_seirx_null_{}_{}.csv'.format(var,tsid),index=False)
                           
        # Add DataFrames to list
        list_df.append(df_ews_temp)
        
    # Print status every realisation
    print('EWS for tsid '+str(tsid)+' complete')

# Construct EWS dataframe
df_ews_null = pd.concat(list_df).reset_index()

# export
df_ews_null.to_csv('data/ews/df_ews_null.csv', index=False)






