#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 10:52:43 2020

Compute residauls and EWS in Dakos climate data

@author: Thomas M. Bury
"""

import numpy as np
import pandas as pd

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go

import ewstools


# Import transition data
df = pd.read_csv('data/transition_data.csv')

# Record names
list_records = df['Record'].unique()

# Bandwidth sizes for Gaussian kernel (used in Dakos (2008) Table S3)
dic_bandwidth = {'End of greenhouse Earth':25,
                 'End of Younger Dryas':100,
                 'End of glaciation I':25,
                 'Bolling-Allerod transition':25,
                 'End of glaciation II':25,
                 'End of glaciation III':10,
                 'End of glaciation IV':50,
                 'Desertification of N. Africa':10
                 }


# Function to do linear interpolation on data prior to transition
def interpolate(df):
    '''
    Get data prior to the transition
    Do linear interpolation to make data equally spaced
    
    Input:
        df: DataFrame with cols ['Age','Proxy','Transition']
    Output:
        df_inter: DataFrame of interpolated data prior to transition.
            Has cols ['Age','Proxy','Transition']

    '''
         
    # Get points prior to transition
    df_prior=df[df['Age']>=df['Transition'].iloc[0]].copy()
    
    # Equally spaced time values with same number of points as original record
    t_inter_vals = np.linspace(
        df_prior['Age'].iloc[0],
        df_prior['Age'].iloc[-1],
        len(df_prior)
        )
    # Make dataframe for interpolated data
    df_inter = pd.DataFrame(
        {'Age':t_inter_vals,
         'Inter':True}
        )
    # Concatenate with original, and interpolate
    df2=pd.concat([df_prior,df_inter]).set_index('Age')
    df2=df2.interpolate(method='index')
    
    # Extract just the interpolated data
    df_inter = df2[df2['Inter']==True][['Proxy','Transition']].reset_index()
    
    return df_inter




# EWS computation parameters
# span = 100 # span for Lowess filtering
rw = 0.5 # half the length of the data
ews = ['var','ac'] # EWS to compute
lag_times = [1] # lag times for autocorrelation computation (lag of 10 to show decreasing AC where tau=T/2)


# Loop through each record
list_df = []
i=1
for record in list_records:
    
    # Get record specific data
    df_select = df[df['Record']==record]
    # Get data prior to transtion and interpolate
    df_inter = interpolate(df_select)
        
    # Make time negative so it increaes up to transition
    df_inter['Age'] = -df_inter['Age']
    # Series for computing EWS
    series=df_inter.set_index('Age')['Proxy']
    
    # Compute EWS
    ews_dic = ewstools.core.ews_compute(series,
                              roll_window = rw,
                              smooth = 'Gaussian',
                              upto='Full',
                              band_width=dic_bandwidth[record],
                              ews = ews,
                              lag_times = lag_times
                              )
    df_ews = ews_dic['EWS metrics']
    df_ews['Record'] = record
    df_ews['tsid'] = i
    list_df.append(df_ews)
    
    # Export residuals for ML
    df_ews[['Residuals']].reset_index().to_csv('data/resids/resids_ar1_dakos_{}_forced.csv'.format(i),index=False)
    i+=1


# Concatenate dataframes
df_ews = pd.concat(list_df)

# # Export
df_ews.to_csv('data/ews/df_ews_forced.csv')







# #-----------------
# # Plot of smoothing
# #–-----------------

# id_vals=[1,2,3,4,5,6,7,8]
# fig = make_subplots(
#     rows=4,
#     cols=2,
#     subplot_titles=list_records,
#     vertical_spacing=0.15,
#     horizontal_spacing=0.15,
#     )
# i=0
# for row in [1,2,3,4]:
#     for col in [1,2]:
#         try:
#             record=list_records[i]
#             # Data for plot
#             df_plot = df_ews[df_ews['Record']==record].reset_index()
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
#             fig.update_xaxes(title_text="Years before present", row=row, col=col)
#             fig.update_yaxes(title_text="Climate proxy", row=row, col=col)

#         except:
#             pass
#         i+=1
        
        

# fig.update_layout(height=800, width=800,
#                   showlegend=False,
#                   )

# # fig.write_html('figures/dakos_smoothing.html')
# # fig.write_image('figures/dakos_smoothing.png',
# #                 scale=2,)


# #-----------------
# # Plot of variance
# #–-----------------

# id_vals=[1,2,3,4,5,6,7,8]
# fig = make_subplots(
#     rows=4,
#     cols=2,
#     subplot_titles=list_records,
#     vertical_spacing=0.15,
#     horizontal_spacing=0.15,
#     )
# i=0
# for row in [1,2,3,4]:
#     for col in [1,2]:
#         try:
#             record=list_records[i]
#             # Data for plot
#             df_plot = df_ews[df_ews['Record']==record].reset_index()
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
#             fig.update_xaxes(title_text="Years before present", row=row, col=col)
#             fig.update_yaxes(title_text='Variance', row=row, col=col)

#         except:
#             pass
#         i+=1
        
        

# fig.update_layout(height=800, width=800,
#                   showlegend=False,
#                   )

# # fig.write_html('figures/dakos_variance.html')
# # fig.write_image('figures/dakos_variance.png',
# #                 scale=2,)



# #-----------------
# # Plot of lag-1 AC
# #–-----------------

# id_vals=[1,2,3,4,5,6,7,8]
# fig = make_subplots(
#     rows=4,
#     cols=2,
#     subplot_titles=list_records,
#     vertical_spacing=0.15,
#     horizontal_spacing=0.15,
#     )
# i=0
# for row in [1,2,3,4]:
#     for col in [1,2]:
#         try:
#             record=list_records[i]
#             # Data for plot
#             df_plot = df_ews[df_ews['Record']==record].reset_index()
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
#             fig.update_xaxes(title_text="Years before present", row=row, col=col)
#             fig.update_yaxes(title_text='Lag-1 AC', row=row, col=col)

#         except:
#             pass
#         i+=1
        
        
# fig.update_layout(height=800, width=800,
#                   showlegend=False,
#                   )

# # fig.write_html('figures/dakos_ac1.html')
# # fig.write_image('figures/dakos_ac1.png',
# #                 scale=2,)










