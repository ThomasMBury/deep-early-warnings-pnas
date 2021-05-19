#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 19:39:06 2021

Make figure of trajectory and EWS for SEIRx model
Panels for trajectory, lag-1 AC, variance, DL prediction

@author: tbury
"""

import numpy as np
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# tsid to plot
tsid = 7


#---------------
# Import data
#---------------


# Import EWS data
df_ews = pd.read_csv('../test_models/seirx_1500/data/ews/df_ews_forced.csv')
# Get transition times (where residuals end)
t_transition = df_ews[['Time','Residuals']].dropna()['Time'].iloc[-1]


# Import trajectory data
path = '../test_models/seirx_1500/data/sims_chris/df_traj.csv'
df_traj = pd.read_csv(path)

# Time range of trajectory to plot
tmax = t_transition*1.2
tmin = df_ews['Time'].iloc[0]
df_traj = df_traj[(df_traj['time']>=tmin)&(df_traj['time']<=tmax)]

# Get forced trajectory data
df_traj = df_traj[df_traj['forcing']=='forced']

# Import ML data
df_ml = pd.read_csv('../test_models/seirx_1500/data/ml_preds/df_ml_forced.csv')



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


fig = make_subplots(rows=4, cols=2,
                    shared_xaxes=True,
                    vertical_spacing=0.04,
                    )


#----------------
# Col 1: x variable
#------------------

# Get data to plot
df_traj_plot = df_traj[(df_traj['tsid']==tsid)]
df_ews_plot = df_ews[(df_ews['tsid']==tsid)&(df_ews['var']=='x')]
df_ml_plot = df_ml[(df_ml['tsid']==tsid)&(df_ml['var']=='x')]

# Trace for trajectory
fig.add_trace(
    go.Scatter(x=df_traj_plot['time'],
               y=df_traj_plot['x'],
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
               y=df_ews_plot['Variance']*1e6,
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
# Col 2: I variable
#------------------

# Get data to plot
df_traj_plot = df_traj[(df_traj['tsid']==tsid)]
df_ews_plot = df_ews[(df_ews['tsid']==tsid)&(df_ews['var']=='I')]
df_ml_plot = df_ml[(df_ml['tsid']==tsid)&(df_ml['var']=='I')]


# Trace for trajectory
fig.add_trace(
    go.Scatter(x=df_traj_plot['time'],
               y=df_traj_plot['I'],
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
               y=df_ews_plot['Variance'],
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




#--------------
# Shapes
#--------------
 
list_shapes = []


# Vertical lines for where transitions occur

#  Line for transition col1
shape = {'type': 'line', 
          'x0': t_transition, 
          'y0': 0, 
          'x1': t_transition, 
          'y1': 1, 
          'xref': 'x', 
          'yref': 'paper',
          'line': {'width':linewidth,'dash':'dot'},
          }
list_shapes.append(shape)

#  Line for transition col2
shape = {'type': 'line', 
          'x0': t_transition, 
          'y0': 0, 
          'x1': t_transition, 
          'y1': 1, 
          'xref': 'x2', 
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

axes_numbers = [str(n) for n in np.arange(1,9)]
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
title_x = dict(
        x=0.5,
        y=y_pos,
        text='x',
        xref='x domain',
        yref='paper',
        showarrow=False,
        font = dict(
                color = "black",
                size = 10)
        )
title_I = dict(
        x=0.5,
        y=y_pos,
        text='I',
        xref='x2 domain',
        yref='paper',
        showarrow=False,
        font = dict(
                color = "black",
                size = 10)
        )


# label for scaling factor of variance (10^-3)
axes_numbers = ['5']
for axis_number in axes_numbers:
    label_scaling = dict(
        x=0,
        y=1,
        text='&times;10<sup>-6</sup>',
        xref='x{} domain'.format(axis_number),
        yref='y{} domain'.format(axis_number),
        showarrow=False,
        font = dict(
                color = "black",
                size = font_size)
        )
    list_annotations.append(label_scaling)




# Arrows to indiciate rolling window
axes_numbers = ['3','4','5','6']
arrowhead=1
arrowsize=1.5
arrowwidth=0.4

for axis_number in axes_numbers:
    # Make right-pointing arrow
    annotation_arrow_right = dict(
          x=df_ews_plot['Time'].iloc[0], # arrows' head
          y=0.1,  # arrows' head
          ax=df_ews_plot[['Time','Variance']].dropna().iloc[0]['Time'],  # arrows' tail
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
          ax=df_ews_plot['Time'].iloc[0], # arrows' head
          y=0.1,  # arrows' head
          x=df_ews_plot[['Time','Variance']].dropna().iloc[0]['Time'],  # arrows' tail
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

list_annotations.append(title_x)
list_annotations.append(title_I)


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

fig.update_yaxes(title='DL weights',
                 row=4,col=1)   

fig.update_yaxes(range=[-0.05,1.05],
                  row=1,col=1)

fig.update_yaxes(range=[-2,50],
                  row=1,col=2)

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
img.save('figures/fig_ews_seirx_model.png', dpi=(dpi,dpi))






