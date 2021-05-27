#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 19:39:06 2021

Make figure of trajectory and EWS for simple ecological models
Panels for trajectory, lag-1 AC, variance, DL prediction

@author: tbury
"""

import numpy as np
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots



#---------------
# Import data
#---------------


# Import EWS data
df_ews_fold = pd.read_csv('../test_models/may_fold_1500/data/ews/df_ews_forced.csv')
df_ews_hopf = pd.read_csv('../test_models/cr_hopf_1500/data/ews/df_ews_forced.csv')
df_ews_branch = pd.read_csv('../test_models/cr_trans_1500/data/ews/df_ews_forced.csv')


# Import ML prediction data
df_ml_fold = pd.read_csv('../test_models/may_fold_1500/data/ml_preds/df_ml_forced.csv')
df_ml_hopf = pd.read_csv('../test_models/cr_hopf_1500/data/ml_preds/df_ml_forced.csv')
df_ml_branch = pd.read_csv('../test_models/cr_trans_1500/data/ml_preds/df_ml_forced.csv')


# Get transition times
t_transition_fold = df_ews_fold[['Time','Residuals']].dropna()['Time'].iloc[-1]
t_transition_hopf = df_ews_hopf[['Time','Residuals']].dropna()['Time'].iloc[-1]
t_transition_branch = df_ews_branch[['Time','Residuals']].dropna()['Time'].iloc[-1]


# tsid to plot
tsid_fold = 1
tsid_hopf = 1
tsid_branch = 3

#----------
# general fig params
#--------------

# Pixels to mm
mm_to_pixel = 96/25.4 # 96 dpi, 25.4mm in an inch

# Nature width of single col fig : 89mm
# Nature width of double col fig : 183mm

# Get width of single panel in pixels
fig_width = 89*mm_to_pixel # try single col width
fig_height = fig_width*0.9


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

font_size = 8
font_family = 'Times New Roman'
font_size_letter_label = 10

linewidth = 0.7
linewidth_axes = 0.5
tickwidth = 0.5
ticklen = 2

# dist from axis to axis label
xaxes_standoff = 0
yaxes_standoff = 0


# Scale up factor on image export
scale = 8 # default dpi=72 - nature=300-600


fig = make_subplots(rows=4, cols=3,
                    shared_xaxes=True,
                    vertical_spacing=0.04,
                    )


#----------------
# Col 1: May Fold bifurcation
#------------------

# Get data to plot
df_ews_plot = df_ews_fold[df_ews_fold['tsid']==tsid_fold]
df_ml_plot = df_ml_fold[df_ml_fold['tsid']==tsid_fold]


# Trace for trajectory
fig.add_trace(
    go.Scatter(x=df_ews_plot['Time'],
               y=df_ews_plot['State variable'],
               marker_color=dic_colours['state'],
               showlegend=False,
               line={'width':linewidth},
               ),
    row=1,col=1,
    )

# Trace for smoothing
fig.add_trace(
    go.Scatter(x=df_ews_plot['Time'],
               y=df_ews_plot['Smoothing'],
               marker_color=dic_colours['smoothing'],
               showlegend=False,
               line={'width':linewidth},
               ),
    row=1,col=1,
    )

# Trace for lag-1 AC
fig.add_trace(
    go.Scatter(x=df_ews_plot['Time'],
               y=df_ews_plot['Lag-1 AC'],
               marker_color=dic_colours['ac'],
               showlegend=False,
               line={'width':linewidth},
               ),
    row=2,col=1,

    )


# Trace for variance
fig.add_trace(
    go.Scatter(x=df_ews_plot['Time'],
               y=df_ews_plot['Variance']*1e3,
               marker_color=dic_colours['variance'],
               showlegend=False,
               line={'width':linewidth},
               ),
    row=3,col=1,

    )



# # Weight for any bif
# fig.add_trace(
#     go.Scatter(x=df_ml_plot['Time'],
#                y=df_ml_plot['bif_prob'],
#                marker_color=dic_colours['dl_bif'],
#                showlegend=False,
#                line={'width':linewidth},
#                ),
#     row=4,col=1,
#     )

# Weight for hopf bif
fig.add_trace(
    go.Scatter(x=df_ml_plot['Time'],
               y=df_ml_plot['hopf_prob'],
               marker_color=dic_colours['dl_hopf'],
               showlegend=False,
               line={'width':linewidth},
               ),
    row=4,col=1,
    )

# Weight for branch bif
fig.add_trace(
    go.Scatter(x=df_ml_plot['Time'],
               y=df_ml_plot['branch_prob'],
            marker_color=dic_colours['dl_branch'],
            showlegend=False,
            line={'width':linewidth},
       ),
    row=4,col=1,
    )

# Weight for fold bif
fig.add_trace(
    go.Scatter(x=df_ml_plot['Time'],
               y=df_ml_plot['fold_prob'],
               marker_color=dic_colours['dl_fold'],
               showlegend=False,
               line={'width':linewidth},
       ),
    row=4,col=1,
    )



#----------------
# Col 2: CR model Hopf
#------------------

# Get data to plot
df_ews_plot = df_ews_hopf[(df_ews_hopf['tsid']==tsid_hopf)&\
                          (df_ews_hopf['Variable']=='x')
                          ]
df_ml_plot = df_ml_hopf[df_ml_hopf['tsid']==tsid_hopf]


# Trace for trajectory
fig.add_trace(
    go.Scatter(x=df_ews_plot['Time'],
               y=df_ews_plot['State variable'],
               marker_color=dic_colours['state'],
               showlegend=False,
               line={'width':linewidth},
               ),
    row=1,col=2,
    )

# Trace for smoothing
fig.add_trace(
    go.Scatter(x=df_ews_plot['Time'],
               y=df_ews_plot['Smoothing'],
               marker_color=dic_colours['smoothing'],
               showlegend=False,
               line={'width':linewidth},
               ),
    row=1,col=2,
    )

# Trace for lag-1 AC
fig.add_trace(
    go.Scatter(x=df_ews_plot['Time'],
               y=df_ews_plot['Lag-1 AC'],
               marker_color=dic_colours['ac'],
               showlegend=False,
               line={'width':linewidth},
               ),
    row=2,col=2,

    )


# Trace for variance
fig.add_trace(
    go.Scatter(x=df_ews_plot['Time'],
               y=df_ews_plot['Variance']*1e3,
               marker_color=dic_colours['variance'],
               showlegend=False,
               line={'width':linewidth},
               ),
    row=3,col=2,

    )


# # Weight for any bif
# fig.add_trace(
#     go.Scatter(x=df_ml_plot['Time'],
#                y=df_ml_plot['bif_prob'],
#                marker_color=dic_colours['dl_bif'],
#                showlegend=False,
#                line={'width':linewidth},
#                ),
#     row=4,col=2,
#     )

# Weight for hopf bif
fig.add_trace(
    go.Scatter(x=df_ml_plot['Time'],
               y=df_ml_plot['hopf_prob'],
               marker_color=dic_colours['dl_hopf'],
               showlegend=False,
               line={'width':linewidth},
               ),
    row=4,col=2,
    )

# Weight for branch bif
fig.add_trace(
    go.Scatter(x=df_ml_plot['Time'],
               y=df_ml_plot['branch_prob'],
            marker_color=dic_colours['dl_branch'],
            showlegend=False,
            line={'width':linewidth},
       ),
    row=4,col=2,
    )

# Weight for fold bif
fig.add_trace(
    go.Scatter(x=df_ml_plot['Time'],
               y=df_ml_plot['fold_prob'],
               marker_color=dic_colours['dl_fold'],
               showlegend=False,
               line={'width':linewidth},
       ),
    row=4,col=2,
    )



#----------------
# Col 3: CR model branch
#------------------

# Get data to plot
df_ews_plot = df_ews_branch[(df_ews_branch['tsid']==tsid_branch)&\
                            (df_ews_branch['Variable']=='x')
                            ]
df_ml_plot = df_ml_branch[df_ml_branch['tsid']==tsid_branch]


# Trace for trajectory
fig.add_trace(
    go.Scatter(x=df_ews_plot['Time'],
               y=df_ews_plot['State variable'],
               marker_color=dic_colours['state'],
               showlegend=False,
               line={'width':linewidth},
               ),
    row=1,col=3,
    )

# Trace for smoothing
fig.add_trace(
    go.Scatter(x=df_ews_plot['Time'],
               y=df_ews_plot['Smoothing'],
               marker_color=dic_colours['smoothing'],
               showlegend=False,
               line={'width':linewidth},
               ),
    row=1,col=3,
    )

# Trace for lag-1 AC
fig.add_trace(
    go.Scatter(x=df_ews_plot['Time'],
               y=df_ews_plot['Lag-1 AC'],
               marker_color=dic_colours['ac'],
               showlegend=False,
               line={'width':linewidth},
               ),
    row=2,col=3,

    )


# Trace for variance
fig.add_trace(
    go.Scatter(x=df_ews_plot['Time'],
               y=df_ews_plot['Variance']*1e3,
               marker_color=dic_colours['variance'],
               showlegend=False,
               line={'width':linewidth},
               ),
    row=3,col=3,

    )


# # Weight for any bif
# fig.add_trace(
#     go.Scatter(x=df_ml_plot['Time'],
#                y=df_ml_plot['bif_prob'],
#                marker_color=dic_colours['dl_bif'],
#                showlegend=False,
#                line={'width':linewidth},
#                ),
#     row=4,col=3,
#     )

# Weight for hopf bif
fig.add_trace(
    go.Scatter(x=df_ml_plot['Time'],
               y=df_ml_plot['hopf_prob'],
               marker_color=dic_colours['dl_hopf'],
               showlegend=False,
               line={'width':linewidth},
               ),
    row=4,col=3,
    )

# Weight for branch bif
fig.add_trace(
    go.Scatter(x=df_ml_plot['Time'],
               y=df_ml_plot['branch_prob'],
            marker_color=dic_colours['dl_branch'],
            showlegend=False,
            line={'width':linewidth},
       ),
    row=4,col=3,
    )

# Weight for fold bif
fig.add_trace(
    go.Scatter(x=df_ml_plot['Time'],
               y=df_ml_plot['fold_prob'],
               marker_color=dic_colours['dl_fold'],
               showlegend=False,
               line={'width':linewidth},
       ),
    row=4,col=3,
    )




#--------------
# Shapes
#--------------
 
list_shapes = []


# Vertical lines for where transitions occur

#  Line for fold transition
shape = {'type': 'line', 
          'x0': t_transition_fold, 
          'y0': 0, 
          'x1': t_transition_fold, 
          'y1': 1, 
          'xref': 'x', 
          'yref': 'paper',
          'line': {'width':linewidth,'dash':'dot'},
          }
list_shapes.append(shape)

#  Line for hopf transition
shape = {'type': 'line', 
          'x0': t_transition_hopf, 
          'y0': 0, 
          'x1': t_transition_hopf, 
          'y1': 1, 
          'xref': 'x5', 
          'yref': 'paper',
          'line': {'width':linewidth,'dash':'dot'},
          } 
list_shapes.append(shape)


#  Line for branch transition
shape = {'type': 'line', 
          'x0': t_transition_branch, 
          'y0': 0, 
          'x1': t_transition_branch, 
          'y1': 1, 
          'xref': 'x9', 
          'yref': 'paper',
          'line': {'width':linewidth,'dash':'dot'},
          } 
list_shapes.append(shape)




fig['layout'].update(shapes=list_shapes)



#--------------
# Add annotations
#----------------------

list_annotations = []


# Letter labels for each panel
import string
label_letters = string.ascii_lowercase

axes_numbers = [str(n) for n in np.arange(1,13)]
axes_numbers[0] = ''
idx=0
for axis_number in axes_numbers:
    label_annotation = dict(
            x=0.01,
            y=1.17,
            text='<b>{}</b>'.format(label_letters[idx]),
            xref='x{} domain'.format(axis_number),
            yref='y{} domain'.format(axis_number),
            showarrow=False,
            font = dict(
                    color = "black",
                    size = font_size_letter_label)
            )
    list_annotations.append(label_annotation)
    idx+=1




# Bifurcation titles
y_pos = 1.06
title_fold = dict(
        x=0.5,
        y=y_pos,
        text='Fold',
        xref='x domain',
        yref='paper',
        showarrow=False,
        font = dict(
                color = "black",
                size = 10)
        )
title_hopf = dict(
        x=0.5,
        y=y_pos,
        text='Hopf',
        xref='x2 domain',
        yref='paper',
        showarrow=False,
        font = dict(
                color = "black",
                size = 10)
        )
title_branch = dict(
        x=0.5,
        y=y_pos,
        text='Transcritical',
        xref='x3 domain',
        yref='paper',
        showarrow=False,
        font = dict(
                color = "black",
                size = 10)
        )

# label for scaling factor of variance (10^-3)
axes_numbers = ['7','8','9']
for axis_number in axes_numbers:
    label_scaling = dict(
        x=0,
        y=1,
        text='&times;10<sup>-3</sup>',
        xref='x{} domain'.format(axis_number),
        yref='y{} domain'.format(axis_number),
        showarrow=False,
        font = dict(
                color = "black",
                size = font_size)
        )
    list_annotations.append(label_scaling)




# Arrows to indiciate rolling window
axes_numbers = ['4','5','6','7','8','9']
arrowhead=1
arrowsize=1.5
arrowwidth=0.4

for axis_number in axes_numbers:
    # Make right-pointing arrow
    annotation_arrow_right = dict(
          x=0,  # arrows' head
          y=0.1,  # arrows' head
          ax=1500*0.25,  # arrows' tail
          ay=0.1,  # arrows' tail
          xref='x{}'.format(axis_number),
          yref='y{} domain'.format(axis_number),
          axref='x{}'.format(axis_number),
          ayref='y{} domain'.format(axis_number),
          text='',  # if you want only the arrow
          showarrow=True,
          arrowhead=arrowhead,
          arrowsize=arrowsize,
          arrowwidth=arrowwidth,
          arrowcolor='black'
        )       
    # Make left-pointing arrow
    annotation_arrow_left = dict(
          ax=0,  # arrows' head
          y=0.1,  # arrows' head
          x=1500*0.25,  # arrows' tail
          ay=0.1,  # arrows' tail
          xref='x{}'.format(axis_number),
          yref='y{} domain'.format(axis_number),
          axref='x{}'.format(axis_number),
          ayref='y{} domain'.format(axis_number),
          text='',  # if you want only the arrow
          showarrow=True,
          arrowhead=arrowhead,
          arrowsize=arrowsize,
          arrowwidth=arrowwidth,
          arrowcolor='black'
        )

    # Append to annotations
    list_annotations.append(annotation_arrow_left)
    list_annotations.append(annotation_arrow_right)



list_annotations.append(label_annotation)

list_annotations.append(title_fold)
list_annotations.append(title_hopf)
list_annotations.append(title_branch)


fig['layout'].update(annotations=list_annotations)



#-------------
# Axes properties
#-----------

# Global y axis properties
fig.update_yaxes(showline=True,
                 ticks="outside",
                 tickwidth=tickwidth,
                 ticklen=ticklen,
                 linecolor='black',
                 linewidth=linewidth_axes,
                 mirror=False,
                 showgrid=False,
                 automargin=False,
                 title_standoff=yaxes_standoff,
                 )

# Global x axis properties
fig.update_xaxes(showline=True,
                 linecolor='black',
                 linewidth=linewidth_axes,
                 mirror=False,
                 showgrid=False,
                 automargin=False,
                 title_standoff=xaxes_standoff
                 )  


# Specific x axes properties
fig.update_xaxes(title='Time',
                 ticks="outside",
                 tickwidth=tickwidth,
                 ticklen=ticklen,
                 row=4,
                 )

fig.update_xaxes(mirror=False,
                 row=1,
                 )

# Specific y axes properties
fig.update_yaxes(title='State',
                 # title_font=dict(size=font_size),
                 row=1,col=1)

fig.update_yaxes(title='Lag-1 AC',
                 row=2,col=1)

fig.update_yaxes(title='Variance',
                 row=3,col=1)    

fig.update_yaxes(title='DL probability',
                 row=4,col=1)   

fig.update_yaxes(range=[0,0.9],
                 row=1,col=1)

fig.update_yaxes(range=[0.2,1],
                 row=1,col=2)

fig.update_yaxes(range=[1.5,1.75],
                 row=1,col=3) 

fig.update_yaxes(range=[-0.05,1.08],
                 row=4,)


# General layout properties
fig.update_layout(height=fig_height,
                  width=fig_width,
                  margin={'l':30,'r':5,'b':25,'t':15},
                  font=dict(size=font_size, family=font_family),
                  paper_bgcolor='rgba(255,255,255,1)',
                  plot_bgcolor='rgba(255,255,255,1)',
                  )

# Export as temp image
fig.write_image('figures/temp.png',scale=8)



# Import image with Pil to assert dpi and export - this assigns correct
# dimensions in mm for figure.
from PIL import Image
img = Image.open('figures/temp.png')
dpi=96*8 # (default dpi) * (scaling factor)
img.save('figures/fig_ews_eco_models.png', dpi=(dpi,dpi))






