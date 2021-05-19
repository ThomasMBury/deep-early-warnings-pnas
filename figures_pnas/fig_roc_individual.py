#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 19:03:01 2021

Create ROC curves and bar chart inset with favoured bifurcation type.

Run to create individual ROC figures for each model and empirical system.

@author: Thoams M. Bury
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Import PIL for image tools
from PIL import Image



#-----------
# General fig params
#------------

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

# Pixels to mm
mm_to_pixel = 96/25.4 # 96 dpi, 25.4mm in an inch

# Nature width of single col fig : 89mm
# Nature width of double col fig : 183mm

# Get width of single panel in pixels
fig_width = 183*mm_to_pixel/4 # 4 horizontal panels
fig_height = fig_width


font_size = 8
font_family = 'Times New Roman'
font_size_letter_label = 12
font_size_auc_text = 8


# AUC annotations
x_auc = 0.98
y_auc = 0.57
y_auc_sep = 0.065

linewidth = 0.7
linewidth_axes = 0.5
tickwidth = 0.5
linewidth_axes_inset = 0.5


axes_standoff = 0


# Scale up factor on image export
scale = 8 # default dpi=72 - nature=300-600


def make_roc_figure(df_roc, df_counts, letter_label, title=''):
    ''' Make ROC figure (no inset)'''
        
    fig = go.Figure()
    
    
    # DL prediction any bif
    df_trace = df_roc[df_roc['ews']=='ML bif']
    auc_dl = df_trace.round(2)['auc'].iloc[0]
    fig.add_trace(
        go.Scatter(x=df_trace['fpr'],
                    y=df_trace['tpr'],
                    showlegend=False,
                    mode='lines',
                    line=dict(width=linewidth,
                              color=dic_colours['dl_bif'],
                              ),
                    )
        )
    
    
    # Variance plot
    df_trace = df_roc[df_roc['ews']=='Variance']
    auc_var = df_trace.round(2)['auc'].iloc[0]
    fig.add_trace(
        go.Scatter(x=df_trace['fpr'],
                    y=df_trace['tpr'],
                    showlegend=False,
                    mode='lines',
                    line=dict(width=linewidth,
                              color=dic_colours['variance'],
                              ),
                    )
        )
    
    # Lag-1  AC plot
    df_trace = df_roc[df_roc['ews']=='Lag-1 AC']
    auc_ac = df_trace.round(2)['auc'].iloc[0]
    fig.add_trace(
        go.Scatter(x=df_trace['fpr'],
                    y=df_trace['tpr'],
                    showlegend=False,
                    mode='lines',
                    line=dict(width=linewidth,
                              color=dic_colours['ac'],
                              ),
                    )
        )
    
    # Line y=x
    fig.add_trace(
        go.Scatter(x=np.linspace(0,1,100),
                    y=np.linspace(0,1,100),
                    showlegend=False,
                    line=dict(color='black',
                              dash='dot',
                              width=linewidth,
                              ),
                    )
        )
    

    #--------------
    # Add labels and titles
    #----------------------
    
    list_annotations = []
    
    label_annotation = dict(
            # x=sum(xrange)/2,
            x=-0.2,
            y=1,
            text='<b>{}</b>'.format(letter_label),
            xref='paper',
            yref='paper',
            showarrow=False,
            font = dict(
                    color = 'black',
                    size = font_size_letter_label,
                    ),
            )


    

    
    annotation_auc_dl = dict(
            # x=sum(xrange)/2,
            x=x_auc,
            y=y_auc,
            text='A<sub>DL</sub>={:.2f}'.format(auc_dl),
            xref='paper',
            yref='paper',
            showarrow=False,
            font = dict(
                    color = 'black',
                    size = font_size_auc_text,
                    )
            )
        
    
    annotation_auc_var = dict(
            # x=sum(xrange)/2,
            x=x_auc,
            y=y_auc-y_auc_sep,
            text='A<sub>Var</sub>={:.2f}'.format(auc_var),
            xref='paper',
            yref='paper',
            showarrow=False,
            font = dict(
                    color = 'black',
                    size = font_size_auc_text,
                    )
            )    
    
    
    
    annotation_auc_ac = dict(
            # x=sum(xrange)/2,
            x=x_auc,
            y=y_auc-2*y_auc_sep,
            text='A<sub>AC</sub>={:.2f}'.format(auc_ac),
            xref='paper',
            yref='paper',
            showarrow=False,
            font = dict(
                    color = 'black',
                    size = font_size_auc_text,
                    )
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
                    size = font_size)
            ) 
      
    
    list_annotations.append(label_annotation)
    list_annotations.append(annotation_auc_dl)
    list_annotations.append(annotation_auc_var)
    list_annotations.append(annotation_auc_ac)
    # list_annotations.append(title_annotation)

    fig['layout'].update(annotations=list_annotations)
        
    
    #-------------
    # General layout properties
    #--------------
    
    # X axes properties
    fig.update_xaxes(
        title=dict(text='False positive',
                   standoff=axes_standoff,
                   ),
        range=[-0.04,1.04],
        ticks="outside",
        tickwidth=tickwidth,
        tickvals =np.arange(0,1.1,0.2),
        showline=True,
        linewidth=linewidth_axes,
        linecolor='black',
        mirror=False,
        )
    
    
    # Y axes properties
    fig.update_yaxes(
        title=dict(text='True positive',
                   standoff=axes_standoff,
                   ),
        range=[-0.04,1.04],
        ticks="outside",
        tickvals=np.arange(0,1.1,0.2),
        tickwidth=tickwidth,
        showline=True,
        linewidth=linewidth_axes,
        linecolor='black',
        mirror=False,
        )
    
    
    # Overall properties
    fig.update_layout(
        legend=dict(x=0.6, y=0),
        width=fig_width,
        height=fig_height,
        margin=dict(l=30,r=5,b=15,t=5),
        font=dict(size=font_size, family=font_family),
        paper_bgcolor='rgba(255,255,255,1)',
        plot_bgcolor='rgba(255,255,255,1)',
        )

    return fig






