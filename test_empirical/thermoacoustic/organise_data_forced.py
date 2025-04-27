#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 12:46:55 2020

Parse Sujith thermoacoustic data

@author: Thomas M. Bury
"""

import numpy as np
import pandas as pd

import glob
import re
import os

import plotly.express as px


# Import transition time series
path_bifparam = (
    "data/thermo_experiments/Rate dependent transitions/Control_parameter_variation/"
)
path_state = "data/thermo_experiments/Rate dependent transitions/pressure data/"


# all_files_bifparam = os.listdir(path_bifparam)
all_files_state = os.listdir(path_state)


# ------------
# Create dataframe for properties of each transition time series
# -------------

# Labels for each transition
list_labels = np.arange(1, 20)

# List of tuples (tsid, rate of forcing (mV/s), sample frequency (kHz), final time (s))
list_tup = [
    (1, 40, 10, 60),
    (2, 2, 4, 1200),
    (3, 4, 4, 600),
    (4, 5, 10, 480),
    (5, 10, 10, 240),
    (6, 20, 10, 120),
    (7, 30, 10, 80),
    (8, 60, 10, 40),
    (9, 80, 10, 30),
    (10, 120, 10, 20),
    (11, 240, 10, 15),
    (12, 480, 10, 10),
    (13, 800, 10, 8),
    (14, 1200, 10, 7),
    (15, 2400, 10, 6),
    (16, 4800, 10, 5),
    (17, 24000, 10, 5),
    (18, 2, 4, 1200),
    (19, 3, 4, 800),
]

df_properties = pd.DataFrame(
    {
        "tsid": [tup[0] for tup in list_tup],
        "rate of forcing (mV/s)": [tup[1] for tup in list_tup],
        "sample frequency (kHz)": [tup[2] for tup in list_tup],
        "final time (s)": [tup[3] for tup in list_tup],
    }
).set_index("tsid")

# Export
df_properties.to_csv("data/processed_data/df_properties.csv")


# List of transition times (eyeballed)
list_trans_times = [
    43.5,
    830.0,
    413.0,
    328.0,
    167.0,
    86.0,
    58.5,
    31.5,
    24.5,
    17.7,
    10.2,
    6.7,
    5.0,
    4.3,
    3.7,
    3.4,
    3.3,
    830.0,
    555.0,
]

df_trans_times = pd.DataFrame(
    {"tsid": np.arange(1, 20), "transition time (s)": list_trans_times}
).set_index("tsid")


# Collect data around transition, downsampled to 2kHz
list_df = []
for label in list_labels:
    # Read in transition data
    filename_state = "{}.txt".format(label)

    df_state = pd.read_csv(
        path_state + filename_state,
        header=0,
        names=["Time (s)", "Pressure"],
        delimiter="\t",
    )

    # Convert pressure column measurement in kPa
    df_state["Pressure (kPa)"] = df_state["Pressure"] / 0.2175

    # Add a column for time in seconds, given sampling frequency
    fs = df_properties.loc[label]["sample frequency (kHz)"]
    time_vals = np.arange(0, len(df_state) / (fs * 1000), 1 / (fs * 1000))
    df_state["Time (s)"] = time_vals

    # Downsample to a sample frequency of 2kHz
    df_state_sample = df_state[:: int(fs / 2)].reset_index(drop=True)

    # Get data 3000 points prior to transition and 1500 points after

    # Find index at which transtion time occurs
    trans_time = df_trans_times.loc[label]["transition time (s)"]
    idx_trans = df_state_sample[df_state_sample["Time (s)"] <= trans_time].index[-1]

    df_keep = df_state_sample.iloc[(idx_trans - 3000) : (idx_trans + 1500)].copy()

    # Add col for tsid and transition time
    df_keep["tsid"] = label
    df_keep["transition time (s)"] = trans_time

    # Drop Pressure col without units
    df_keep.drop(["Pressure"], axis=1, inplace=True)

    list_df.append(df_keep)
    print("Data loaded for tsid = {}".format(label))


df_transitions = pd.concat(list_df)


# Export transition data
df_transitions.to_csv(
    "data/processed_data/df_transitions.csv",
    index=False,
)
