#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 16:41:47 2018

@author: Thomas M. Bury

Simulate consumer-resource model
Simulations going through Hopf bifurcation
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

os.makedirs("data/ews", exist_ok=True)


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

# EWS parameters
dt2 = 1  # spacing between time-series for EWS computation
rw = 0.25  # rolling window
span = 0.2  # span for Lowess smoothing
# lags = [1]  # autocorrelation lag times
# ews = ["var", "ac"]

# ----------------------------------
# Simulate many (transient) realisations
# ----------------------------------

# Model (see gellner et al. 2016)


def de_fun_x(x, y, r, k, a, h):
    return r * x * (1 - x / k) - (a * x * y) / (1 + a * h * x)


def de_fun_y(x, y, e, a, h, m):
    return e * a * x * y / (1 + a * h * x) - m * y


# Model parameters
sf = 4  # scale factor
sigma_x = 0.01  # noise intensity
sigma_y = 0.01
r = 1 * sf
k = 1.7
h = 0.6 / sf
e = 0.5
m = 0.5 * sf
al = 3 * sf  # control parameter initial value
ah = 4 * sf  # control parameter final value
abif = 3.923 * sf  # bifurcation point (computed in Mathematica)
x0 = 1  # intial condition (equilibrium value computed in Mathematica)
y0 = 0.412


# initialise DataFrame for each variable to store all realisations
df_sims_x = pd.DataFrame([])
df_sims_y = pd.DataFrame([])

# Initialise arrays to store single time-series data
t = np.arange(t0, tmax, dt)
x = np.zeros(len(t))
y = np.zeros(len(t))

# Set up control parameter a, that increases linearly in time from al to ah
a = pd.Series(np.linspace(al, ah, len(t)), index=t)
# Time at which bifurcation occurs
tcrit = a[a > abif].index[1]

## Implement Euler Maryuyama for stocahstic simulation


# Set seed
np.random.seed(seed)

# Initialise a list to collect trajectories
list_traj_append = []

# loop over simulations
print("\nBegin simulations \n")
for j in range(numSims):

    # Create brownian increments (s.d. sqrt(dt))
    dW_x_burn = np.random.normal(
        loc=0, scale=sigma_x * np.sqrt(dt), size=int(tburn / dt)
    )
    dW_x = np.random.normal(loc=0, scale=sigma_x * np.sqrt(dt), size=len(t))

    dW_y_burn = np.random.normal(
        loc=0, scale=sigma_y * np.sqrt(dt), size=int(tburn / dt)
    )
    dW_y = np.random.normal(loc=0, scale=sigma_y * np.sqrt(dt), size=len(t))

    # Run burn-in period on x0
    for i in range(int(tburn / dt)):
        x0 = x0 + de_fun_x(x0, y0, r, k, a[0], h) * dt + dW_x_burn[i]
        y0 = y0 + de_fun_y(x0, y0, e, a[0], h, m) * dt + dW_y_burn[i]

    # Initial condition post burn-in period
    x[0] = x0
    y[0] = y0

    # Run simulation
    for i in range(len(t) - 1):
        x[i + 1] = x[i] + de_fun_x(x[i], y[i], r, k, a.iloc[i], h) * dt + dW_x[i]
        y[i + 1] = y[i] + de_fun_y(x[i], y[i], e, a.iloc[i], h, m) * dt + dW_y[i]
        # make sure that state variable remains >= 0
        if x[i + 1] < 0:
            x[i + 1] = 0
        if y[i + 1] < 0:
            y[i + 1] = 0

    # Store series data in a temporary DataFrame
    data = {"Realisation number": (j + 1) * np.ones(len(t)), "Time": t, "x": x, "y": y}
    df_temp = pd.DataFrame(data)
    # Append to list
    list_traj_append.append(df_temp)

    print("Simulation " + str(j + 1) + " complete")

#  Concatenate DataFrame from each realisation
df_traj = pd.concat(list_traj_append)
df_traj.set_index(["Realisation number", "Time"], inplace=True)


# ----------------------
# Compute EWS for each simulation in x and y
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
    for var in ["x", "y"]:

        ts = ewstools.TimeSeries(df_traj_filt.loc[i + 1][var], transition=tcrit)
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


# #-------------------------
# # Plots to visualise EWS
# #-------------------------

# # Realisation number to plot
# plot_num = 1
# var = 'x'
# ## Plot of trajectory, smoothing and EWS of var (x or y)
# fig1, axes = plt.subplots(nrows=4, ncols=1, sharex=True, figsize=(6,6))
# df_ews.loc[plot_num,var][['State variable','Smoothing']].plot(ax=axes[0],
#           title='Early warning signals for a single realisation')
# df_ews.loc[plot_num,var]['Residuals'].plot(ax=axes[1],legend=True)
# df_ews.loc[plot_num,var]['Variance'].plot(ax=axes[2],legend=True)
# df_ews.loc[plot_num,var]['Lag-1 AC'].plot(ax=axes[3],legend=True)


# ------------------------------------
## Export data / figures
# -----------------------------------


# Export EWS data
df_ews.to_csv("data/ews/df_ews_forced.csv")

# # Export individual resids files (for Chris)
# for i in np.arange(numSims) + 1:
#     df_resids = df_ews.loc[i, "x"].reset_index()[["Time", "Residuals"]]
#     filepath = "data/resids/cr_hopf_1500_resids_{}.csv".format(i)
#     df_resids.to_csv(filepath, index=False)