def make_bar_inset(df_counts):

    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(x=['F','H','T','N'],
               y=df_counts.iloc[0].values,
               marker_color='gray',
               )
    )
    
    
    #-------------
    # General layout properties
    #--------------
    
    # X axes properties
    fig.update_xaxes(
        # title=dict(text='False positive',
        #            standoff=5,
        #            ),
        # range=[-0.04,1.04],
        # ticks="outside",
        # tickvals =np.arange(0,1.1,0.2),
        showline=True,
        linewidth=linewidth_axes_inset,
        linecolor='black',
        mirror=True,
        )
    
    
    # Y axes properties
    fig.update_yaxes(
        title=dict(text='Frequency',
                   standoff=0,
                   ),
        # range=[-0.04,1.04],
        # ticks="outside",
        # tickvals=np.arange(0,1.1,0.2),
        showline=True,
        linewidth=linewidth_axes_inset,
        linecolor='black',
        mirror=True,
        )
    
    
    # Overall properties
    fig.update_layout(
        # legend=dict(x=0.6, y=0),
        width=fig_width*0.4,
        height=fig_height*0.3,
        margin=dict(l=30,r=3,b=12,t=2),
        font=dict(size=7, family=font_family),
        paper_bgcolor='rgba(255,255,255,1)',
        plot_bgcolor='rgba(255,255,255,1)',
        )
    
    
    return fig



def combine_roc_inset(path_roc, path_inset, path_out):
    ''' 
    Combine ROC plot and inset, and export to path_out
    '''
    
    # Import image
    img_roc = Image.open(path_roc)
    img_inset = Image.open(path_inset)
    
    # Get height and width of frame (in pixels)
    height = img_roc.height
    width = img_roc.width
    
    # Create frame
    dst = Image.new('RGB', (width,height), (255,255,255))
    
    # Pasete in images
    dst.paste(img_roc,(0,0))
    dst.paste(img_inset,(width-img_inset.width-50, 730))
    
    dpi=96*8 # (default dpi) * (scaling factor)
    dst.save(path_out, dpi=(dpi,dpi))
    
    return
    








#---------
# Anoxia early
#---------

print('Make ROC figure for anoxia system using early predictions')

# Import ROC data
df_roc = pd.read_csv('../test_empirical/anoxia/data/roc/df_roc_anoxia_early.csv')

# Import counts of favoured bifurcation
df_counts = pd.read_csv('../test_empirical/anoxia/data/roc/df_bif_pred_counts_early.csv')

# Make ROC fig
fig_roc = make_roc_figure(df_roc, df_counts, 'f')

