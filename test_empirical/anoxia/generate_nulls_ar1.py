#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 14:50:45 2020

Generate surrogate data for anoxia data using AR(1) process
Compute EWS

@author: Thomas M. Bury
"""

import numpy as np
import pandas as pd

import plotly.express as px

import ewstools

# Set random number seed
np.random.seed(0)

# Import transition data
df = pd.read_csv('data/data_transitions.csv')
list_tsid = df['tsid'].unique()

# Import EWS data (need residuals to genereate null)
df_ews_forced = pd.read_csv('data/ews/df_ews_forced.csv')

# Number of null time series to generate for each record
n_sims = 1


# Initialise list of dfs to store null time series and null EWS
list_df_null=[]
list_df_ews_null=[]


# EWS parameters
rw = 0.5 # half the length of the data
ews = ['var','ac'] # EWS to compute
lag_times = [1] # lag times for autocorrelation computation (lag of 10 to show decreasing AC where tau=T/2)
span = 0.2
bandwidth = 0.09 # BW used in paper = 900yr = 0.09% of pre-transiiton data (10,000kyr)
smooth = 'Gaussian'


# Loop through tsid
for tsid in list_tsid:
    for var_label in ['Mo','U']:
        
        # Get residuals for this tsid
        df_select = df_ews_forced[(df_ews_forced['tsid']==tsid)&\
                                  (df_ews_forced['Variable label']==var_label)
                                  ]
        series_resids = df_select['Residuals']
        
        # Length of resid time series
        l = len(series_resids)
        
        # Compute variance and lag-1 autocorrelation
        # of first 20% of data points
        var = series_resids[:int(len(series_resids)/5)].var()
        print('Var = {}'.format(var))
        ac1 = series_resids[:int(len(series_resids)/5)].autocorr(lag=1)
        print('AC1 = {}'.format(ac1))
        
        # Correspondign AR1 coefficients
        alpha = ac1
        sigma = np.sqrt(var*(1-alpha**2))
        
        
        # Loop through each null simulation number
        for sim_number in np.arange(1,n_sims+1):
            # Generate surrogate time series using AR1 reucrsion relation
            x0 = series_resids.iloc[0] # initial condition
            list_x = [x0]
            
            # Run recursion in time
            x = x0
            for i in np.arange(l-1):
                # Generate noise increment N(0,1)
                epsilon = np.random.normal(loc=0,scale=1)
                x = alpha*x + sigma*epsilon
                list_x.append(x)
                
            # Create pandas series of null data
            series_null = pd.Series(list_x, index=df_select['Time'],name='Null')
        
            # print(span)
            ews_dic = ewstools.core.ews_compute(series_null,
                                      roll_window = 0.5,
                                      smooth = smooth,
                                      upto='Full',
                                      span = span,
                                      band_width=bandwidth,
                                      ews = ews,
                                      lag_times = lag_times,
                                      )
            df_ews_null = ews_dic['EWS metrics']
    
        
            # Export AR1 detrended
            filepath = 'data/resids/resids_anoxia_null_{}_{}.csv'.format(var_label.lower(),tsid)
            df_ews_null['Residuals'].round(6).to_csv(filepath)
            
            
            # Add null trajectory to list
            df_null = series_null.to_frame().reset_index()
            df_null['tsid'] = tsid
            df_null['Variable label']=var_label
            list_df_null.append(df_null)
            
            
            # Add ews trajectory to list
            df_ews_null['tsid'] = tsid
            df_ews_null['Variable label']=var_label
            list_df_ews_null.append(df_ews_null.reset_index())
        

# Concatenate dataframes
df_null = pd.concat(list_df_null)
df_ews_null = pd.concat(list_df_ews_null)


# Export dataframes
df_null.round(6).to_csv('data/nulls/df_null.csv', index=False)
df_ews_null.round(6).to_csv('data/ews/df_ews_null.csv', index=False)



# # Create figure of nulls
# fig = px.line(df_null[df_null['sim_number']==1],
#               y='Null',
#               facet_col='tsid',
#               facet_col_wrap=2,
#               )

# fig.write_html('temp.html')



# # Check out Lowess fit to these AR(1) processes

# # Create figure of Lowess fit to AR(1)
# df_temp = df_ews_null[df_ews_null['Variable label']=='Mo'][['Time','State variable','Smoothing','tsid']]
# df_plot = df_temp.melt(id_vars=['Time','tsid'],
#                         value_vars=['State variable','Smoothing'],
#                         var_name='Variable',
#                         value_name='Value',
#                         ignore_index=False)
# fig = px.line(
#     df_plot,
#     y='Value',
#     color='Variable',
#     facet_col='tsid',
#     facet_col_wrap=4,
#     )

# fig.write_html('temp_smoothing.html')


# # Create figure of Lowess fit to AR(1)
# fig = px.line(
#     df_ews[df_ews['sim_number']==sim_plot],
#     y='Residuals',
#     facet_col='tsid',
#     facet_col_wrap=2,
#     )

# # fig.write_html('temp_residuals.html')


# df_plot = df_temp.melt(id_vars=['Time','tsid'],value_vars=['State variable','Smoothing'],var_name='Variable',value_name='Value')
 

