#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 19:39:06 2021

Make a grid figure of an individual trajectory
Panels for trajectory, lag-1 AC, variance, DL prediction

@author: Thomas M. Bury
"""

import numpy as np
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Import trajectory data
df_traj = pd.read_csv('../data/data_transitions.csv')
df_traj['Time (kyr BP)'] = -df_traj['Age [ka BP]']


# Import EWS data
df_ews = pd.read_csv('../data/ews/df_ews_forced.csv')

# Import ML prediction data
df_ml = pd.read_csv('../data/ml_preds/parsed/df_ml_forced.csv')


# Colour scheme
# cols = px.colors.qualitative.D3 # blue, orange, green, red, purple, brown
cols = px.colors.qualitative.Plotly # blue, red, green, purple, orange, cyan, pink, light green
col_grays = px.colors.sequential.gray

dic_colours = {
        'state':'gray',
        'smoothing':col_grays[2],
        'dl_bif':cols[0],
        'variance':cols[1],
        'ac':cols[2],
        'dl_fold':cols[3],  
        'dl_hopf':cols[4],
        'dl_branch':cols[5],
        'dl_null':'black',
     }


letter_label='a'


def make_grid_figure(tsid, var_label, letter_label, title):

    #---------------
    # Build figure
    #--------------
    
    fig = make_subplots(rows=4, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0,
                        )
    

    
    
    #----------------
    # Panel 1: Trajectory including transition
    #------------------
    
    df_traj_plot = df_traj[df_traj['tsid']==tsid]
    
    # Trace for trajectory
    fig.add_trace(
        go.Scatter(x=df_traj_plot['Time (kyr BP)'],
                   y=df_traj_plot['{} [ppm]'.format(var_label)],
                   marker_color=dic_colours['state'],
                   showlegend=False,
                   line={'width':1.2},
                   ),
        row=1,col=1,
        )
    
    
    # Trace for smoothing
    df_ews_plot = df_ews[(df_ews['tsid']==tsid)&(df_ews['Variable label']==var_label)]
    fig.add_trace(
        go.Scatter(x=df_ews_plot['Time'],
                   y=df_ews_plot['Smoothing'],
                   marker_color=dic_colours['smoothing'],
                   showlegend=False,
                   line={'width':1.2},
                   ),
        row=1,col=1,
        )


    
    #-------------------
    # Panel 2: Lag-1 AC
    #--------------------
    
    fig.add_trace(
        go.Scatter(x=df_ews_plot['Time'],
                   y=df_ews_plot['Lag-1 AC'],
                   marker_color=dic_colours['ac'],
                   showlegend=False,
                   line={'width':1.2},
                   ),
        row=2,col=1,

        )

    
    #-------------------
    # Panel 3: Variance
    #--------------------

    fig.add_trace(
        go.Scatter(x=df_ews_plot['Time'],
                   y=df_ews_plot['Variance'],
                   marker_color=dic_colours['variance'],
                   showlegend=False,
                   line={'width':1.2},
                   ),
        row=3,col=1,

        )
    
    
    #-------------------
    # Panel 4: DL weight for any bif
    #--------------------
    
    df_ml_plot = df_ml[(df_ml['tsid']==tsid)&(df_ml['Variable label']==var_label)]

    # # Weight for any bif
    # fig.add_trace(
    #     go.Scatter(x=df_ml_plot['Time'],
    #                y=df_ml_plot['bif_prob'],
    #                marker_color=dic_colors['bif'],
    #                showlegend=False,
    #                line={'width':1.2},
    #                ),
    #     row=4,col=1,
    #     )

    # Weight for hopf bif
    fig.add_trace(
        go.Scatter(x=df_ml_plot['Time'],
                   y=df_ml_plot['hopf_prob'],
                   marker_color=dic_colours['dl_hopf'],
                   showlegend=False,
                   line={'width':1.2},
                   ),
        row=4,col=1,
        )

    # Weight for branch bif
    fig.add_trace(
        go.Scatter(x=df_ml_plot['Time'],
                   y=df_ml_plot['branch_prob'],
                marker_color=dic_colours['dl_branch'],
                showlegend=False,
                line={'width':1.2},
           ),
        row=4,col=1,
        )
    
    # Weight for fold bif
    fig.add_trace(
        go.Scatter(x=df_ml_plot['Time'],
                   y=df_ml_plot['fold_prob'],
                   marker_color=dic_colours['dl_fold'],
                   showlegend=False,
                   line={'width':1.2},
           ),
        row=4,col=1,
        )


    #--------------
    # Add vertical line where transition occurs
    #--------------
     
    # Add vertical lines where transitions occur
    list_shapes = []

    # Get transtiion interval
    t_transition_start = -df_traj_plot['t_transition_start'].iloc[0]
    t_transition_end = -df_traj_plot['t_transition_end'].iloc[0]

    # #  Make line for start of transition transition
    # shape = {'type': 'line', 
    #           'x0': t_transition_start, 
    #           'y0': 0, 
    #           'x1': t_transition_start, 
    #           'y1': 1, 
    #           'xref': 'x', 
    #           'yref': 'paper',
    #           'line': {'width':2,'dash':'dot'},
    #           }    
    

    #  Make shaded box to show transition
    shape = {'type': 'rect', 
              'x0': t_transition_start, 
              'y0': 0, 
              'x1': t_transition_end, 
              'y1': 1, 
              'xref': 'x', 
              'yref': 'paper',
              'fillcolor':'gray',
              'opacity':0.5,
              'line_width':0,
              # 'line': {'width':2,'dash':'dot'},
              }       
    
    
    # Add shape to list
    list_shapes.append(shape)
    
    fig['layout'].update(shapes=list_shapes)
    
    
    #--------------
    # Add labels and titles
    #----------------------
    
    list_annotations = []
    
    
    label_annotation = dict(
            # x=sum(xrange)/2,
            x=0.03,
            y=1,
            text='<b>{}</b>'.format(letter_label),
            xref='paper',
            yref='paper',
            showarrow=False,
            font = dict(
                    color = "black",
                    size = 16)
            )
    
    title_annotation = dict(
            # x=sum(xrange)/2,
            x=0.5,
            y=1,
            text=title,
            xref='paper',
            yref='paper',
            showarrow=False,
            font = dict(
                    color = "black",
                    size = 14)
            ) 
    
    # Label for N of data points
    n_label = 'N={}'.format(len(df_ews_plot))
    n_annotation = dict(
            # x=sum(xrange)/2,
            x=0,
            y=0.86,
            text=n_label,
            xref='paper',
            yref='paper',
            showarrow=False,
            font = dict(
                    color = "black",
                    size = 11)
            )       
    
    list_annotations.append(label_annotation)
    list_annotations.append(title_annotation)
    list_annotations.append(n_annotation)

    
    
    
    
    fig['layout'].update(annotations=list_annotations)
    
    
    
    # Layout properties
    fig.update_xaxes(title={'text':'Time (kyr BP)',
                            'standoff':5},
                     ticks="outside",
                     showline=True,
                     linewidth=1,
                     linecolor='black',
                     mirror=True,
                     row=4,col=1)
    
    # Global y axis properties
    fig.update_yaxes(showline=True,
                     ticks="outside",
                     linecolor='black',
                     mirror=True,
                     showgrid=False,
                     automargin=False,
                     )
    
    
    # Global x axis properties
    fig.update_xaxes(showline=True,
                     linecolor='black',
                     mirror=False,
                     showgrid=False,
                     )  
    
    fig.update_xaxes(mirror=True,
                     row=1,col=1)
    
    fig.update_yaxes(title={'text':'{} (ppm)'.format(var_label),
                            'standoff':5,
                            },
                     row=1,col=1)
    
    fig.update_yaxes(title={'text':'Lag-1 AC',
                            'standoff':5,
                            },
                     row=2,col=1)
    
    fig.update_yaxes(title={'text':'Variance',
                            'standoff':5,
                            },
                     row=3,col=1)    
    
    fig.update_yaxes(title={'text':'ML weights',
                            'standoff':5,
                            },
                     range=[-0.05,1.07],
                     row=4,col=1)     
    
    fig.update_layout(height=400,
                      width=200,
                      margin={'l':50,'r':10,'b':20,'t':10},
                      font=dict(size=12, family='Times New Roman'),
                      paper_bgcolor='rgba(255,255,255,1)',
                      plot_bgcolor='rgba(255,255,255,1)',
                      )
    

    return fig



# # make single fig
# fig = make_grid_figure(1, 'Mo','a','S1')
# fig.write_html('temp.html')
# # fig.write_image('temp.png',scale=2)




#---------- Loop over all tsid-------

import string
list_letter_labels = string.ascii_lowercase[:14]



# Make ind figures for Mo

i=0
list_tsid = np.arange(1,14)
for tsid in list_tsid: 
    # Make figure
    letter_label = list_letter_labels[i]
    i+=1
    
    # Get sapropel ID and core name
    sapropel = df_traj[df_traj['tsid']==tsid]['ID'].iloc[0]
    core = df_traj[df_traj['tsid']==tsid]['Core'].iloc[0]    
    title='{} - {}'.format(sapropel, core[:4])
    
    fig = make_grid_figure(tsid, 'Mo', letter_label, title)      
    # Export as png
    fig.write_image('../figures/fig_grid_ind/ind_figs_u/img_{}.png'.format(tsid),
                    scale=2)    
    print('Exported for tsid = {}'.format(tsid))





# Make ind figures for U
i=0
list_tsid = np.arange(1,14)
for tsid in list_tsid: 
    # Make figure
    letter_label = list_letter_labels[i]
    i+=1
    
    # Get sapropel ID and core name
    sapropel = df_traj[df_traj['tsid']==tsid]['ID'].iloc[0]
    core = df_traj[df_traj['tsid']==tsid]['Core'].iloc[0]    
    title='{} - {}'.format(sapropel, core[:4])
    
    fig = make_grid_figure(tsid, 'U', letter_label, title)      
    # Export as png
    fig.write_image('../figures/fig_grid_ind/ind_figs_u/img_{}.png'.format(tsid),
                    scale=2)    
    print('Exported for tsid = {}'.format(tsid))