# Export ROC fig - scale by 8 - defualt dpi = 72 - nature 300-600dpi
fig_roc.write_image('figures/temp_roc.png', 
                    scale=scale,
                    )



# Make inset fig
fig_inset = make_bar_inset(df_counts)
# fig_inset.update_yaxes(range=[0,170])

# Export inset fig
fig_inset.write_image('figures/temp_inset.png',scale=scale)

# Combine figs and export
path_roc = 'figures/temp_roc.png'
path_inset = 'figures/temp_inset.png'
path_out = 'figures/roc_individual/roc_anoxia_early.png'

combine_roc_inset(path_roc, path_inset, path_out)




#---------
# Anoxia late
#---------
print('Make ROC figure for anoxia system using late predictions')

# Import ROC data
df_roc = pd.read_csv('../test_empirical/anoxia/data/roc/df_roc_anoxia_late.csv')

# Import counts of favoured bifurcation
df_counts = pd.read_csv('../test_empirical/anoxia/data/roc/df_bif_pred_counts_late.csv')

# Make ROC fig
fig_roc = make_roc_figure(df_roc, df_counts, 'f')

# Export ROC fig - scale by 8 - defualt dpi = 72 - nature 300-600dpi
fig_roc.write_image('figures/temp_roc.png', 
                    scale=scale,
                    )


# Make inset fig
fig_inset = make_bar_inset(df_counts)
# fig_inset.update_yaxes(range=[0,170])

# Export inset fig
fig_inset.write_image('figures/temp_inset.png',scale=scale)

# Combine figs and export
path_roc = 'figures/temp_roc.png'
path_inset = 'figures/temp_inset.png'
path_out = 'figures/roc_individual/roc_anoxia_late.png'

combine_roc_inset(path_roc, path_inset, path_out)





#---------
# Thermo early
#---------
print('Make ROC figure for thermoacoustic system using early predictions')

# Import ROC data
df_roc = pd.read_csv('../test_empirical/thermoacoustic/data/roc/df_roc_thermo_early.csv')

# Import counts of favoured bifurcation
df_counts = pd.read_csv('../test_empirical/thermoacoustic/data/roc/df_bif_pred_counts_early.csv')

# Make ROC fig
fig_roc = make_roc_figure(df_roc, df_counts, 'g')

# Export ROC fig
fig_roc.write_image('figures/temp_roc.png', scale=scale)


# Make inset fig
fig_inset = make_bar_inset(df_counts)
# fig_inset.update_yaxes(range=[0,130])

# Export inset fig
fig_inset.write_image('figures/temp_inset.png',scale=scale)

# Combine figs and export
path_roc = 'figures/temp_roc.png'
path_inset = 'figures/temp_inset.png'
path_out = 'figures/roc_individual/roc_thermo_early.png'

combine_roc_inset(path_roc, path_inset, path_out)


#---------
# Thermo late
#---------
print('Make ROC figure for thermoacoustic system using late predictions')

# Import ROC data
df_roc = pd.read_csv('../test_empirical/thermoacoustic/data/roc/df_roc_thermo_late.csv')

# Import counts of favoured bifurcation
df_counts = pd.read_csv('../test_empirical/thermoacoustic/data/roc/df_bif_pred_counts_late.csv')

# Make ROC fig
fig_roc = make_roc_figure(df_roc, df_counts, 'g')

# Export ROC fig
fig_roc.write_image('figures/temp_roc.png', scale=scale)


# Make inset fig
fig_inset = make_bar_inset(df_counts)
# fig_inset.update_yaxes(range=[0,130])

# Export inset fig
fig_inset.write_image('figures/temp_inset.png',scale=scale)

# Combine figs and export
path_roc = 'figures/temp_roc.png'
path_inset = 'figures/temp_inset.png'
path_out = 'figures/roc_individual/roc_thermo_late.png'

combine_roc_inset(path_roc, path_inset, path_out)





#---------
# Paeloclimate early
#---------
print('Make ROC figure for paleoclimate system using early predictions')

# Import ROC data
df_roc = pd.read_csv('../test_empirical/paleoclimate/data/roc/df_roc_dakos_early.csv')

# Import counts of favoured bifurcation
df_counts = pd.read_csv('../test_empirical/paleoclimate/data/roc/df_bif_pred_counts_early.csv')

