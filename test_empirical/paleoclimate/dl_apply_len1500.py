#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 24 April, 2025

Get ensemble predictions from len1500 DL classifiers for climate data
Apply to tsid=3 (longer records)

Key:
0 - fold bifurcation
1 - Hopf bifuracation
2 - transcritical bifurcation
3 - null

@author: Thomas M. Bury
"""

# Start timer to record execution time of notebook
import time

start_time = time.time()

import numpy as np

np.random.seed(0)  # Set seed for reproducibility

import pandas as pd
import matplotlib.pyplot as plt
import os

import ewstools

from tensorflow.keras.models import load_model

os.makedirs("data/ml_preds/", exist_ok=True)

# -------------
# Load all len1500 DL classifiers -
# --------------

root_path = "../../dl_train/best_models_tf215/len1500/"
classifier_names = sorted(
    [name[:-6] for name in os.listdir(root_path) if name[-6:] == ".keras"]
)
list_classifiers = []
for classifier_name in classifier_names:
    # Import classifier
    classifier = load_model(root_path + classifier_name + ".keras")
    list_classifiers.append(classifier)


tsid_vals = [3]

# -----------
# Get ensemble predictions for forced residual time series
# ------------
df_ews_forced = pd.read_csv("data/ews/df_ews_forced.csv")
for tsid in tsid_vals:
    print(f"compute dl predictions for tsid={tsid}")
    series = df_ews_forced[(df_ews_forced["tsid"] == tsid)].set_index("Time")[
        "residuals"
    ]
    # apply classifer to last 1500 points prior to transition
    ts = ewstools.TimeSeries(series.iloc[-1500:])
    # space predictions apart by 10 data points (inc must be defined in terms of time)
    dt = series.index[1] - series.index[0]
    inc = dt * 10

    for classifier, classifier_name in zip(list_classifiers, classifier_names):
        ts.apply_classifier_inc(classifier, inc=inc, verbose=0, name=classifier_name)
        print("Predictions complete for classifier {}".format(classifier_name))

    # Get ensemble dl prediction
    dl_preds_mean = ts.dl_preds.groupby("time")[[0, 1, 2, 3]].mean()
    dl_preds_mean.columns = ["fold_prob", "hopf_prob", "branch_prob", "null_prob"]
    dl_preds_mean.index.name = "Time"

    # Export
    dl_preds_mean.to_csv(
        f"data/ml_preds/ensemble_trend_probs_dakos_forced_{tsid}.csv",
    )


# -----------
# Get ensemble predictions for null residual time series
# ------------

df_ews_null = pd.read_csv("data/ews/df_ews_null.csv")
null_numbers = df_ews_null["Null number"].unique()

for tsid in tsid_vals:
    for null_number in null_numbers:
        print(
            f"compute dl predictions for null time seires of tsid={tsid}, null number={null_number}"
        )
        series = df_ews_null[
            (df_ews_null["tsid"] == tsid) & (df_ews_null["Null number"] == null_number)
        ].set_index("Time")["residuals"]
        # apply classifer to last 1500 points prior to transition
        ts = ewstools.TimeSeries(series.iloc[-1500:])
        # space predictions apart by 10 data points (inc must be defined in terms of time)
        dt = series.index[1] - series.index[0]
        inc = dt * 10

        for classifier, classifier_name in zip(list_classifiers, classifier_names):
            ts.apply_classifier_inc(
                classifier, inc=inc, verbose=0, name=classifier_name
            )
            print("Predictions complete for classifier {}".format(classifier_name))

        # Get ensemble dl prediction
        dl_preds_mean = ts.dl_preds.groupby("time")[[0, 1, 2, 3]].mean()
        dl_preds_mean.columns = ["fold_prob", "hopf_prob", "branch_prob", "null_prob"]
        dl_preds_mean.index.name = "Time"

        # Export
        dl_preds_mean.to_csv(
            f"data/ml_preds/ensemble_trend_probs_dakos_null_{tsid}_{null_number}.csv",
        )
