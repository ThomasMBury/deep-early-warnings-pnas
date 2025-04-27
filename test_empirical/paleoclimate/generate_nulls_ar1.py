#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 14:50:45 2020

Generate surrogate data for climate data using AR(1) process
Compute EWS

@author: Thomas M. Bury
"""

import numpy as np
import pandas as pd

import plotly.express as px

import ewstools

# Set random number seed
np.random.seed(0)

rw = 0.5
# Bandwidth sizes for Gaussian kernel (used in Dakos (2008) Table S3)
dic_bandwidth = {
    "End of greenhouse Earth": 25,
    "End of Younger Dryas": 100,
    "End of glaciation I": 25,
    "Bolling-Allerod transition": 25,
    "End of glaciation II": 25,
    "End of glaciation III": 10,
    "End of glaciation IV": 50,
    "Desertification of N. Africa": 10,
}


# Import transition data
df = pd.read_csv("data/transition_data.csv")

# Import ews data
df_ews_forced = pd.read_csv("data/ews/df_ews_forced.csv")
list_tsid = df_ews_forced["tsid"].unique()

# Number of null time series to generate for each record
n_sims = 10

# Initialise list of dfs to store (tsid, sim_number, null)
# list_df=[]
list_df_ews = []


# Loop through tsid
for tsid in list_tsid:

    # Get residuals for this tsid
    df_temp = df_ews_forced[df_ews_forced["tsid"] == tsid]
    series_resids = df_temp["residuals"]

    # Get bandwidth used for this record
    record = df_temp["Record"].iloc[0]
    bandwidth = dic_bandwidth[record]

    # Length of resid time series
    l = len(series_resids)

    # Compute variance and lag-1 autocorrelation of climate residual time series
    # First 20% of data points
    var = series_resids[: int(len(series_resids) / 5)].var()
    print("Var = {}".format(var))
    ac1 = series_resids[: int(len(series_resids) / 5)].autocorr(lag=1)
    print("AC1 = {}".format(ac1))

    # Correspondign AR1 coefficients
    alpha = ac1
    sigma = np.sqrt(var * (1 - alpha**2))

    # Loop through each simulation number
    for null_number in np.arange(1, n_sims + 1):
        # Generate surrogate time series using AR1 reucrsion relation
        x0 = series_resids.iloc[0]  # initial condition
        list_x = [x0]

        # Run recursion in time
        x = x0
        for i in np.arange(l - 1):
            # Generate noise increment N(0,1)
            epsilon = np.random.normal(loc=0, scale=1)
            x = alpha * x + sigma * epsilon
            list_x.append(x)

        # Create pandas series of null data
        series_null = pd.Series(list_x, index=df_temp["Time"], name="Null")

        ts = ewstools.TimeSeries(series_null)
        ts.detrend(method="Gaussian", bandwidth=dic_bandwidth[record])
        ts.compute_var(rolling_window=rw)
        ts.compute_auto(rolling_window=rw, lag=1)

        df_ews = ts.state.join(ts.ews)
        df_ews["Record"] = record

        # # Export resids
        # filepath = "data/resids/resids_ar1_dakos_{}_null_{}.csv".format(
        #     tsid, null_number
        # )
        # df_ews["residuals"].to_csv(filepath)

        # # Add data to DataFrame for storage
        # df_null = series_null.to_frame().reset_index()
        # df_null['tsid'] = tsid
        # df_null['Null number'] = null_number
        # # Append to list
        # list_df.append(df_null)

        df_ews["tsid"] = tsid
        df_ews["Null number"] = null_number
        list_df_ews.append(df_ews)

# Concatenate dataframes
# df_null_trajectories = pd.concat(list_df)
df_ews = pd.concat(list_df_ews)
df_ews.index.name = "Time"

# Export EWS
df_ews.to_csv("data/ews/df_ews_null.csv")
