# -*- coding: utf-8 -*-
"""
Spyder Editor

Script to stack group and label data from across batches

"""


import numpy as np
import pandas as pd
import os
import csv
import sys


# Command line parameters
num_batches=int(sys.argv[1]) # number of batches generated
ts_len = int(sys.argv[2]) # time series length

# List of batch numbers
batch_nums=range(1,num_batches+1)

#----------------------------
# Concatenate label data
#-----------------------------

list_df_labels = []
# Import label dataframes
for i in batch_nums:
    filepath = 'output/ts_{}/batch{}/output_labels/out_labels.csv'.format(ts_len,i)
    df_labels = pd.read_csv(filepath)
    list_df_labels.append(df_labels)

df_labels = pd.concat(list_df_labels).set_index('sequence_ID')

# Export
filepath='output/ts_{}/combined/'.format(ts_len)
if not os.path.exists(filepath):
    os.mkdir(filepath)
df_labels.to_csv(filepath+'labels.csv')




#----------------------------
# Concatenate group data
#-----------------------------

list_df_groups = []
# Import label dataframes
for i in batch_nums:
    filepath = 'output/ts_{}/batch{}/output_groups/groups.csv'.format(ts_len,i)
    df_groups_temp = pd.read_csv(filepath)
    list_df_groups.append(df_groups_temp)

df_groups = pd.concat(list_df_groups).set_index('sequence_ID')

# Export  
filepath='output/ts_{}/combined/'.format(ts_len)
df_groups.to_csv(filepath+'groups.csv')











