'''
Code to generate ensemble predictions from the DL classifiers
on a give time series of residuals

'''


import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

import gc
import numpy as np
import pandas as pd
import random
import sys
import itertools

import tensorflow as tf
from tensorflow.keras.models import load_model
from datetime import datetime

random.seed(datetime.now())


'''
10 of the DL models are trained on training set data that are censored (padded) 
on the left hand side only, hence they are trained on data that always includes 
the transition.  The other 10 were trained on training set data that are 
censored on both left and right, hence they do not include the transition.
kk runs from 1 to 10 and denotes the index of the 10 models of each type.
model_type is 1 or 2.  1 denotes the model that is trained on data censored on 
both the left and right.  2 is the model trained on data censored on the left only. 

'''


# Filepath to residual time series to make predictions on 
filepath = '../test_models/may_fold_1500/data/resids/may_fold_1500_resids.csv'

# Filepath to export ensemble DL predictions to
filepath_out = '../test_models/may_fold_1500/data/ml_preds_test/ensemble_trend_probs_may_fold_forced_1_len1500.csv'

# Type of classifier to use (1500 or 500)
ts_len=1500

'''  
The following two parameters control how many sample points along the 
timeseries are used, and the length between them.  For instance, for an input 
time series equal to or less then length 1500, mult_factor=10 and 
pad_samples=150 means that it will do the unveiling in steps of 10 datapoints, 
at 150 evenly spaced points across the entire time series (150 x 10 = 1500).
Needs to be adjusted according to whether you are using the trained 500 length 
or 1500 length classifier.
'''

# Steps of datapoints in between each DL prediction
mult_factor = 10

# Total number of DL predictions to make
# Use 150 for length 1500 time series. Use 50 for length 500 time series.
pad_samples = 150



# Load residual time series data
df = pd.read_csv(filepath).dropna()
resids = df['Residuals'].values.reshape(1,-1,1)
# Length of inupt time series
seq_len = len(df)



def get_dl_predictions(resids, model_type, kk):
    
    '''
    Generate DL prediction time series on resids
    from DL classifier with type 'model_type' and index kk.
    '''
        
    # Setup file to store DL predictions
    predictions_file_name = 'predictions/y_pred_{}_{}.csv'.format(kk,model_type)
    f1 = open(predictions_file_name,'w')

    # Load in specific DL classifier
    model_name = 'best_models/best_model_{}_{}_len{}.pkl'.format(kk,model_type,ts_len)
    model = load_model(model_name)
    
    # Loop through each possible length of padding
    # Start with revelaing the DL algorith only the earliest points
    for pad_count in range(pad_samples-1, -1, -1):
    
        temp_ts = np.zeros((1,ts_len,1))
    
        ts_gap = ts_len-seq_len
        pad_length = mult_factor*pad_count
    
        if pad_length + ts_gap > ts_len:
            zero_range = ts_len
        else:
            zero_range = pad_length + ts_gap
        
        if zero_range == ts_len:
            # Set all ML predictions to zero
            y_pred = np.zeros(4).reshape(1,4)
        else:
            for j in range(0, zero_range):
                temp_ts[0,j] = 0
            for j in range(zero_range, ts_len):
                temp_ts[0,j] = resids[0,j-zero_range]
    
            # normalizing inputs: take averages, since the models were also trained on averaged data. 
            values_avg = 0.0
            count_avg = 0
            for j in range (0,ts_len):
                if temp_ts[0,j] != 0:
                    values_avg = values_avg + abs(temp_ts[0,j])
                    count_avg = count_avg + 1
            if count_avg != 0:
                values_avg = values_avg/count_avg
            for j in range (0,ts_len):
                if temp_ts[0,j] != 0:
                    temp_ts[0,j] = temp_ts[0,j]/values_avg
            
            # Compute DL prediction
            y_pred = model.predict(temp_ts)
            
                    
    
        # Write predictions to file
        np.savetxt(f1, y_pred, delimiter=',')
        print('Predictions computed for padding={}'.format(pad_count*mult_factor))
        
    # Delete model and do garbage collection to free up RAM
    tf.keras.backend.clear_session()
    if zero_range != ts_len:
        del model
    gc.collect()
    f1.close()
    
    return 



# Compute DL predictions from all 20 trained models
for model_type in [1,2]:                                
    for kk in np.arange(1,11):
        print('Compute DL predictions for model_type={}, kk={}'.format(
            model_type,kk))
        
        get_dl_predictions(resids, model_type, kk)




# Compute average prediction among all 20 DL classifiers
list_df_preds = []
for model_type in [1,2]:
    for kk in np.arange(1,11):
        filename = 'predictions/y_pred_{}_{}.csv'.format(kk,model_type)
        df_preds = pd.read_csv(filename,header=None)
        df_preds['time_index'] = df_preds.index
        df_preds['model_type'] = model_type
        df_preds['kk'] = kk
        list_df_preds.append(df_preds)
    

# Concatenate
df_preds_all = pd.concat(list_df_preds).reset_index(drop=True)

# Compute mean over all predictions
df_preds_mean = df_preds_all.groupby('time_index').mean()

# Export predictions
df_preds_mean[[0,1,2,3]].to_csv(filepath_out,index=False,header=False)




