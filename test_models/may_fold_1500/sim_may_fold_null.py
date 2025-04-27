#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 16:41:47 2018

@author: Thomas M. Bury

Simulate May's harvesting model
Null simulations
Compute EWS

"""

# import python libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import ewstools

np.random.seed(0)


# --------------------------------
# Global parameters
# –-----------------------------


# Simulation parameters
dt = 0.01
t0 = 0
tmax = 1500
tburn = 100  # burn-in period
numSims = 10
seed = 0  # random number generation seed
sigma = 0.01  # noise intensity

# EWS parameters
dt2 = 1  # spacing between time-series for EWS computation
rw = 0.25  # rolling window
span = 0.2  # bandwidth


# ----------------------------------
# Simulate many (transient) realisations
# ----------------------------------


# Model
def de_fun(x, r, k, h, s):
    return r * x * (1 - x / k) - h * (x**2 / (s**2 + x**2))


# Model parameters
r = 1  # growth rate
k = 1  # carrying capacity
s = 0.1  # half-saturation constant of harvesting function
bl = 0.15  # bifurcation parameter low
bh = 0.15  # bifurcation parameter high
# bcrit = 0.260437 # bifurcation point (computed in Mathematica)
x0 = 0.8197  # intial condition (equilibrium value computed in Mathematica)


# Initialise arrays to store single time-series data
t = np.arange(t0, tmax, dt)
x = np.zeros(len(t))

# Set bifurcation parameter b, that increases linearly in time from bl to bh
b = pd.Series(np.linspace(bl, bh, len(t)), index=t)
# Time at which bifurcation occurs (it doesn't here as null sim)
# tcrit = b[b > bcrit].index[1]

## Implement Euler Maryuyama for stocahstic simulation

# Set seed
np.random.seed(seed)

# Initialise a list to collect trajectories
list_traj_append = []

# loop over simulations
print("\nBegin simulations \n")
for j in range(numSims):

    # Create brownian increments (s.d. sqrt(dt))
    dW_burn = np.random.normal(loc=0, scale=sigma * np.sqrt(dt), size=int(tburn / dt))
    dW = np.random.normal(loc=0, scale=sigma * np.sqrt(dt), size=len(t))

    # Run burn-in period on x0
    for i in range(int(tburn / dt)):
        x0 = x0 + de_fun(x0, r, k, b[0], s) * dt + dW_burn[i]

    # Initial condition post burn-in period
    x[0] = x0

    # Run simulation
    for i in range(len(t) - 1):
        x[i + 1] = x[i] + de_fun(x[i], r, k, b.iloc[i], s) * dt + dW[i]
        # make sure that state variable remains >= 0
        if x[i + 1] < 0:
            x[i + 1] = 0

    # Store series data in a temporary DataFrame
    data = {"tsid": (j + 1) * np.ones(len(t)), "Time": t, "x": x}
    df_temp = pd.DataFrame(data)
    # Append to list
    list_traj_append.append(df_temp)

    print("Simulation " + str(j + 1) + " complete")

#  Concatenate DataFrame from each realisation
df_traj = pd.concat(list_traj_append)
df_traj.set_index(["tsid", "Time"], inplace=True)


# ----------------------
# Compute EWS for each simulation
# ---------------------

# Filter time-series to have time-spacing dt2
df_traj_filt = df_traj.loc[:: int(dt2 / dt)]

# set up a list to store output dataframes from ews_compute- we will concatenate them at the end
appended_ews = []
appended_pspec = []

# loop through realisation number
print("\nBegin EWS computation\n")
for i in range(numSims):
    # loop through variable
    for var in ["x"]:

        ts = ewstools.TimeSeries(df_traj_filt.loc[i + 1][var])
        ts.detrend(method="Lowess", span=span)
        ts.compute_var(rolling_window=rw)
        ts.compute_auto(rolling_window=rw, lag=1)
        df_ews_temp = ts.state.join(ts.ews)

        # Include a column in the DataFrames for realisation number and variable
        df_ews_temp["tsid"] = i + 1
        df_ews_temp["Variable"] = var

        # Add DataFrames to list
        appended_ews.append(df_ews_temp)

    # Print status every realisation
    if np.remainder(i + 1, 1) == 0:
        print("EWS for realisation " + str(i + 1) + " complete")


# Concatenate EWS DataFrames. Index [Realisation number, Variable, Time]
df_ews = pd.concat(appended_ews).reset_index().set_index(["tsid", "Variable", "Time"])


# Export EWS data
df_ews.to_csv("data/ews/df_ews_null.csv")
