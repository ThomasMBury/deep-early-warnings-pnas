# python code for training of machine learning algorithm, using keras library 

import os
import zipfile

os.environ['KMP_DUPLICATE_LIB_OK']='True'

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

random.seed(datetime.now())

# job number can be appended to file names in case you want to generate ensemble predictions
job_number = int(sys.argv[1])

# keeps track of training metrics
f1_name = "training_results.txt"
f2_name = "training_results.csv"

f_results= open(f1_name, "a+")
f_results2 = open(f2_name, "a+")

set_size = 500001  # set to size of time series library plus 1
seq_len = 500  # length of input time series 

pad_left = 0 # can pad left or right with zeros to replicate unmasking approach used in the paper
pad_right = 0 

# zipfile of time series 
zf = zipfile.ZipFile('/work/cbauch/EWS/Training17a/Archive.zip')
text_files = zf.infolist()
sequences = list()

for i in range (1,set_size):
    df = pandas.read_csv(zf.open('resids'+str(i)+'.csv'))
    keep_col = ['Residuals']
    new_f = df[keep_col]
    values = new_f.values
    
    sequences.append(values)

sequences = np.array(sequences)

# training labels file
targets = pandas.read_csv('/work/cbauch/EWS/Training17a/labels.csv')
targets = targets.values[:,1]

# train/validation/test split denotations
groups = pandas.read_csv('/work/cbauch/EWS/Training17a/groups.csv', header=0)
groups = groups.values[:,1]

#Padding input sequences

for i in range(set_size-1):
    pad_length = int(pad_left*random.uniform(0, 1))
    for j in range(0,pad_length):     
        sequences[i,j] = 0

    pad_length = int(pad_right*random.uniform(0, 1))
    for j in range(seq_len - pad_length, seq_len):
        sequences[i,j] = 0

# normalizing input time series by the average. 
for i in range(set_size-1):
    values_avg = 0.0
    count_avg = 0
    for j in range (0,seq_len):
        if sequences[i,j] != 0:
            values_avg = values_avg + abs(sequences[i,j])
            count_avg = count_avg + 1
    if count_avg != 0:
        values_avg = values_avg/count_avg
        for j in range (0,seq_len):
            if sequences[i,j] != 0:
                sequences[i,j] = sequences[i,j]/values_avg

final_seq = sequences

# apply train/test/validation labels

train = [final_seq[i] for i in range(len(groups)) if (groups[i]==1)]
validation = [final_seq[i] for i in range(len(groups)) if groups[i]==2]
test = [final_seq[i] for i in range(len(groups)) if groups[i]==3]

train_target = [targets[i] for i in range(len(groups)) if (groups[i]==1)]
validation_target = [targets[i] for i in range(len(groups)) if groups[i]==2]
test_target = [targets[i] for i in range(len(groups)) if groups[i]==3]  

train = np.array(train)
validation = np.array(validation)
test = np.array(test)

train_target = np.array(train_target)

validation_target = np.array(validation_target)

test_target = np.array(test_target)

# hyperparameter settings

CNN_layers = 1
LSTM_layers = 0  
pool_size_param = 2
learning_rate_param = 0.0005     
batch_param = 1000
dropout_percent = 0.10
filters_param = 50  
mem_cells = 50
mem_cells2 = 10
kernel_size_param = 12
epoch_param = 1500
initializer_param = 'lecun_normal'

# if you want to train multiple identical models, kk is the label for the files
for kk in range(1,2):

    model = Sequential()