# Make ROC fig
fig_roc = make_roc_figure(df_roc, df_counts, 'h')

# Export ROC fig
fig_roc.write_image('figures/temp_roc.png', scale=scale)


# Make inset fig
fig_inset = make_bar_inset(df_counts)
# fig_inset.update_yaxes(range=[0,40])

# Export inset fig
fig_inset.write_image('figures/temp_inset.png',scale=scale)

# Combine figs and export
path_roc = 'figures/temp_roc.png'
path_inset = 'figures/temp_inset.png'
path_out = 'figures/roc_individual/roc_climate_early.png'

combine_roc_inset(path_roc, path_inset, path_out)


#---------
# Paeloclimate late
#---------
print('Make ROC figure for paleoclimate system using late predictions')

# Import ROC data
df_roc = pd.read_csv('../test_empirical/paleoclimate/data/roc/df_roc_dakos_late.csv')

# Import counts of favoured bifurcation
df_counts = pd.read_csv('../test_empirical/paleoclimate/data/roc/df_bif_pred_counts_late.csv')

# Make ROC fig
fig_roc = make_roc_figure(df_roc, df_counts, 'h')

# Export ROC fig
fig_roc.write_image('figures/temp_roc.png', scale=scale)


# Make inset fig
fig_inset = make_bar_inset(df_counts)
# fig_inset.update_yaxes(range=[0,40])

# Export inset fig
fig_inset.write_image('figures/temp_inset.png',scale=scale)

# Combine figs and export
path_roc = 'figures/temp_roc.png'
path_inset = 'figures/temp_inset.png'
path_out = 'figures/roc_individual/roc_climate_late.png'

combine_roc_inset(path_roc, path_inset, path_out)




#---------
# May Fold 500-classifier early
#---------
print('Make ROC figure for May Fold model using early predictions with 500-classifier')

# Import ROC data
df_roc = pd.read_csv('../test_models/may_fold_500/data/roc/df_roc_may_fold_early.csv')

# Import counts of favoured bifurcation
df_counts = pd.read_csv('../test_models/may_fold_500/data/roc/df_bif_pred_counts_early.csv')

# Make ROC fig
fig_roc = make_roc_figure(df_roc, df_counts, 'a')
# # Provide a title
# fig_roc.update_layout(title=dict(text='May fold bifurcation',x=0.57,y=0.99,
#                                  font=dict(size=10,family='Times New Roman'),
#                                  ),
#                       margin=dict(t=15))

# Export ROC fig
fig_roc.write_image('figures/temp_roc.png', scale=scale)


# Make inset fig
fig_inset = make_bar_inset(df_counts)
# fig_inset.update_yaxes(range=[0,40])

# Export inset fig
fig_inset.write_image('figures/temp_inset.png',scale=scale)

# Combine figs and export
path_roc = 'figures/temp_roc.png'
path_inset = 'figures/temp_inset.png'
path_out = 'figures/roc_individual/roc_may_fold_500_early.png'

combine_roc_inset(path_roc, path_inset, path_out)



#---------
# May Fold 500-classifier late
#---------
print('Make ROC figure for May Fold model using late predictions with 500-classifier')

# Import ROC data
df_roc = pd.read_csv('../test_models/may_fold_500/data/roc/df_roc_may_fold_late.csv')

# Import counts of favoured bifurcation
df_counts = pd.read_csv('../test_models/may_fold_500/data/roc/df_bif_pred_counts_late.csv')

# Make ROC fig
fig_roc = make_roc_figure(df_roc, df_counts, 'a')

# Export ROC fig
fig_roc.write_image('figures/temp_roc.png', scale=scale)


# Make inset fig
fig_inset = make_bar_inset(df_counts)
# fig_inset.update_yaxes(range=[0,40])

# Export inset fig
fig_inset.write_image('figures/temp_inset.png',scale=scale)

# Combine figs and export
path_roc = 'figures/temp_roc.png'
path_inset = 'figures/temp_inset.png'
path_out = 'figures/roc_individual/roc_may_fold_500_late.png'

combine_roc_inset(path_roc, path_inset, path_out)





#---------
# May Fold 1500-classifier early 
#---------
print('Make ROC figure for May Fold model using early predictions with 1500-classifier')

