#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sep  26 10:52:43 2020

Compute residauls and EWS for anoxia data

@author: Thomas M. Bury
"""

import numpy as np
import pandas as pd

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go

import ewstools

# Import transition data
df = pd.read_csv('data/data_transitions.csv')

# EWS computation parameters

# span = 100 # span for Lowess filtering
rw = 0.5 # half the length of the data
ews = ['var','ac'] # EWS to compute
lag_times = [1] # lag times for autocorrelation computation (lag of 10 to show decreasing AC where tau=T/2)
span = 0.2
bandwidth = 0.09 # BW used in paper = 900yr = 0.09% of pre-transiiton data (10,000kyr)
smooth = 'Gaussian'

#-------------
# Compute EWS for transition data
#--------------

# Record names

# Loop through each record
list_df = []
list_tsid = df['tsid'].unique()
for tsid in list_tsid:
    
    # Get record specific data up to the transition point
    df_temp = df[(df['tsid']==tsid)]
    df_select = df_temp[
        df_temp['Age [ka BP]']>=df_temp['t_transition_start'].iloc[0]
        ].copy()
    
    # Make time negative so it increaes up to transition
    df_select['Age [ka BP]'] = -df_select['Age [ka BP]']
    # Reverse order of dataframe so transition occurs at the end of the series
    df_select = df_select[::-1]

    
    #------------
    # Compute EWS for Mo
    #------------
    series=df_select.set_index('Age [ka BP]')['Mo [ppm]']
    ews_dic = ewstools.core.ews_compute(series,
                              roll_window = rw,
                              smooth = smooth,
                              upto='Full',
                              span = span,
                              ews = ews,
                              lag_times = lag_times,
                              )
    df_ews = ews_dic['EWS metrics']
    df_ews['tsid'] = tsid
    df_ews['Variable label'] = 'Mo'
    
    # Export residuals for ML
    df_ews[['Residuals']].reset_index().round(6).to_csv('data/resids/resids_anoxia_forced_mo_{}.csv'.format(tsid),index=False)
    
    # Add to list
    list_df.append(df_ews)
    
    
    #------------
    # Compute EWS for U
    #------------
    series=df_select.set_index('Age [ka BP]')['U [ppm]']
    ews_dic = ewstools.core.ews_compute(series,
                              roll_window = rw,
                              smooth = smooth,
                              upto='Full',
                              span = span,
                              ews = ews,
                              lag_times = lag_times,
                              )
    df_ews = ews_dic['EWS metrics']
    df_ews['tsid'] = tsid
    df_ews['Variable label'] = 'U'
    
    # # Export residuals for ML
    # df_ews[['Residuals']].reset_index().to_csv('data/resids_gaussian/resids_anoxia_gaussian_forced_u_{}.csv'.format(tsid),index=False)
    
    # Add to list
    list_df.append(df_ews)    
    
    print('EWS computed for tsid {}'.format(tsid))

# Concatenate dataframes
df_ews = pd.concat(list_df)

# Export ews dataframe
df_ews.to_csv('data/ews/df_ews_forced.csv')




# #------------------
# # Plot of smoothing
# #–-----------------

# # var_plot = 'Mo'
# var_plot = 'Mo'

# # Do plots for Mo
# df_ews = df_ews[df_ews['Variable label']==var_plot]

# fig = make_subplots(
#     rows=4,
#     cols=4,
#     subplot_titles=['tsid = {}'.format(tsid) for tsid in list_tsid],
#     vertical_spacing=0.15,
#     horizontal_spacing=0.15,
#     )
# i=0
# for row in [1,2,3,4]:
#     for col in [1,2,3,4]:
#         try:
#             tsid=list_tsid[i]
#             # Data for plot
#             df_plot = df_ews[df_ews['tsid']==tsid].reset_index()
#             fig.add_trace(
#                 go.Scatter(
#                     x=df_plot['Time'], 
#                     y=df_plot['State variable'],
#                     marker_color='#1f77b4',
#                     ),
#                 row=row, 
#                 col=col
#                 )
#             fig.add_trace(
#                 go.Scatter(
#                     x=df_plot['Time'], 
#                     y=df_plot['Smoothing'],
#                     marker_color='#ff7f0e',
#                     ),
#                 row=row, 
#                 col=col
#                 ) 
#             # Axes labels
#             fig.update_xaxes(title_text='Age (kyr BP)', row=row, col=col)
#             fig.update_yaxes(title_text=var_plot+' (ppm)', row=row, col=col)

#         except:
#             pass
#         i+=1
        
        
# fig.update_layout(height=800, width=800,
#                   showlegend=False,
#                   )

# # fig.write_html('figures/anoxia_smoothing.html')
# fig.write_image('figures/fig_smoothing_{}.png'.format(var_plot),
#                 scale=2,)


# #-----------------
# # Plot of variance
# #–-----------------

# fig = make_subplots(
#     rows=4,
#     cols=4,
#     subplot_titles=['tsid = {}'.format(tsid) for tsid in list_tsid],
#     vertical_spacing=0.15,
#     horizontal_spacing=0.15,
#     )
# i=0
# for row in [1,2,3,4]:
#     for col in [1,2,3,4]:
#         try:
#             tsid=list_tsid[i]
#             # Data for plot
#             df_plot = df_ews[df_ews['tsid']==tsid].reset_index()
#             fig.add_trace(
#                 go.Scatter(
#                     x=df_plot['Time'], 
#                     y=df_plot['Variance'],
#                     marker_color='#1f77b4',
#                     ),
#                 row=row, 
#                 col=col
#                 )
#             # Axes labels
#             fig.update_xaxes(title_text='Age (kyr BP)', row=row, col=col)
#             fig.update_yaxes(title_text='Variance', row=row, col=col)

#         except:
#             pass
#         i+=1
        
        

# fig.update_layout(height=800, width=800,
#                   showlegend=False,
#                   title='Variance for {}'.format(var_plot),
#                   )

# # fig.write_html('figures/dakos_variance.html')
# fig.write_image('figures/fig_var_{}.png'.format(var_plot),
#                 scale=2,)


# #-----------------
# # Plot of lag-1 AC
# #–-----------------

# fig = make_subplots(
#     rows=4,
#     cols=4,
#     subplot_titles=['tsid = {}'.format(tsid) for tsid in list_tsid],
#     vertical_spacing=0.15,
#     horizontal_spacing=0.15,
#     )
# i=0
# for row in [1,2,3,4]:
#     for col in [1,2,3,4]:
#         try:
#             tsid=list_tsid[i]
#             # Data for plot
#             df_plot = df_ews[df_ews['tsid']==tsid].reset_index()
#             fig.add_trace(
#                 go.Scatter(
#                     x=df_plot['Time'], 
#                     y=df_plot['Lag-1 AC'],
#                     marker_color='#1f77b4',
#                     ),
#                 row=row, 
#                 col=col
#                 )
#             # Axes labels
#             fig.update_xaxes(title_text='Age (kyr BP)', row=row, col=col)
#             fig.update_yaxes(title_text='Lag-1 AC', row=row, col=col)

#         except:
#             pass
#         i+=1
        
        
# fig.update_layout(height=800, width=800,
#                   showlegend=False,
#                   title='Lag-1 AC for {}'.format(var_plot)
#                   )

# # fig.write_html('figures/dakos_ac1.html')
# fig.write_image('figures/fig_ac1_{}.png'.format(var_plot),
#                 scale=2,)






