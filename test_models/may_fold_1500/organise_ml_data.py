#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 10:49:34 2020

Organise ML data output into a single dataframe

@author: Thomas M. Bury
"""


import numpy as np
import pandas as pd

import glob
import re
import os


os.makedirs("data/ml_preds/parsed/", exist_ok=True)

# # length of classifier
# classifier_length=1500
# # Spacing between ML data points
# ml_spacing = int(classifier_length/150)


# # Import EWS data (required for time values of original data)
# df_ews = pd.read_csv('data/ews/df_ews_forced.csv')

# # Get all file names of ML predictions
# all_files = os.listdir('data/ml_preds/')
# all_files = [f for f in all_files if f.split('_')[0]=='ensemble']

# # Get null and forced filenames
# all_files_null = [s for s in all_files if s.find('null')!=-1]
# all_files_forced = [s for s in all_files if s.find('forced')!=-1]

# Import all ML predictions
path = "data/ml_preds/"

# Get all file names of null time series
all_files = glob.glob(path + "*.csv")
# Don't include df files
all_files = [f for f in all_files if f.find("ensemble") != -1]
all_files_null = sorted([f for f in all_files if f.find("null") != -1])
all_files_forced = sorted([f for f in all_files if f.find("null") == -1])


# ----------------
# Organise data for forced trajectories
# -----------------


# Collect ML data for forced trajectories
list_df_ml = []
for filename in all_files_forced:
    print(f"organize for {filename}")
    df = pd.read_csv(
        filename,
    )

    tsid = int(filename.split("_")[-1].split(".")[0])

    # Add info to dataframe
    df["tsid"] = tsid
    df["Variable"] = "x"

    # Append dataframe to list
    list_df_ml.append(df)

# Concatenate dfs
df_ml_forced = pd.concat(list_df_ml)
# sort by type, then latitude
df_ml_forced.sort_values(
    ["Variable", "tsid", "Time"], inplace=True, na_position="first"
)

# # Export ML dataframe
filepath = "data/ml_preds/parsed/"
df_ml_forced.to_csv(filepath + "df_ml_forced.csv", index=False)


# ----------------
# Organise data for null trajectories
# -----------------

# Collect ML data for null trajectories
list_df_ml = []
for filename in all_files_null:
    print(f"organize for {filename}")
    df = pd.read_csv(
        filename,
    )

    tsid = int(filename.split("_")[-1].split(".")[0])

    # Add info to dataframe
    df["tsid"] = tsid
    df["Variable"] = "x"
    # Append dataframe to list
    list_df_ml.append(df)

# Concatenate dfs
df_ml_null = pd.concat(list_df_ml)
# sort by type, then latitude
df_ml_null.sort_values(["Variable", "tsid", "Time"], inplace=True, na_position="first")

# # Export ML dataframe
filepath = "data/ml_preds/parsed/"
df_ml_null.to_csv(filepath + "df_ml_null.csv", index=False)
