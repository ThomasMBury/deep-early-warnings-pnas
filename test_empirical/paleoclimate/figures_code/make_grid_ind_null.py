#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 19:39:06 2021

Make a grid figure of an individual NULL trajectory
Panels for trajectory, lag-1 AC, variance, DL prediction

@author: Thomas M. Bury
"""

import numpy as np
import pandas as pd


import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Null number to plot
null_number = 2

# Import trajectory data
df_traj = pd.read_csv("../data/transition_data.csv")
# Make time negative
df_traj["Time"] = -df_traj["Age"]
# (Just need this data here for the climate proxy names)


# Import EWS data
df_ews = pd.read_csv("../data/ews/df_ews_null.csv")
df_ews = df_ews[df_ews["Null number"] == null_number]

# Import ML prediction data
df_ml = pd.read_csv("../data/ml_preds/parsed/df_ml_null.csv")
df_ml = df_ml[df_ml["Null number"] == null_number]


# Colour scheme
# cols = px.colors.qualitative.D3 # blue, orange, green, red, purple, brown
cols = (
    px.colors.qualitative.Plotly
)  # blue, red, green, purple, orange, cyan, pink, light green
col_grays = px.colors.sequential.gray

dic_colours = {
    "state": "gray",
    "smoothing": col_grays[2],
    "dl_bif": cols[0],
    "variance": cols[1],
    "ac": cols[2],
    "dl_fold": cols[3],
    "dl_hopf": cols[4],
    "dl_branch": cols[5],
    "dl_null": "black",
}


def make_grid_figure(tsid, letter_label, title):

    # ---------------
    # Build figure
    # --------------

    fig = make_subplots(
        rows=4,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0,
    )

    # ----------------
    # Panel 1: Trajectory of null (no transition)
    # ------------------
    df_plot = df_ews[df_ews["tsid"] == tsid]

    fig.add_trace(
        go.Scatter(
            x=df_plot["Time"],
            y=df_plot["state"],
            marker_color=dic_colours["state"],
            showlegend=False,
            line={"width": 1.2},
        ),
        row=1,
        col=1,
    )

    # Add trace for smoothing
    fig.add_trace(
        go.Scatter(
            x=df_plot["Time"],
            y=df_plot["smoothing"],
            marker_color=dic_colours["smoothing"],
            showlegend=False,
            line={"width": 1.2},
        ),
        row=1,
        col=1,
    )

    # -------------------
    # Panel 2: Lag-1 AC
    # --------------------

    fig.add_trace(
        go.Scatter(
            x=df_plot["Time"],
            y=df_plot["ac1"],
            marker_color=dic_colours["ac"],
            showlegend=False,
            line={"width": 1.2},
        ),
        row=2,
        col=1,
    )

    # -------------------
    # Panel 3: Variance
    # --------------------

    fig.add_trace(
        go.Scatter(
            x=df_plot["Time"],
            y=df_plot["variance"],
            marker_color=dic_colours["variance"],
            showlegend=False,
            line={"width": 1.2},
        ),
        row=3,
        col=1,
    )

    # -------------------
    # Panel 4: DL weights
    # --------------------

    df_plot = df_ml[df_ml["tsid"] == tsid]

    # # Weight for any bif
    # fig.add_trace(
    #     go.Scatter(x=df_plot['Time'],
    #        y=df_plot['bif_prob'],
    #         marker_color=dic_colours['dl_bif'],
    #         showlegend=False,
    #         line={'width':1.2},
    #        ),
    #     row=4,col=1,
    #     )

    # Weight for hopf bif
    fig.add_trace(
        go.Scatter(
            x=df_plot["Time"],
            y=df_plot["hopf_prob"],
            marker_color=dic_colours["dl_hopf"],
            showlegend=False,
            line={"width": 1.2},
        ),
        row=4,
        col=1,
    )

    # Weight for branch bif
    fig.add_trace(
        go.Scatter(
            x=df_plot["Time"],
            y=df_plot["branch_prob"],
            marker_color=dic_colours["dl_branch"],
            showlegend=False,
            line={"width": 1.2},
        ),
        row=4,
        col=1,
    )

    # Weight for fold bif
    fig.add_trace(
        go.Scatter(
            x=df_plot["Time"],
            y=df_plot["fold_prob"],
            marker_color=dic_colours["dl_fold"],
            showlegend=False,
            line={"width": 1.2},
        ),
        row=4,
        col=1,
    )

    # --------------
    # Add labels and titles
    # ----------------------

    list_annotations = []

    # Letter label
    label_annotation = dict(
        # x=sum(xrange)/2,
        x=0.03,
        y=1,
        text="<b>{}</b>".format(letter_label),
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(color="black", size=16),
    )

    # Label for N of data points
    n_label = "N={}".format(len(df_ews[df_ews["tsid"] == tsid]))
    n_annotation = dict(
        # x=sum(xrange)/2,
        x=1,
        y=0.8,
        text=n_label,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(color="black", size=11),
    )

    title_annotation = dict(
        # x=sum(xrange)/2,
        x=0.15,
        y=1,
        text=title,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(color="black", size=14),
    )

    list_annotations.append(label_annotation)
    list_annotations.append(n_annotation)
    # list_annotations.append(title_annotation)

    fig["layout"].update(annotations=list_annotations)

    # -------
    # Axes properties
    # ---------

    fig.update_xaxes(
        title={"text": "Age (yr BP)", "standoff": 5},
        ticks="outside",
        showline=True,
        linewidth=1,
        linecolor="black",
        mirror=True,
        row=4,
        col=1,
    )

    # Global y axis properties
    fig.update_yaxes(
        showline=True,
        ticks="outside",
        linecolor="black",
        mirror=True,
        showgrid=False,
        automargin=False,
    )

    # Global x axis properties
    fig.update_xaxes(
        showline=True,
        linecolor="black",
        mirror=False,
        showgrid=False,
        automargin=False,
        tickangle=0,
    )

    fig.update_xaxes(mirror=True, row=1, col=1)

    # Y label for proxy
    proxy_label = df_traj[df_traj["tsid"] == tsid]["Climate proxy"].iloc[0]
    # Abbreviations
    if proxy_label == "Temperature (C)":
        proxy_label = "Temp. (C)"
    if proxy_label == "Grayscale (0-255)":
        proxy_label = "Grayscale"
    if proxy_label == "Terrigeneous dust (%)":
        proxy_label = "T. dust (%)"

    fig.update_yaxes(
        title={
            "text": proxy_label,
            "standoff": 5,
        },
        row=1,
        col=1,
    )

    fig.update_yaxes(
        title={
            "text": "Lag-1 AC",
            "standoff": 5,
        },
        row=2,
        col=1,
    )

    fig.update_yaxes(
        title={
            "text": "Variance",
            "standoff": 5,
        },
        row=3,
        col=1,
    )

    fig.update_yaxes(
        title={
            "text": "DL probability",
            "standoff": 5,
        },
        range=[-0.05, 1.07],
        row=4,
        col=1,
    )

    fig.update_layout(
        height=400,
        width=200,
        margin={"l": 50, "r": 10, "b": 50, "t": 10},
        font=dict(size=12, family="Times New Roman"),
        paper_bgcolor="rgba(255,255,255,1)",
        plot_bgcolor="rgba(255,255,255,1)",
    )

    return fig


# ---------- Loop over all ID values

# Order tsid same way as Dakos (2008)
list_tsid = [1, 8, 7, 6, 5, 2, 3]

import string

list_letter_labels = string.ascii_lowercase[: len(list_tsid)]

i = 0
for tsid in list_tsid:
    # Make figure
    letter_label = list_letter_labels[i]
    i += 1

    fig = make_grid_figure(tsid, letter_label, "")

    # Any specific adjustments
    if tsid == 3:
        fig.update_xaxes(tickvals=[-12.4e3, -12.2e3, -12e3, -11.8e3])

    # Export as png
    fig.write_image(
        "../figures/fig_grid_ind/ind_figs_null/img_{}.png".format(tsid), scale=2
    )
    print("Exported image {}".format(tsid))
