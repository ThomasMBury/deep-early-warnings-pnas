#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 14:27:12 2021

Compute EWS from residuals for the final 500 points of the 1500-point simulations

@author: Thomas M. Bury
"""

# import python libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import ewstools

os.makedirs("data/ews", exist_ok=True)


# ---------------
# import data
# -------------

# import residual data from 1500-point simulations
columns = ["tsid", "Variable", "Time", "residuals"]
df_resids_forced = pd.read_csv(
    "../cr_hopf_1500/data/ews/df_ews_forced.csv",
    usecols=columns,
).dropna()

df_resids_null = pd.read_csv(
    "../cr_hopf_1500/data/ews/df_ews_null.csv",
    usecols=columns,
).dropna()


# -----------
# compute ews
# -----------

# EWS parameters
dt2 = 1  # spacing between time-series for EWS computation
rw = 0.25  # rolling window
span = 0.2  # bandwidth
# lags = [1] # autocorrelation lag times
# ews = ['var','ac']


# compute ews over final 500 points of residuals - forced trajectories - variable x
df_resids = df_resids_forced[df_resids_forced["Variable"] == "x"]

list_df_ews = []
tsid_vals = df_resids["tsid"].unique()
for tsid in tsid_vals:

    # resids for this tsid - take final 500 points
    df_resids500 = df_resids[df_resids["tsid"] == tsid].iloc[-500:]
    series_resids500 = df_resids500.set_index("Time")["residuals"]

    ts = ewstools.TimeSeries(series_resids500)
    ts.compute_var(rolling_window=rw)
    ts.compute_auto(rolling_window=rw, lag=1)
    df_ews_temp = ts.state.join(ts.ews)

    df_ews_temp["tsid"] = tsid

    # Add DataFrames to list
    list_df_ews.append(df_ews_temp)
    print("Complete for tsid = {}".format(tsid))

# Concatenate EWS DataFrames. Index [Realisation number, Variable, Time]
df_ews = pd.concat(list_df_ews).reset_index().set_index(["tsid", "Time"])

# Change col name to Residuals
df_ews.rename(columns={"state": "residuals"}, inplace=True)

# # Quick plot
# df_ews.loc[2].plot()

# Export EWS data
df_ews.to_csv("data/ews/df_ews_forced.csv")


# compute ews over final 500 points of residuals - null trajectories
df_resids = df_resids_null[df_resids_null["Variable"] == "x"]

list_df_ews = []
tsid_vals = df_resids["tsid"].unique()
for tsid in tsid_vals:

    # resids for this tsid - take final 500 points
    df_resids500 = df_resids[df_resids["tsid"] == tsid].iloc[-500:]
    series_resids500 = df_resids500.set_index("Time")["residuals"]

    ts = ewstools.TimeSeries(series_resids500)
    ts.compute_var(rolling_window=rw)
    ts.compute_auto(rolling_window=rw, lag=1)
    df_ews_temp = ts.state.join(ts.ews)

    df_ews_temp["tsid"] = tsid

    # Add DataFrames to list
    list_df_ews.append(df_ews_temp)
    print("Complete for tsid = {}".format(tsid))

# Concatenate EWS DataFrames. Index [Realisation number, Variable, Time]
df_ews = pd.concat(list_df_ews).reset_index().set_index(["tsid", "Time"])


# Change col name to Residuals
df_ews.rename(columns={"state": "residuals"}, inplace=True)

# # Quick plot
# df_ews.loc[2].plot()

# Export EWS data
df_ews.to_csv("data/ews/df_ews_null.csv")
