#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 12:59:41 2019

@author: tbury

Script to investigate output of auto simulations with some plots

Also investigate EWS of simualtions.

"""




import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import random


filepath = 'output/batch5/'


# Set seed for reproducibility of figures
seed = 5
random.seed(seed)

# Import label data
df_labels = pd.read_csv(filepath+'output_labels/out_labels.csv').set_index('sequence_ID')


# Number of samples to plot
num_samples = 6
# Import trajectories of 10 of each bifurcation at random
fold_id = df_labels[df_labels['class_label']==0].sample(num_samples).index.values
hopf_id = df_labels[df_labels['class_label']==1].sample(num_samples).index.values
branch_id = df_labels[df_labels['class_label']==2].sample(num_samples).index.values
null_id = df_labels[df_labels['class_label']==3].sample(num_samples).index.values



# List of dfs
list_df_ews = []
# Loop through sequence IDs
for i in np.concatenate((fold_id,hopf_id,branch_id,null_id)):
    # Import time seires and EWS
    df_series = pd.read_csv(filepath+'output_sims/tseries'+str(i)+'.csv', index_col='Time')
    df_resids = pd.read_csv(filepath+'output_resids/resids'+str(i)+'.csv', index_col='Time')
#    df_var = pd.read_csv(filepath+'output_var/var'+str(i)+'.csv', index_col='Time')
#    df_ac = pd.read_csv(filepath+'output_ac1/ac'+str(i)+'.csv', index_col='Time')
#    df_skew = pd.read_csv(filepath+'output_skew/skew'+str(i)+'.csv', index_col='Time')
#
    # Join the dataframes
    df_ews = pd.concat([df_series,df_resids],axis=1)
    # Add the label number and the sequence ID
    df_ews['seq_id'] = i
    df_ews['Label'] = df_labels.loc[i]['class_label']
    df_ews.reset_index(inplace=True)
    # Add the df to the list
    list_df_ews.append(df_ews)

# Concatenate dataframes
df_ews = pd.concat(list_df_ews).set_index(['seq_id','Time'])




## Trajecotry plots


ylim=(-3,3)

# Fold trajectories
df_ews[df_ews['Label']==0]['x'].unstack(level=0).plot(
        title='Fold trajectories',
        ylim = ylim)
# Export
plt.savefig('figures/sims_fold.png')

# Hopf trajecotires
df_ews[df_ews['Label']==1]['x'].unstack(level=0).plot(
        title='Hopf trajectories',
        ylim = ylim)
# Export
plt.savefig('figures/sims_hopf.png')


# Branch trajecotires
df_ews[df_ews['Label']==2]['x'].unstack(level=0).plot(
        title='Branch trajectories',
        ylim = ylim)
# Export
plt.savefig('figures/sims_branch.png')


# Null trajecotires
df_ews[df_ews['Label']==3]['x'].unstack(level=0).plot(
        title='Null trajectories',
        ylim = ylim)
# Export
plt.savefig('figures/sims_null.png')







## Variance plots
#df_ews[df_ews['Label']==0]['Variance'].unstack(level=0).plot(
#        title='Variance - Fold trajectories')
#
## Hopf trajecotires
#df_ews[df_ews['Label']==1]['Variance'].unstack(level=0).plot(
#        title='Variance - Hopf trajectories')
#
## Branch trajecotires
#df_ews[df_ews['Label']==2]['Variance'].unstack(level=0).plot(
#        title='Variance - Branch trajectories')
#
## Null trajecotires
#df_ews[df_ews['Label']==3]['Variance'].unstack(level=0).plot(
#        title='Variance - Null trajectories')
#
#
### Autocorrelation plots
#df_ews[df_ews['Label']==0]['Lag-1 AC'].unstack(level=0).plot(
#        title='Lag-1 AC: Fold trajectories')
#
## Hopf trajecotires
#df_ews[df_ews['Label']==1]['Lag-1 AC'].unstack(level=0).plot(
#        title='Lag-1 AC: Hopf trajectories')
#
## Branch trajecotires
#df_ews[df_ews['Label']==2]['Lag-1 AC'].unstack(level=0).plot(
#        title='Lag-1 AC: Branch trajectories')
#
## Null trajecotires
#df_ews[df_ews['Label']==3]['Lag-1 AC'].unstack(level=0).plot(
#        title='Lag-1 AC: Null trajectories')
#
#
#
### Skewness plots
#df_ews[df_ews['Label']==0]['Lag-1 AC'].unstack(level=0).plot(
#        title='Skew: Fold trajectories')
#
## Hopf trajecotires
#df_ews[df_ews['Label']==1]['Lag-1 AC'].unstack(level=0).plot(
#        title='Skew: Hopf trajectories')
#
## Branch trajecotires
#df_ews[df_ews['Label']==2]['Lag-1 AC'].unstack(level=0).plot(
#        title='Skew: Branch trajectories')
#
## Null trajecotires
#df_ews[df_ews['Label']==3]['Lag-1 AC'].unstack(level=0).plot(
#        title='Skew: Null trajectories')
#