# Import ROC data
df_roc = pd.read_csv('../test_models/may_fold_1500/data/roc/df_roc_may_fold_early.csv')

# Import counts of favoured bifurcation
df_counts = pd.read_csv('../test_models/may_fold_1500/data/roc/df_bif_pred_counts_early.csv')

# Make ROC fig
fig_roc = make_roc_figure(df_roc, df_counts, 'a')
# Provide a title
fig_roc.update_layout(title=dict(text='May fold bifurcation',x=0.57,y=0.99,
                                  font=dict(size=10,family='Times New Roman'),
                                  ),
                      margin=dict(t=15))



# Export ROC fig
fig_roc.write_image('figures/temp_roc.png', scale=scale)


# Make inset fig
fig_inset = make_bar_inset(df_counts)
# fig_inset.update_yaxes(range=[0,40])

# Export inset fig
fig_inset.write_image('figures/temp_inset.png',scale=scale)

# Combine figs and export
path_roc = 'figures/temp_roc.png'
path_inset = 'figures/temp_inset.png'
path_out = 'figures/roc_individual/roc_may_fold_1500_early.png'

combine_roc_inset(path_roc, path_inset, path_out)




#---------
# May Fold 1500-classifier late
#---------
print('Make ROC figure for May Fold model using late predictions with 1500-classifier')

# Import ROC data
df_roc = pd.read_csv('../test_models/may_fold_1500/data/roc/df_roc_may_fold_late.csv')

# Import counts of favoured bifurcation
df_counts = pd.read_csv('../test_models/may_fold_1500/data/roc/df_bif_pred_counts_late.csv')

# Make ROC fig
fig_roc = make_roc_figure(df_roc, df_counts, 'd')

# Export ROC fig
fig_roc.write_image('figures/temp_roc.png', scale=scale)


# Make inset fig
fig_inset = make_bar_inset(df_counts)
# fig_inset.update_yaxes(range=[0,40])

# Export inset fig
fig_inset.write_image('figures/temp_inset.png',scale=scale)

# Combine figs and export
path_roc = 'figures/temp_roc.png'
path_inset = 'figures/temp_inset.png'
path_out = 'figures/roc_individual/roc_may_fold_1500_late.png'

combine_roc_inset(path_roc, path_inset, path_out)






#---------
# CR Hopf 500-classifier early
#---------
print('Make ROC figure for CR Hopf model using early predictions with 500-classifier')

# Import ROC data
df_roc = pd.read_csv('../test_models/cr_hopf_500/data/roc/df_roc_early.csv')

# Import counts of favoured bifurcation
df_counts = pd.read_csv('../test_models/cr_hopf_500/data/roc/df_bif_pred_counts_early.csv')

# Make ROC fig
fig_roc = make_roc_figure(df_roc, df_counts, 'a')
# # Provide a title
# fig_roc.update_layout(title=dict(text='May fold bifurcation',x=0.57,y=0.99,
#                                  font=dict(size=10,family='Times New Roman'),
#                                  ),
#                       margin=dict(t=15))

# Export ROC fig
fig_roc.write_image('figures/temp_roc.png', scale=scale)


# Make inset fig
fig_inset = make_bar_inset(df_counts)
# fig_inset.update_yaxes(range=[0,40])

# Export inset fig
fig_inset.write_image('figures/temp_inset.png',scale=scale)

# Combine figs and export
path_roc = 'figures/temp_roc.png'
path_inset = 'figures/temp_inset.png'
path_out = 'figures/roc_individual/roc_cr_hopf_500_early.png'

combine_roc_inset(path_roc, path_inset, path_out)




#---------
# CR Hopf 500-classifier late
#---------
print('Make ROC figure for CR Hopf model using late predictions with 500-classifier')

# Import ROC data
df_roc = pd.read_csv('../test_models/cr_hopf_500/data/roc/df_roc_late.csv')

# Import counts of favoured bifurcation
df_counts = pd.read_csv('../test_models/cr_hopf_500/data/roc/df_bif_pred_counts_late.csv')

# Make ROC fig
fig_roc = make_roc_figure(df_roc, df_counts, 'a')
# # Provide a title
# fig_roc.update_layout(title=dict(text='May fold bifurcation',x=0.57,y=0.99,
#                                  font=dict(size=10,family='Times New Roman'),
#                                  ),
#                       margin=dict(t=15))

