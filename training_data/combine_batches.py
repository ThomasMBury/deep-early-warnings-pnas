# -*- coding: utf-8 -*-
"""
Spyder Editor

Script to:
    Combine all batches into single data files:
        - Put all series files into single directory
        - Concatenate label data
        - Concatenate groups data

"""


import numpy as np
import pandas as pd
import os
import csv
import sys


# Label exernal variables
batch_set=int(sys.argv[1])
num_batches=int(sys.argv[2])

# List of batch numbers
batch_nums=range((batch_set-1)*num_batches+1,batch_set*num_batches+1)

#----------------------------
# Concatenate label data
#-----------------------------

list_df_labels = []
# Import label dataframes
for i in batch_nums:
    filepath = 'output/batch'+str(i)+'/output_labels/out_labels.csv'
    df_labels = pd.read_csv(filepath)
    list_df_labels.append(df_labels)

df_labels = pd.concat(list_df_labels).set_index('sequence_ID')

# Export
filepath='output/combined_{}/'.format(batch_set)
if not os.path.exists(filepath):
    os.mkdir(filepath)
df_labels.to_csv(filepath+'labels.csv')




#----------------------------
# Concatenate group data
#-----------------------------

list_df_groups = []
# Import label dataframes
for i in batch_nums:
    filepath = 'output/batch'+str(i)+'/output_groups/groups.csv'
    df_groups_temp = pd.read_csv(filepath)
    list_df_groups.append(df_groups_temp)

df_groups = pd.concat(list_df_groups).set_index('sequence_ID')

# Export  
filepath='output/combined_{}/'.format(batch_set)
df_groups.to_csv(filepath+'groups.csv')











