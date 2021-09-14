# Code to call up and run trained DL models.  Generates an ensemble prediction from 20 different models of two different types. 

import os
import zipfile

os.environ['KMP_DUPLICATE_LIB_OK']='True'

import gc
import pandas
import numpy as np
import matplotlib.pyplot as plt
import random
import sys
import math 
from os import listdir

import tensorflow as tf
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Conv1D
from tensorflow.keras.layers import MaxPooling1D
from tensorflow.keras.preprocessing.sequence import pad_sequences

from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import ModelCheckpoint
from datetime import datetime

from numpy import array
from numpy import argmax

from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import classification_report

#print ("All packages imported")

random.seed(datetime.now())

# This code generates a time series of the DL classification probabilities (the EWS timeseries) by progressively unveiling more of the input residual time series from the start to finish, through padding 
# the input time series.  The following two parameters control how many samples points along the timeseries are used, and the length between them.  For instance, for an input time series equal to or less  
# then length 1500, mult_factor=10 and pad_samples=150 means that it will do the unveiling in steps of 10 datapoints, at 150 evenly spaced points across the entire time series (150 x 10 = 1500).
# Needs to be adjusted according to whether you are using the trained 500 length or 1500 length classifier.

mult_factor = 10
pad_samples = 150

# 10 of the DL models were are trained on training set data that are censored (padded) on the left hand side only, hence they are trained on data that
# always includes the transition.  The other 10 were trained on training set data that are censored on both left and right, hence they do not include the transition.
# kk runs from 1 to 10 and denotes the index of the 10 models of each type
# model_type is 1 or 2.  1 denotes the model that is trained on data censored on both the left and right.  2 is the model trained on data censored on the left only. 
# The following lines assume you are running a script that calls all 20 models in succession based on command line inputs for kk and model_type

kk = int(sys.argv[1])
model_type = int(sys.argv[2])

sequences = list()

# input residual time series file that you want to generate EWS for 
# adjust following lines depending on file format 

file_path = 'resids_input_file.csv'

df = pandas.read_csv(file_path)

keep_col = ['Residuals']
new_f = df[keep_col]
values = new_f.values
seq_len = new_f.size

sequences.append(values)
sequences = np.array(sequences)

final_seq = sequences

test =  final_seq

test = np.array(test)

# output timeseries of EWS prediction probabilities 
f1 = open('prediction_probs_output.csv','a')

# unveiling: run through each possible length of padding and generate EWS predictions for each padded time series. 
# start with only presenting the DL algorithms with the very earliest data points. 

for pad_count in range (pad_samples - 1, -1, -1):

# adjust 1500 to 500 if you are using the DL models trained on length 500 time series 
    temp_ts = np.zeros((1,1500,1))

    ts_gap = 1500-seq_len
    pad_length = mult_factor*pad_count

    if pad_length + ts_gap > 1500:
        zero_range = 1500
    else:
        zero_range = pad_length + ts_gap
    
    if zero_range == 1500:
        y_pred = np.zeros(4).reshape(1,4)
    else:    
        for j in range(0, zero_range):
            temp_ts[0,j] = 0
        for j in range(zero_range, 1500):
            temp_ts[0,j] = test[0,j-zero_range]

        # normalizing inputs: take averages, since the models were also trained on averaged data. 
        values_avg = 0.0
        count_avg = 0
        for j in range (0,1500):
            if temp_ts[0,j] != 0:
                values_avg = values_avg + abs(temp_ts[0,j])
                count_avg = count_avg + 1
        if count_avg != 0:
            values_avg = values_avg/count_avg
        for j in range (0,1500):
            if temp_ts[0,j] != 0:
                temp_ts[0,j] = temp_ts[0,j]/values_avg
            
        # need location of trained DL files 
        if model_type == 1:
            a_name="Directory1/best_model_"
        elif model_type == 2:
            a_name="Directory2/best_model_"

        b_name = kk
        c_name = "_"

        if model_type == 1:
            e_name = "1.pkl"
        elif model_type == 2:
            e_name = "2.pkl"
        
        model_name = a_name+str(b_name)+c_name+e_name
            
        model = load_model(model_name)

        y_pred = model.predict(temp_ts)

    if model_type == 1:
        predictions_file_name = 'y_pred_censored_1_null.npy'
    elif model_type == 2:
        predictions_file_name = 'y_pred_censored_2_null.npy'
    elif model_type == 3:
        predictions_file_name = 'y_pred_censored_3_null.npy'
    elif model_type == 4:
        predictions_file_name = 'y_pred_censored_4_null.npy'
                        
    # save predictions

    np.save(predictions_file_name,y_pred)

    np.savetxt(f1, y_pred, delimiter=',', newline=', ')
    f1.write("\n")
    
    tf.keras.backend.clear_session()
    if zero_range != 1500:
        del model
    gc.collect()   

f1.close()


    