# Export ROC fig
fig_roc.write_image('figures/temp_roc.png', scale=scale)


# Make inset fig
fig_inset = make_bar_inset(df_counts)
# fig_inset.update_yaxes(range=[0,40])

# Export inset fig
fig_inset.write_image('figures/temp_inset.png',scale=scale)

# Combine figs and export
path_roc = 'figures/temp_roc.png'
path_inset = 'figures/temp_inset.png'
path_out = 'figures/roc_individual/roc_cr_hopf_500_late.png'

combine_roc_inset(path_roc, path_inset, path_out)








#---------
# CR Hopf 1500-classifier early 
#---------
print('Make ROC figure for CR Hopf model using early predictions with 1500-classifier')

# Import ROC data
df_roc = pd.read_csv('../test_models/cr_hopf_1500/data/roc/df_roc_cr_hopf_early.csv')

# Import counts of favoured bifurcation
df_counts = pd.read_csv('../test_models/cr_hopf_1500/data/roc/df_bif_pred_counts_early.csv')

# Make ROC fig
fig_roc = make_roc_figure(df_roc, df_counts, 'b')
# Provide a title
fig_roc.update_layout(title=dict(text='CR Hopf bifurcation',x=0.57,y=0.99,
                                  font=dict(size=10,family='Times New Roman'),
                                  ),
                      margin=dict(t=15))
# Export ROC fig
fig_roc.write_image('figures/temp_roc.png', scale=scale)


# Make inset fig
fig_inset = make_bar_inset(df_counts)
# fig_inset.update_yaxes(range=[0,40])

# Export inset fig
fig_inset.write_image('figures/temp_inset.png',scale=scale)

# Combine figs and export
path_roc = 'figures/temp_roc.png'
path_inset = 'figures/temp_inset.png'
path_out = 'figures/roc_individual/roc_cr_hopf_1500_early.png'

combine_roc_inset(path_roc, path_inset, path_out)





#---------
# CR Hopf 1500-classifier late 
#---------
print('Make ROC figure for CR Hopf model using late predictions with 1500-classifier')

# Import ROC data
df_roc = pd.read_csv('../test_models/cr_hopf_1500/data/roc/df_roc_cr_hopf_late.csv')

# Import counts of favoured bifurcation
df_counts = pd.read_csv('../test_models/cr_hopf_1500/data/roc/df_bif_pred_counts_late.csv')

# Make ROC fig
fig_roc = make_roc_figure(df_roc, df_counts, 'b')
# Provide a title
fig_roc.update_layout(title=dict(text='CR Hopf bifurcation',x=0.57,y=0.99,
                                  font=dict(size=10,family='Times New Roman'),
                                  ),
                      margin=dict(t=15))
# Export ROC fig
fig_roc.write_image('figures/temp_roc.png', scale=scale)


# Make inset fig
fig_inset = make_bar_inset(df_counts)
# fig_inset.update_yaxes(range=[0,40])

# Export inset fig
fig_inset.write_image('figures/temp_inset.png',scale=scale)

# Combine figs and export
path_roc = 'figures/temp_roc.png'
path_inset = 'figures/temp_inset.png'
path_out = 'figures/roc_individual/roc_cr_hopf_1500_late.png'

combine_roc_inset(path_roc, path_inset, path_out)







#---------
# CR Transcritical 500-classifier early
#---------
print('Make ROC figure for CR Transcritical model using early predictions with 500-classifier')

# Import ROC data
df_roc = pd.read_csv('../test_models/cr_trans_500/data/roc/df_roc_early.csv')

# Import counts of favoured bifurcation
df_counts = pd.read_csv('../test_models/cr_trans_500/data/roc/df_bif_pred_counts_early.csv')

# Make ROC fig
fig_roc = make_roc_figure(df_roc, df_counts, 'a')
# # Provide a title
# fig_roc.update_layout(title=dict(text='May fold bifurcation',x=0.57,y=0.99,
#                                  font=dict(size=10,family='Times New Roman'),
#                                  ),
#                       margin=dict(t=15))

# Export ROC fig
fig_roc.write_image('figures/temp_roc.png', scale=scale)


# Make inset fig
fig_inset = make_bar_inset(df_counts)
# fig_inset.update_yaxes(range=[0,40])

# Export inset fig
fig_inset.write_image('figures/temp_inset.png',scale=scale)

