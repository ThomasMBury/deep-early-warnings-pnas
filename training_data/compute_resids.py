#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 19:29:10 2019

@author: tbury

Compute residual dynamics from Lowess smoothing for each time series
generated for training data

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

# Loop through each time-series and compute residuals

# Counter
i = (batch_num-1)*(4*bif_total) + 1
# While the file exists
while os.path.isfile('output_sims/tseries'+str(i)+'.csv'):
    df_traj = pd.read_csv('output_sims/tseries'+str(i)+'.csv')
    
    # Compute EWS
    dic_ews = ewstools.core.ews_compute(df_traj['x'],
                                        smooth = 'Lowess',
                                        span = 0.2,
                                        ews=[])
    df_ews = dic_ews['EWS metrics']
    df_resids = df_ews[['Residuals']]
    
    # Output residual time-series
    df_resids.to_csv('output_resids/resids'+str(i)+'.csv')
    
    if np.mod(i,100) == 0:
        print('Residuals for trajectory {} complete'.format(i))
        
    # Increment
    i+=1
