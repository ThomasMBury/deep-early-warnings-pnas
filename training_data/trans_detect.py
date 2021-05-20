#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 15:38:06 2019

Function to locate transition point in time-series data - 
if no transiiton detected, outputs final point.

@author: tbury
"""


import numpy as np
import ruptures as rpt
from statsmodels.nonparametric.smoothers_lowess import lowess
import pandas as pd


# Function to detect change points
def trans_detect(df_in):
    '''
    Function to detect a change point in a time series
    Input:
        df_in: DataFrame indexed by time, with series data in column 'x'
    Output:
        float: time at which transition occurs
    '''
    # Check for a jump to Nan
    df_nan = df_in[np.isnan(df_in['x'])]
    if df_nan.size == 0:
        # Assign a big value to t_nan
        t_nan = 1e6
    else:
        # First time of Nan
        t_nan = df_nan.iloc[0].name
    
    
    if t_nan > 500:        
        # Detect a jump to another state (in time-series prior to infinity jump)
        
        # First detrend the series (breakpoint detection is not working well with non-stationary data)
        span = 0.2
        series_data = df_in.loc[:t_nan-1]['x']
        smooth_data = lowess(series_data.values, series_data.index.values, frac=span)[:,1]
        # On rare occasion the smoothing function messes up
        # In this case output 0, and run new simulation
        if len(series_data.values) != len(smooth_data):
            return 0
        
        # Compute residuals
        residuals = series_data.values[:len(smooth_data)] - smooth_data
        resid_series = pd.Series(residuals, index=series_data.index)
    
        
        array_traj = resid_series.values.transpose()
        # Window-based change point detection
        model = "l2"
        algo = rpt.Window(width=10, model=model, jump=1, min_size=2).fit(array_traj)
        # Break points - higher penalty means less likely to detect jumps
        bps = algo.predict(pen=1)
        
        t_jump = bps[0]
    else:
        # Assign big value to t_jump
        t_jump = 1e6
    
    # Output minimum of tnan or tjump
    out = min(max(0,t_nan-1),t_jump-1)
    return out
