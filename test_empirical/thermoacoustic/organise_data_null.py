#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 12:46:55 2020

Organise Sujith thermoacoustic data - control time series

@author: Thomas M. Bury
"""


import numpy as np
import pandas as pd

import glob
import re
import os

import plotly.express as px


# Path to data
path_state = "data/thermo_experiments/quasi_static_experiments/"

# Get volate values for each timeseries
df_voltage = pd.read_csv(
    path_state + "control parameter/voltage_in_volt.txt",
    header=None,
    names=["Voltage (V)"],
)

df_voltage["tsid"] = np.arange(1, 20)
df_voltage.set_index("tsid", inplace=True)


# Labels for each time series
list_labels = np.arange(1, 20)

# Sample frequency
fs = 10


# Collect data around transition, downsampled to 2kHz
list_df = []
for label in list_labels:
    # Read in time series data
    filename = "{}.txt".format(label)

    df_state = pd.read_csv(
        path_state + filename, delimiter="\t", header=0, names=["temp", "pressure"]
    )

    # Convert pressure column measurement in kPa
    df_state["Pressure (kPa)"] = df_state["pressure"] / 0.2175

    # Add a column for time in seconds, given sampling frequency
    time_vals = np.arange(0, len(df_state) / (fs * 1000), 1 / (fs * 1000))
    df_state["Time (s)"] = time_vals

    # Downsample to 2kHz
    df_state_sample = df_state[:: int(fs / 2)].reset_index(drop=True)

    # Add col for tsid
    df_state_sample["tsid"] = label
    # Add col for voltage
    df_state_sample["Voltage (V)"] = df_voltage.loc[label].iloc[0]

    # Drop cols
    df_state_sample.drop(["temp", "pressure"], axis=1, inplace=True)

    list_df.append(df_state_sample)
    print("Data loaded for tsid = {}".format(label))


df_nulls = pd.concat(list_df)


# Export null data
df_nulls.to_csv(
    "data/processed_data/df_nulls.csv",
    index=False,
)
