#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 19:29:10 2019

@author: tbury


Script to compute residual dyanmics and EWS for each simulation

"""

import numpy as np
import pandas as pd

import ewstools
import os
import sys


bif_total = int(sys.argv[1])
batch_num = int(sys.argv[2])


# Create directories for output
if not os.path.exists('output_resids'):
    os.makedirs('output_resids')
#if not os.path.exists('output_var'):
#    os.makedirs('output_var')
#if not os.path.exists('output_ac1'):
#    os.makedirs('output_ac1')
#if not os.path.exists('output_skew'):
#    os.makedirs('output_skew')



# Loop thorugh each time-series and compute EWS

# Counter
i = (batch_num-1)*(4*bif_total) + 1
# While the file exists
while os.path.isfile('output_sims/tseries'+str(i)+'.csv'):
    df_traj = pd.read_csv('output_sims/tseries'+str(i)+'.csv')
    
    # Compute EWS
    dic_ews = ewstools.core.ews_compute(df_traj['x'],
                                        smooth = 'Lowess',
                                        band_width = 0.1,
                                        span = 0.2,
                                        roll_window = 0.4,
                                        lag_times=[1],
                                        ews=[])
    df_ews = dic_ews['EWS metrics']
    
    # Collect dfs for each EWS
    df_resids = df_ews[['Residuals']]
#    df_var = df_ews[['Variance']]
#    df_ac1 = df_ews[['Lag-1 AC']]
#    df_skew = df_ews[['Skewness']]
    
    
    # Output residual time-series
    df_resids.to_csv('output_resids/resids'+str(i)+'.csv')
#    df_var.to_csv('output_var/var'+str(i)+'.csv')
#    df_ac1.to_csv('output_ac1/ac'+str(i)+'.csv')
#    df_skew.to_csv('output_skew/skew'+str(i)+'.csv')
    
    if np.mod(i,100) == 0:
        print('EWS for trajectory {} complete'.format(i))
        
    # Increment
    i+=1

