# Combine figs and export
path_roc = 'figures/temp_roc.png'
path_inset = 'figures/temp_inset.png'
path_out = 'figures/roc_individual/roc_cr_trans_500_early.png'

combine_roc_inset(path_roc, path_inset, path_out)







#---------
# CR Transcritical 500-classifier late
#---------
print('Make ROC figure for CR Transcritical model using late predictions with 500-classifier')

# Import ROC data
df_roc = pd.read_csv('../test_models/cr_trans_500/data/roc/df_roc_late.csv')

# Import counts of favoured bifurcation
df_counts = pd.read_csv('../test_models/cr_trans_500/data/roc/df_bif_pred_counts_late.csv')

# Make ROC fig
fig_roc = make_roc_figure(df_roc, df_counts, 'a')
# # Provide a title
# fig_roc.update_layout(title=dict(text='May fold bifurcation',x=0.57,y=0.99,
#                                  font=dict(size=10,family='Times New Roman'),
#                                  ),
#                       margin=dict(t=15))

# Export ROC fig
fig_roc.write_image('figures/temp_roc.png', scale=scale)


# Make inset fig
fig_inset = make_bar_inset(df_counts)
# fig_inset.update_yaxes(range=[0,40])

# Export inset fig
fig_inset.write_image('figures/temp_inset.png',scale=scale)

# Combine figs and export
path_roc = 'figures/temp_roc.png'
path_inset = 'figures/temp_inset.png'
path_out = 'figures/roc_individual/roc_cr_trans_500_late.png'

combine_roc_inset(path_roc, path_inset, path_out)





#---------
# CR Transcritical 1500-classifier early
#---------
print('Make ROC figure for CR Transcritical model using early predictions with 1500-classifier')

# Import ROC data
df_roc = pd.read_csv('../test_models/cr_trans_1500/data/roc/df_roc_cr_trans_early.csv')

# Import counts of favoured bifurcation
df_counts = pd.read_csv('../test_models/cr_trans_1500/data/roc/df_bif_pred_counts_early.csv')

# Make ROC fig
fig_roc = make_roc_figure(df_roc, df_counts, 'a')
# # Provide a title
# fig_roc.update_layout(title=dict(text='May fold bifurcation',x=0.57,y=0.99,
#                                  font=dict(size=10,family='Times New Roman'),
#                                  ),
#                       margin=dict(t=15))

# Export ROC fig
fig_roc.write_image('figures/temp_roc.png', scale=scale)


# Make inset fig
fig_inset = make_bar_inset(df_counts)
# fig_inset.update_yaxes(range=[0,40])

# Export inset fig
fig_inset.write_image('figures/temp_inset.png',scale=scale)

# Combine figs and export
path_roc = 'figures/temp_roc.png'
path_inset = 'figures/temp_inset.png'
path_out = 'figures/roc_individual/roc_cr_trans_1500_early.png'

combine_roc_inset(path_roc, path_inset, path_out)





#---------
# CR Transcritical 1500-classifier late
#---------
print('Make ROC figure for CR Transcritical model using late predictions with 1500-classifier')

# Import ROC data
df_roc = pd.read_csv('../test_models/cr_trans_1500/data/roc/df_roc_cr_trans_late.csv')

# Import counts of favoured bifurcation
df_counts = pd.read_csv('../test_models/cr_trans_1500/data/roc/df_bif_pred_counts_late.csv')

# Make ROC fig
fig_roc = make_roc_figure(df_roc, df_counts, 'a')
# # Provide a title
# fig_roc.update_layout(title=dict(text='May fold bifurcation',x=0.57,y=0.99,
#                                  font=dict(size=10,family='Times New Roman'),
#                                  ),
#                       margin=dict(t=15))

# Export ROC fig
fig_roc.write_image('figures/temp_roc.png', scale=scale)


# Make inset fig
fig_inset = make_bar_inset(df_counts)
# fig_inset.update_yaxes(range=[0,40])

# Export inset fig
fig_inset.write_image('figures/temp_inset.png',scale=scale)

# Combine figs and export
path_roc = 'figures/temp_roc.png'
path_inset = 'figures/temp_inset.png'
path_out = 'figures/roc_individual/roc_cr_trans_1500_late.png'

combine_roc_inset(path_roc, path_inset, path_out)










