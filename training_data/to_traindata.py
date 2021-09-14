# -*- coding: utf-8 -*-
"""
Spyder Editor

Choose a ratio for training/validation/testing here.

Script to:
    Take in all label files and output single list of labels
    Split data into a ratio for trianing/validation/testing

"""


import numpy as np
import pandas as pd
import os
import csv
import sys


# External arguments
bif_total = int(sys.argv[1])
batch_num = int(sys.argv[2])


#----------------------------
# Convert label files into single csv file
#-----------------------------

list_labels = []
# Import all label files
for i in np.arange(4*bif_total)+1 + 4*bif_total*(batch_num-1):
    filename = 'output_labels/label'+str(i)+'.csv'
    # Import label
    with open(filename) as csvfile:
        label = list(csv.reader(csvfile))
        label_int = int(label[0][0])
    # Add label to list
    list_labels.append(label_int)

# Make an array of the labels
ar_labels = np.array(list_labels)

# Make an array for the indices
ar_index = np.arange(4*bif_total)+1 + 4*bif_total*(batch_num-1)

# Combine into a DataFrame for export
df_labels = pd.DataFrame({'sequence_ID':ar_index, 'class_label':ar_labels})

# Export to csv
df_labels.to_csv('output_labels/out_labels.csv', header=True,index=False)




#----------------------------
# Create groups file in ratio for training:validation:testing
#-----------------------------

# Create the file groups.csv with headers (sequence_ID, dataset_ID)
# Use numbers 1 for training, 2 for validation and 3 for testing
# Use raito 38:1:1

# Make output folder to split
if not os.path.exists('output_groups'):
    os.makedirs('output_groups')
    

# Collect Fold bifurcations (label 0)
df_fold = df_labels[df_labels['class_label']==0].copy()
# Collect Hopf bifurcations (label 1)
df_hopf = df_labels[df_labels['class_label']==1].copy()
# Collect Branch points (label 2)
df_branch = df_labels[df_labels['class_label']==2].copy()
# Collect Null labels (label 3)
df_null = df_labels[df_labels['class_label']==3].copy()

# Check they all have the same length
assert len(df_fold) == len(df_hopf)
assert len(df_hopf) == len(df_branch)
assert len(df_branch) == len(df_null)


# Compute number of bifurcations for each group
num_valid = int(np.floor(bif_total*0.04))
num_test = int(np.floor(bif_total*0.01))
num_train = bif_total - num_valid - num_test

# Create list of group numbers
group_nums = [1]*num_train + [2]*num_valid + [3]*num_test

# Assign group numbers to each bifurcation category
df_fold['dataset_ID'] = group_nums
df_hopf['dataset_ID'] = group_nums
df_branch['dataset_ID'] = group_nums
df_null['dataset_ID'] = group_nums

# Concatenate dataframes and select relevant columns
df_groups = pd.concat([df_fold,df_hopf,df_branch,df_null])[['sequence_ID','dataset_ID']]
# Sort rows by sequence_ID
df_groups.sort_values(by=['sequence_ID'], inplace=True)

# Export to csv
df_groups.to_csv('output_groups/groups.csv', header=True,index=False)





