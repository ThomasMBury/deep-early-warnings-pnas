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
df = pd.read_csv("data/data_transitions.csv")

# EWS computation parameters
rw = 0.5  # half the length of the data
bandwidth = 0.2

# -------------
# Compute EWS for transition data
# --------------

# Loop through each record
list_df = []
list_tsid = df["tsid"].unique()
for tsid in list_tsid:

    # Get record specific data up to the transition point
    df_temp = df[(df["tsid"] == tsid)]
    df_select = df_temp[
        df_temp["Age [ka BP]"] >= df_temp["t_transition_start"].iloc[0]
    ].copy()

    # Make time negative so it increaes up to transition
    df_select["Age [ka BP]"] = -df_select["Age [ka BP]"]
    # Reverse order of dataframe so transition occurs at the end of the series
    df_select = df_select[::-1]

    # ------------
    # Compute EWS for Mo
    # ------------
    series = df_select.set_index("Age [ka BP]")["Mo [ppm]"]
    ts = ewstools.TimeSeries(series)
    ts.detrend(method="Gaussian", bandwidth=bandwidth)
    ts.compute_var(rolling_window=rw)
    ts.compute_auto(rolling_window=rw, lag=1)

    df_ews = ts.state.join(ts.ews)
    df_ews["tsid"] = tsid
    df_ews["Variable label"] = "Mo"

    # Export residuals for ML
    ts.state[["residuals"]].reset_index().round(6).to_csv(
        "data/resids/resids_anoxia_forced_mo_{}.csv".format(tsid), index=False
    )

    # Add to list
    list_df.append(df_ews)

    # ------------
    # Compute EWS for U
    # ------------

    series = df_select.set_index("Age [ka BP]")["U [ppm]"]
    ts = ewstools.TimeSeries(series)
    ts.detrend(method="Gaussian", bandwidth=bandwidth)
    ts.compute_var(rolling_window=rw)
    ts.compute_auto(rolling_window=rw, lag=1)

    df_ews = ts.state.join(ts.ews)
    df_ews["tsid"] = tsid
    df_ews["Variable label"] = "U"

    # Export residuals for ML
    ts.state[["residuals"]].reset_index().round(6).to_csv(
        "data/resids/resids_anoxia_forced_u_{}.csv".format(tsid), index=False
    )

    # Add to list
    list_df.append(df_ews)

    print("EWS computed for tsid {}".format(tsid))

# Concatenate dataframes
df_ews = pd.concat(list_df)

# Export ews dataframe
df_ews.to_csv("data/ews/df_ews_forced.csv")