#---------
# SEIRX Var x early 
#---------
print('Make ROC figure for SEIRx model using early predictions in variable x')

# Import ROC data
df_roc = pd.read_csv('../test_models/seirx_1500/data/roc/df_roc_seirx_x_early.csv')

# Import counts of favoured bifurcation
df_counts = pd.read_csv('../test_models/seirx_1500/data/roc/df_bif_pred_counts_x_early.csv')

# Make ROC fig
fig_roc = make_roc_figure(df_roc, df_counts, 'd')

# Export ROC fig
fig_roc.write_image('figures/temp_roc.png', scale=scale)


# Make inset fig
fig_inset = make_bar_inset(df_counts)
# fig_inset.update_yaxes(range=[0,40])

# Export inset fig
fig_inset.write_image('figures/temp_inset.png',scale=scale)

# Combine figs and export
path_roc = 'figures/temp_roc.png'
path_inset = 'figures/temp_inset.png'
path_out = 'figures/roc_individual/roc_seirx_x_early.png'

combine_roc_inset(path_roc, path_inset, path_out)






#---------
# SEIRX Var x late
#---------
print('Make ROC figure for SEIRx model using late predictions in variable x')

# Import ROC data
df_roc = pd.read_csv('../test_models/seirx_1500/data/roc/df_roc_seirx_x_late.csv')

# Import counts of favoured bifurcation
df_counts = pd.read_csv('../test_models/seirx_1500/data/roc/df_bif_pred_counts_x_late.csv')

# Make ROC fig
fig_roc = make_roc_figure(df_roc, df_counts, 'd')

# Export ROC fig
fig_roc.write_image('figures/temp_roc.png', scale=scale)


# Make inset fig
fig_inset = make_bar_inset(df_counts)
# fig_inset.update_yaxes(range=[0,40])

# Export inset fig
fig_inset.write_image('figures/temp_inset.png',scale=scale)

# Combine figs and export
path_roc = 'figures/temp_roc.png'
path_inset = 'figures/temp_inset.png'
path_out = 'figures/roc_individual/roc_seirx_x_late.png'

combine_roc_inset(path_roc, path_inset, path_out)







#---------
# SEIRX Var I early 
#---------
print('Make ROC figure for SEIRx model using early predictions in variable I')

# Import ROC data
df_roc = pd.read_csv('../test_models/seirx_1500/data/roc/df_roc_seirx_I_early.csv')

# Import counts of favoured bifurcation
df_counts = pd.read_csv('../test_models/seirx_1500/data/roc/df_bif_pred_counts_I_early.csv')

# Make ROC fig
fig_roc = make_roc_figure(df_roc, df_counts, 'd')

# Export ROC fig
fig_roc.write_image('figures/temp_roc.png', scale=scale)


# Make inset fig
fig_inset = make_bar_inset(df_counts)
# fig_inset.update_yaxes(range=[0,40])

# Export inset fig
fig_inset.write_image('figures/temp_inset.png',scale=scale)

# Combine figs and export
path_roc = 'figures/temp_roc.png'
path_inset = 'figures/temp_inset.png'
path_out = 'figures/roc_individual/roc_seirx_I_early.png'

combine_roc_inset(path_roc, path_inset, path_out)






#---------
# SEIRX Var I late
#---------
print('Make ROC figure for SEIRx model using late predictions in variable I')

# Import ROC data
df_roc = pd.read_csv('../test_models/seirx_1500/data/roc/df_roc_seirx_I_late.csv')

# Import counts of favoured bifurcation
df_counts = pd.read_csv('../test_models/seirx_1500/data/roc/df_bif_pred_counts_I_late.csv')

# Make ROC fig
fig_roc = make_roc_figure(df_roc, df_counts, 'd')

# Export ROC fig
fig_roc.write_image('figures/temp_roc.png', scale=scale)


# Make inset fig
fig_inset = make_bar_inset(df_counts)
# fig_inset.update_yaxes(range=[0,40])

# Export inset fig
fig_inset.write_image('figures/temp_inset.png',scale=scale)

# Combine figs and export
path_roc = 'figures/temp_roc.png'
path_inset = 'figures/temp_inset.png'
path_out = 'figures/roc_individual/roc_seirx_I_late.png'

combine_roc_inset(path_roc, path_inset, path_out)







