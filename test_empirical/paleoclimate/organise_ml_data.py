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


# # ML model number
# ml_number = "Protocol3_Jan21_len500"


# 500 or 1500 point classifier used
# classifier_length = 500
# Spacing between ML data points
# ml_spacing = int(classifier_length / 50)

os.makedirs("data/ml_preds/parsed/", exist_ok=True)


# # Import EWS data (need time values for plot)
# df_ews = pd.read_csv("data/ews/df_ews_forced.csv")

# Import all ML predictions
path = "data/ml_preds/"

# Get all file names
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

    # Append dataframe to list
    list_df_ml.append(df)

# Concatenate dfs
df_ml_forced = pd.concat(list_df_ml)
# sort by type, then latitude
df_ml_forced.sort_values(["tsid", "Time"], inplace=True, na_position="first")

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

    tsid = int(filename.split("_")[-2])
    null_number = int(filename.split("_")[-1].split(".")[0])

    # Add info to dataframe
    df["tsid"] = tsid
    df["Null number"] = null_number
    # Append dataframe to list
    list_df_ml.append(df)

# Concatenate dfs
df_ml_null = pd.concat(list_df_ml)
# sort by type, then latitude
df_ml_null.sort_values(
    ["tsid", "Null number", "Time"], inplace=True, na_position="first"
)

# # Export ML dataframe
filepath = "data/ml_preds/parsed/"
df_ml_null.to_csv(filepath + "df_ml_null.csv", index=False)


# ------


# # ---------------
# # Organise forced trajectory data into df
# # -----------------

# # Collect ML data for forced trajectories
# list_df_ml = []
# for filename in all_files_forced:
#     df = pd.read_csv(
#         filename,
#         header=None,
#         names=["fold_prob", "hopf_prob", "branch_prob", "null_prob", "bif_prob"],
#     )

#     filename_split = filename.split("_")
#     tsid = int(filename_split[-3])

#     # Add info to dataframe
#     df["tsid"] = tsid
#     # Get name of record
#     record = df_ews[df_ews["tsid"] == tsid]["Record"].iloc[0]
#     df["Record"] = record

#     # Get time values for this transition
#     tVals = df_ews[df_ews["tsid"] == tsid]["Time"].values

#     # Take last classifier_length time points
#     tValsLast = tVals[-classifier_length:]
#     # If shorter than classifier_length points, pad with Nan (this is done prior to using ML)
#     if len(tValsLast) < classifier_length:
#         tValsLast = np.pad(
#             tValsLast, (classifier_length - len(tValsLast), 0), constant_values=np.nan
#         )
#     # ML time points spacing
#     ml_time_vals = tValsLast[::ml_spacing]

#     # Assign to df
#     df["Age"] = ml_time_vals

#     # Append dataframe to list
#     list_df_ml.append(df)


# # Concatenate dfs
# df_ml_forced = pd.concat(list_df_ml)
# # sort by type, then latitude
# df_ml_forced.sort_values(["tsid", "Age"], inplace=True, na_position="first")

# # Export ML dataframe
# df_ml_forced.to_csv(
#     "data/ml_preds/model_{}/parsed/df_ml_forced.csv".format(ml_number), index=False
# )


# # ---------------
# # Organise null trajectory data into df
# # -----------------

# # Collect ML data for null trajectories
# list_df_ml = []
# for filename in all_files_null:
#     df = pd.read_csv(
#         filename,
#         header=None,
#         names=["fold_prob", "hopf_prob", "branch_prob", "null_prob", "bif_prob"],
#     )

#     filename_split = filename.split("_")
#     tsid = int(filename_split[-5])
#     null_number = int(filename_split[-3])

#     # Add info to dataframe
#     df["tsid"] = tsid
#     # Get name of record
#     record = df_ews[df_ews["tsid"] == tsid]["Record"].iloc[0]
#     df["Record"] = record
#     # Add info on null sim number
#     df["Null number"] = null_number

#     # Get time values for this transition
#     tVals = df_ews[df_ews["tsid"] == tsid]["Time"].values

#     # Take last classifier_length time points
#     tValsLast = tVals[-classifier_length:]
#     # If shorter than classifier_length points, pad with Nan (this is done prior to using ML)
#     if len(tValsLast) < classifier_length:
#         tValsLast = np.pad(
#             tValsLast, (classifier_length - len(tValsLast), 0), constant_values=np.nan
#         )
#     # ML time points spacing
#     ml_time_vals = tValsLast[::ml_spacing]

#     # 30 time series points per ML data point
#     df["Age"] = ml_time_vals

#     # Append dataframe to list
#     list_df_ml.append(df)


# # Concatenate dfs
# df_ml_null = pd.concat(list_df_ml)
# # sort by type, then latitude
# df_ml_null.sort_values(
#     ["tsid", "Null number", "Age"], inplace=True, na_position="first"
# )

# # Export ML dataframe
# df_ml_null.to_csv(
#     "data/ml_preds/model_{}/parsed/df_ml_null.csv".format(ml_number), index=False
# )
