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

# from ewstools_temp import ews_compute
import os

os.makedirs("data/ews", exist_ok=True)
os.makedirs("data/resids", exist_ok=True)


# Import transition data
df = pd.read_csv("data/transition_data.csv")

# Record names
list_records = df["Record"].unique()

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


# Function to do linear interpolation on data prior to transition
def interpolate(df):
    """
    Get data prior to the transition
    Do linear interpolation to make data equally spaced

    Input:
        df: DataFrame with cols ['Age','Proxy','Transition']
    Output:
        df_inter: DataFrame of interpolated data prior to transition.
            Has cols ['Age','Proxy','Transition']

    """

    # Get points prior to transition
    df_prior = df[df["Age"] >= df["Transition"].iloc[0]].copy()

    # Equally spaced time values with same number of points as original record
    t_inter_vals = np.linspace(
        df_prior["Age"].iloc[0], df_prior["Age"].iloc[-1], len(df_prior)
    )
    # Make dataframe for interpolated data
    df_inter = pd.DataFrame({"Age": t_inter_vals, "Inter": True})
    # Concatenate with original, and interpolate
    df2 = pd.concat([df_prior, df_inter]).set_index("Age")
    df2 = df2.interpolate(method="index")

    # Extract just the interpolated data
    df_inter = df2[df2["Inter"] == True][["Proxy", "Transition"]].reset_index()

    return df_inter


# EWS computation parameters
rw = 0.5  # half the length of the data

# Loop through each record
list_df = []
i = 1
for record in list_records:

    # Get record specific data
    df_select = df[df["Record"] == record]
    # Get data prior to transtion and interpolate
    df_inter = interpolate(df_select[["Age", "Proxy", "Transition"]])

    # Make time negative so it increaes up to transition
    df_inter["Age"] = -df_inter["Age"]
    # Series for computing EWS
    series = df_inter.set_index("Age")["Proxy"]

    ts = ewstools.TimeSeries(series)
    ts.detrend(method="Gaussian", bandwidth=dic_bandwidth[record])
    ts.compute_var(rolling_window=rw)
    ts.compute_auto(rolling_window=rw, lag=1)

    df_ews = ts.state.join(ts.ews)
    df_ews["Record"] = record
    df_ews["tsid"] = i
    list_df.append(df_ews)

    i += 1

# Concatenate dataframes
df_ews = pd.concat(list_df)
df_ews.index.name = "Time"

# # Export
df_ews.to_csv("data/ews/df_ews_forced.csv")
