#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 10:52:43 2020

Compute residauls and EWS for thermoacoustic data

@author: Thomas M. Bury
"""

import numpy as np
import pandas as pd

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go

import ewstools

import os

os.makedirs("data/resids", exist_ok=True)
os.makedirs("data/ews", exist_ok=True)


# Set seed
seed = 0
np.random.seed(seed)

# Import transition data
df = pd.read_csv("data/processed_data/df_transitions.csv")

# Import null data
df_nulls = pd.read_csv("data/processed_data/df_nulls.csv")

# Classifier length of ML
classifier_length = 1500

# EWS computation parameters
rw = 0.5  # half the length of the data
span = 0.2  # total points (0.2*1500).


# -------------
# Compute EWS for transition data
# --------------

# Record names
list_tsid = df["tsid"].unique()


# Loop through each record
list_df = []
for tsid in list_tsid:

    # Get record specific data
    df_select = df[df["tsid"] == tsid].reset_index(drop=True)

    # Get classifier_length points prior to transition
    time_trans = df_select["transition time (s)"].iloc[0]
    idx_trans = df_select[df_select["Time (s)"] <= time_trans].index[-1]
    df_prior = df_select.iloc[idx_trans - classifier_length : idx_trans]

    # Series for computing EWS
    series = df_prior.set_index("Time (s)")["Pressure (kPa)"]

    # Compute EWS
    ts = ewstools.TimeSeries(series)
    ts.detrend(method="Lowess", span=span)
    ts.compute_var(rolling_window=rw)
    ts.compute_auto(rolling_window=rw, lag=1)

    df_ews = ts.state.join(ts.ews)
    df_ews["tsid"] = tsid
    list_df.append(df_ews)

    print("EWS computed for tsid {}".format(tsid))

# Concatenate dataframes
df_ews = pd.concat(list_df)

# Export
df_ews.to_csv("data/ews/df_ews_forced.csv")


# -------------
# Compute EWS for null data
# --------------

# Only use IDs 1-10 since the rest are already at the limit cycle.
list_tsid = np.arange(1, 11)
# Loop through each record
list_df = []
for tsid in list_tsid:

    # Get record specific data
    df_select = df_nulls[df_nulls["tsid"] == tsid].reset_index(drop=True)

    # Create two segements from each null time series (20 in total)
    for i in [1, 2]:

        # Select a region of 1500 (or 500) points at random
        idx_start = np.random.choice(np.arange(len(df_select) - classifier_length))

        df_select1500 = df_select.iloc[idx_start : idx_start + classifier_length]

        # Series for computing EWS
        series = df_select1500.set_index("Time (s)")["Pressure (kPa)"]

        # Compute EWS
        ts = ewstools.TimeSeries(series)
        ts.detrend(method="Lowess", span=span)
        ts.compute_var(rolling_window=rw)
        ts.compute_auto(rolling_window=rw, lag=1)

        df_ews = ts.state.join(ts.ews)
        df_ews["tsid"] = tsid
        df_ews["Null number"] = i
        list_df.append(df_ews)

    print("EWS computed for null tsid {}".format(tsid))

# Concatenate dataframes
df_ews_null = pd.concat(list_df)

# Export
df_ews_null.to_csv("data/ews/df_ews_null.csv")
