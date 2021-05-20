#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 12:06:16 2019

Write function to simulate models

@author: Thomas Bury
"""

import numpy as np
import pandas as pd

    
def sim_model(model, dt_sample=1, series_len=500, sigma=0.1, null_sim=False, null_location=0):
    '''
    Function to run a stochastic simulation of model up to bifurcation point
    Input:
        model (class) : contains details of model to simulate
        dt_sample : time between sampled points (must be a multiple of 0.01)
        series_len : number of points in time series
        sigma (float) : amplitude factor of GWN - total amplitude also
            depends on parameter values
        null_sim (bool) : Null simulation (bifurcation parameter fixed) or
            transient simulation (bifurcation parameter increments to bifurcation point)
        null_location (float) : Value in [0,1] to determine location along bifurcation branch
            where null is simulated. Value is proportion of distance to the 
            bifurcation from initial point (0 is initial point, 1 is bifurcation point)
    Output:
        DataFrame of trajectories indexed by time
    '''

    
    # Simulation parameters
    dt = 0.01
    t0 = 0
    tburn = 100 # burn-in period
#   seed = 0 # random number generation 
    
    # Bifurcation point of model
    bcrit = model.bif_value # bifurcation point
    
    # Initial value of bifurcation parameter
    bl = model.pars[model.bif_param]
    
    # If a null simulation, simulate at a fixed value of b, given by b_null
    if null_sim:
        b_null = bl + null_location*(bcrit-bl)
        # Set bl and bh for simulation as equal to b_null
        bl = b_null
        bh = b_null
    
    # If a transient simulation, let b go from bl to bh, where bh is bifurcation point
    else:
        bh = bcrit
    
    s0 = model.equi_init    # initial condition
    
    # Parameter labels
    parlabels_a = ['a'+str(i) for i in np.arange(1,11)]
    parlabels_b = ['b'+str(i) for i in np.arange(1,11)]
    
    # Model equations

    def de_fun(s,pars):
        '''
        Input:
        s is state vector
        pars is dictionary of parameter values
        
        Output:
        array [dxdt, dydt]
        
        '''
        
        # Obtain model parameters from dictionary
        pars_a = np.array([pars[k] for k in parlabels_a])
        pars_b = np.array([pars[k] for k in parlabels_b])
        
        # Polynomial forms up to third order
        x=s[0]
        y=s[1]
        polys = np.array([1,x,y,x**2,x*y,y**2,x**3,x**2*y,x*y**2,y**3])
        
        dxdt = np.dot(pars_a, polys)
        dydt = np.dot(pars_b, polys)
                      
        return np.array([dxdt, dydt])
        
        
    
    # Initialise arrays to store single time-series data
    t = np.arange(t0, series_len*dt_sample, dt)
    s = np.zeros([len(t),2])
    
   
    # Set up bifurcation parameter b, that increases linearly in time from bl to bh
    b = pd.Series(np.linspace(bl,bh,len(t)),index=t)
#    # Time at which bifurcation occurs
#    if bh > bcrit:
#        tbif = b[b > bcrit].index[1]
#        print('Bifurcation occurs at time {}'.format(tbif))
#    else:
#        print('Bifurcation not passed')
    
    

    ## Implement Euler Maryuyama for stocahstic simulation
    
    # Create brownian increments (s.d. sqrt(dt))
    dW_burn = np.random.normal(loc=0, scale=sigma*np.sqrt(dt), size = [int(tburn/dt),2])
    dW = np.random.normal(loc=0, scale=sigma*np.sqrt(dt), size = [len(t/dt),2])
    
    # Run burn-in period on s0
    for i in range(int(tburn/dt)):
        s0 = s0 + de_fun(s0, model.pars)*dt + dW_burn[i]
        
    # Initial condition post burn-in period
    s[0] = s0
    
    # Run simulation
    for i in range(len(t)-1):
        # Update bifurcation parameter
        pars = dict(model.pars)
        pars[model.bif_param] = b.iloc[i]
        s[i+1] = s[i] + de_fun(s[i],pars)*dt + dW[i]
            
    # Store series data in a DataFrame
    data = {'Time': t,'x': s[:,0],'y': s[:,1], 'b':b.values}
    df_traj = pd.DataFrame(data)
    
    # Filter dataframe according to spacing
    df_traj_filt = df_traj.iloc[0::int(dt_sample/dt)].copy()
    
    # Replace time column with integers for compatibility
    # with trans_detect
    df_traj_filt['Time'] = np.arange(0,series_len)
    df_traj_filt.set_index('Time', inplace=True)

    
    return df_traj_filt
    
    

