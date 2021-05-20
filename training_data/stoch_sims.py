#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 10:05:17 2019

@author: tbury

SCRIPT TO:
Get info from b.out files (AUTO files)
Run stochastic simulations up to bifurcation points for 700 time units
Detect transition point using change-point algorithm
Ouptut time-series of 500 time units prior to transition

"""

import numpy as np
import pandas as pd
import csv
import os

# Function to convert b.out files into readable form
from convert_bifdata import convert_bifdata

    
# Function to simulation model
from sim_model import sim_model


# Function to detect transition point in time series
from trans_detect import trans_detect


# Create model class
class Model():
    pass
 

# Create directory if does not exist
if not os.path.exists('output_sims'):
    os.makedirs('output_sims')
if not os.path.exists('output_labels'):
    os.makedirs('output_labels')
if not os.path.exists('output_counts'):
    os.makedirs('output_counts')

# Variables from bash shell
import sys
hopf_count = int(sys.argv[1])
fold_count = int(sys.argv[2])
branch_count = int(sys.argv[3])
null_h_count = int(sys.argv[4])
null_f_count = int(sys.argv[5])
null_b_count = int(sys.argv[6])
bif_max = int(sys.argv[7])
batch_num = int(sys.argv[8])


# Noise amplitude
sigma_tilde = 0.01
print('Using sigma_tilde value of {}'.format(sigma_tilde))


# Total count of bifurcations in this batch
total_count = hopf_count + fold_count + branch_count + null_h_count + null_f_count + null_b_count + 1    
# Corresponding ID for naming time series file
seq_id = total_count + (batch_num-1)*(4*bif_max)

# Parameter labels
parlabels_a = ['a'+str(i) for i in np.arange(1,11)]
parlabels_b = ['b'+str(i) for i in np.arange(1,11)]
parlabels = parlabels_a + parlabels_b


#----------
# Extract info from b.out files
#–-------------

# Initiate list of models
list_models = []

# Assign attributes to model objects from b.out files
print('Extract data from b.out files')

for j in range(len(parlabels)):
    # Check to see if file exists
    bool_exists = os.path.exists('output_auto/b.out'+parlabels[j])
    if not bool_exists:
        continue

    model_temp = Model()
    
    out = convert_bifdata('output_auto/b.out'+parlabels[j])
        
    # Assign bifurcation properties to model object
    model_temp.bif_param = out['bif_param']
    model_temp.bif_type = out['type']
    model_temp.bif_value = out['value']
    model_temp.branch_vals = out['branch_vals']

    
    # Import parameter values for the model
    with open('output_model/pars.csv') as csvfile:
        pars_raw = list(csv.reader(csvfile))
    par_list = [float(p[0]) for p in pars_raw]
    par_dict = dict(zip(parlabels,par_list))
    # Assign parameters to model object
    model_temp.pars = par_dict
    
    
    # Import equilibrium data as an array
    with open('output_model/equi.csv') as csvfile:
        equi_raw = list(csv.reader(csvfile))   
           
    equi_list = [float(e[0]) for e in equi_raw]
    equi_array = np.array(equi_list)
    # Assign equilibria to model object
    model_temp.equi_init = equi_array
    
    # Import recovery rate
    with open('output_model/rrate.csv') as csvfile:
        rrate_raw = list(csv.reader(csvfile))          
    rrate = float(rrate_raw[0][0])
 
    # Add model to list
    list_models.append(model_temp)
    

# Separate models into their bifurcation types
hb_models = [model for model in list_models if model.bif_type == 'HB']
bp_models = [model for model in list_models if model.bif_type == 'BP']
lp_models = [model for model in list_models if model.bif_type == 'LP']





#-------------------
## Simulate models
#------------------
    
# Construct noise as in Methods
rv_tri = np.random.triangular(0.75,1,1.25)
# rv_tri = 1 # temporary
sigma = np.sqrt(2*rrate) * sigma_tilde * rv_tri


# Only simulate bifurcation types that have count below bif_max

#Split bif total into 3 parts for different null trajectories
bif_null_totals = [bif_max//3, bif_max//3, bif_max-2*(bif_max//3)]
# Create booleans
[hopf_sim, fold_sim, branch_sim] = np.array([hopf_count, fold_count, branch_count]) < bif_max
[null_h_sim, null_f_sim, null_b_sim] = np.array([null_h_count, null_f_count, null_b_count]) < bif_null_totals



print('Begin simulating model up to bifurcation points')
# Loop through model configurations (different bifurcation params)
for i in range(len(list_models)):
    model = list_models[i]
    
    # Pick sample spacing randomly from [0.1,0.2,...,1]
    dt_sample = np.random.choice(np.arange(1,11)/10)
    # Number of points in simulation data
    series_len = 700
    
    # Simulate a null_h trajectory
    if null_h_sim and (model.bif_type == 'HB'):
        print('Simulating a Hopf Null trajectory with noise amplitude {}'.format(sigma))
        df_out = sim_model(model, dt_sample=dt_sample, series_len=series_len,
                           sigma=sigma, null_sim=True,
                           null_location=0)
        # Detect transition point (if none then outputs end point)
        trans_time = trans_detect(df_out)
        # Only if trans_time > 500, keep and cut trajectory
        if trans_time > 500:
            df_cut = df_out.loc[trans_time-500:trans_time-1].reset_index()
            # Have time-series start at time t=0
            df_cut['Time'] = df_cut['Time']-df_cut['Time'][0]
            df_cut.set_index('Time', inplace=True)
            # Export
            df_cut[['x']].to_csv('output_sims/tseries'+str(seq_id)+'.csv')
            df_label = pd.DataFrame([3])
            df_label.to_csv('output_labels/label'+str(seq_id)+'.csv',
                            header=False, index=False)
            
            null_h_count += 1
            total_count += 1
            seq_id += 1
            # Allow a maximum of one Null simulation for model
            null_h_sim = False
            print('   Achieved 500 steps - exporting')
        else:
        	print('   Transitioned before 500 steps - no export')
        

    
    # Simulate a null_f trajectory
    if null_f_sim and (model.bif_type == 'LP'):
        print('Simulating a Fold Null trajectory with noise amplitude {}'.format(sigma))
        df_out = sim_model(model, dt_sample=dt_sample, series_len=series_len,
                           sigma=sigma, null_sim=True,
                           null_location=0)
        # Detect transition point (if none then outputs end point)
        trans_time = trans_detect(df_out)
        # Only if trans_time > 500, keep and cut trajectory
        if trans_time > 500:
            df_cut = df_out.loc[trans_time-500:trans_time-1].reset_index()
            # Have time-series start at time t=0
            df_cut['Time'] = df_cut['Time']-df_cut['Time'][0]
            df_cut.set_index('Time', inplace=True)
            # Export
            df_cut[['x']].to_csv('output_sims/tseries'+str(seq_id)+'.csv')
            df_label = pd.DataFrame([3])
            df_label.to_csv('output_labels/label'+str(seq_id)+'.csv',
                            header=False, index=False)
            
            null_f_count += 1
            total_count += 1
            seq_id += 1
            # Allow a maximum of one Null simulation for model
            null_f_sim = False
            print('   Achieved 500 steps - exporting')
        else:
        	print('   Transitioned before 500 steps - no export')



        
    # Simulate a null_b trajectory
    if null_b_sim and (model.bif_type == 'BP'):
        print('Simulating a Branch Null trajectory with noise amplitude {}'.format(sigma))
        df_out = sim_model(model, dt_sample=dt_sample, series_len=series_len,
                           sigma=sigma, null_sim=True,
                           null_location=0)
        # Detect transition point (if none then outputs end point)
        trans_time = trans_detect(df_out)
        # Only if trans_time > 500, keep and cut trajectory
        if trans_time > 500:
            df_cut = df_out.loc[trans_time-500:trans_time-1].reset_index()
            # Have time-series start at time t=0
            df_cut['Time'] = df_cut['Time']-df_cut['Time'][0]
            df_cut.set_index('Time', inplace=True)
            # Export
            df_cut[['x']].to_csv('output_sims/tseries'+str(seq_id)+'.csv')
            df_label = pd.DataFrame([3])
            df_label.to_csv('output_labels/label'+str(seq_id)+'.csv',
                            header=False, index=False)
            
            null_b_count += 1
            total_count += 1
            seq_id += 1
            # Allow a maximum of one Null simulation for model
            null_b_sim = False
            print('   Achieved 500 steps - exporting')
        else:
        	print('   Transitioned before 500 steps - no export')

    # Simulate a Hopf trajectory
    if hopf_sim and (model.bif_type == 'HB'):
        print('Simulating a Hopf trajectory')
        df_out = sim_model(model, dt_sample=dt_sample, series_len=series_len,
                           sigma=sigma)
        # Detect transition point
        trans_time = trans_detect(df_out)
        # Only if trans_time > 500, keep and cut trajectory
        if trans_time > 500:
            df_cut = df_out.loc[trans_time-500:trans_time-1].reset_index()
            # Have time-series start at time t=0
            df_cut['Time'] = df_cut['Time']-df_cut['Time'][0]
            df_cut.set_index('Time', inplace=True)
            # Export
            df_cut[['x']].to_csv('output_sims/tseries'+str(seq_id)+'.csv')
            df_label = pd.DataFrame([1])
            df_label.to_csv('output_labels/label'+str(seq_id)+'.csv',
                            header=False, index=False)
            
            hopf_count += 1
            total_count += 1
            seq_id += 1
            # Allow a maximum of one Hopf bifurcation for model
            hopf_sim = False
            print('   Achieved 500 steps - exporting')
        else:
        	print('   Transitioned before 500 steps - no export') 
            
    # Simulate a Fold trajectory
    if fold_sim and (model.bif_type == 'LP'):
        print('Simulating a Fold trajectory')
        df_out = sim_model(model, dt_sample=dt_sample, series_len=series_len,
                           sigma=sigma)
        # Detect transition point
        trans_time = trans_detect(df_out)
        # Only if trans_time > 500, keep and cut trajectory
        if trans_time > 500:
            df_cut = df_out.loc[trans_time-500:trans_time-1].reset_index()
            # Have time-series start at time t=0
            df_cut['Time'] = df_cut['Time']-df_cut['Time'][0]
            df_cut.set_index('Time', inplace=True)
            # Export
            df_cut[['x']].to_csv('output_sims/tseries'+str(seq_id)+'.csv')
            df_label = pd.DataFrame([0])
            df_label.to_csv('output_labels/label'+str(seq_id)+'.csv',
                            header=False, index=False)
            
            fold_count += 1
            total_count += 1
            seq_id += 1
            # Allow a maximum of one fold bifurcation from model
            fold_sim = False
            print('   Achieved 500 steps - exporting')
        else:
        	print('   Transitioned before 500 steps - no export')


    # Simulate a Branch point trajectory
    if branch_sim and (model.bif_type == 'BP'):
        print('Simulating a branch point')
        df_out = sim_model(model, dt_sample=dt_sample, series_len=series_len,
                           sigma=sigma)
        # Detect transition point
        trans_time = trans_detect(df_out)
        
        # Only if trans_time > 500, keep and cut trajectory
        if trans_time > 500:
            df_cut = df_out.loc[trans_time-500:trans_time-1].reset_index()
            # Have time-series start at time t=0
            df_cut['Time'] = df_cut['Time']-df_cut['Time'][0]
            df_cut.set_index('Time', inplace=True)
            # Export
            df_cut[['x']].to_csv('output_sims/tseries'+str(seq_id)+'.csv')
            df_label = pd.DataFrame([2])
            df_label.to_csv('output_labels/label'+str(seq_id)+'.csv',
                            header=False, index=False)
            
            branch_count += 1
            total_count += 1
            seq_id += 1
            # Allow a maximum of one branch point from model
            branch_sim = False
            print('   Achieved 500 steps - exporting')
        else:
        	print('   Transitioned before 500 steps - no export')

print('Simulations finished\n')
# Export updated counts of bifurcations for the bash scriptr
list_counts = np.array([hopf_count, fold_count, branch_count, null_h_count, null_f_count, null_b_count])
np.savetxt('output_counts/list_counts.txt',list_counts, fmt='%i')
    









    