# add layers
    if CNN_layers == 1:
        model.add(Conv1D(filters=filters_param, kernel_size=kernel_size_param, activation='relu', padding='same',input_shape=(seq_len, 1),kernel_initializer = initializer_param))
    elif CNN_layers == 2:
        model.add(Conv1D(filters=filters_param, kernel_size=kernel_size_param, activation='relu', padding='same',input_shape=(seq_len, 1)))
        model.add(Conv1D(filters=2*filters_param, kernel_size=kernel_size_param, activation='relu', padding='same'))
        
    model.add(Dropout(dropout_percent))
    model.add(MaxPooling1D(pool_size=pool_size_param))
    
    model.add(LSTM(mem_cells, return_sequences=True,kernel_initializer = initializer_param))
    model.add(Dropout(dropout_percent))
    
    if LSTM_layers == 1:
        model.add(LSTM(mem_cells, return_sequences=True,kernel_initializer = initializer_param))
        model.add(Dropout(dropout_percent))
    elif LSTM_layers == 2:
        model.add(LSTM(mem_cells, return_sequences=True))
        model.add(LSTM(mem_cells, return_sequences=True))
        model.add(Dropout(dropout_percent))
    
    model.add(LSTM(mem_cells2,kernel_initializer = initializer_param))
    model.add(Dropout(dropout_percent))
    model.add(Dense(4, activation='softmax',kernel_initializer = initializer_param))
    
    model_index = kk

    model_name = "best_model"

    a_name="best_model_"
    b_name = kk
    c_name = "_"
    d_name = job_number
    e_name = ".pkl"
    model_name = a_name+str(b_name)+c_name+str(d_name)+e_name

    adam = Adam(lr=learning_rate_param)
    chk = ModelCheckpoint(model_name, monitor='val_acc', save_best_only=True, mode='max', verbose=1)
    model.compile(loss='sparse_categorical_crossentropy', optimizer=adam, metrics=['accuracy', 'val_acc', 'sparse_categorical_accuracy'])
    history = model.fit(train, train_target, epochs=epoch_param, batch_size=batch_param, callbacks=[chk], validation_data=(validation,validation_target))

    model = load_model(model_name)

# generate test metrics
    from sklearn.metrics import accuracy_score
    test_preds = model.predict_classes(test)
    accuracy_score(test_target, test_preds)

    from sklearn.metrics import f1_score
    from sklearn.metrics import confusion_matrix
    from sklearn.metrics import precision_score
    from sklearn.metrics import recall_score
    from sklearn.metrics import classification_report 
    from sklearn import learning_curve
    
    print(classification_report(test_target, test_preds, digits=3))

    print(history.history['accuracy'])
    print(history.history['val_accuracy'])
    print(history.history['loss'])
    print(history.history['val_loss'])
    print("F1 score:",f1_score(test_target, test_preds, average='macro'))
    print("Precision: ",precision_score(test_target, test_preds, average="macro"))
    print("Recall: ",recall_score(test_target, test_preds, average="macro"))    
    print("Confusion matrix: \n",confusion_matrix(test_target, test_preds))
    
    f_results.write("Simulation %d macro f1: %f. macro avg precision %f.  macro avg recall %f. Kernel size %d.  Filters %d.  Batch size %d.  Epochs %d.  seq_len %d.  Set size %d.  Mem_cells %d. Mem_cells2 %d. dropout %f. CNN layers %d, LSTM layers %d, pool_size_param %d, learning_rate_param %f.  initializer %s. pad_left %d.  pad_right %d \r\n" % (kk, f1_score(test_target, test_preds, average='macro'),precision_score(test_target, test_preds, average='macro'),recall_score(test_target, test_preds, average='macro'),kernel_size_param,filters_param,batch_param,epoch_param,seq_len,set_size-1,mem_cells,mem_cells2,dropout_percent,CNN_layers,LSTM_layers,pool_size_param,learning_rate_param,initializer_param,pad_left, pad_right))
    f_results.flush()
    
    f_results2.write("%d, %f, %f, %f, %d, %d, %d, %d, %d, %d, %d, %d, %f, %d, %d, %d, %f, %s, %d, %d \r\n" % (kk, f1_score(test_target, test_preds, average='macro'),precision_score(test_target, test_preds, average='macro'),recall_score(test_target, test_preds, average='macro'),kernel_size_param,filters_param,batch_param,epoch_param,seq_len,set_size-1,mem_cells,mem_cells2,dropout_percent,CNN_layers,LSTM_layers,pool_size_param,learning_rate_param,initializer_param,pad_left, pad_right))
    f_results2.flush()

f_results.close() 
f_results2.close() 

