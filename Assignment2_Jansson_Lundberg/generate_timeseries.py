# -*- coding: utf-8 -*-
"""
Created on Tue May 23 09:26:57 2023

@author: ielmartin
"""

import numpy as np
import pandas as pd
import pandapower as pp
import pandapower.plotting as plot
from pandapower.timeseries import DFData


def timeseries(net, timesteps = 10, scenario = False):
    
    timeseries_loads_p = pd.DataFrame()
    timeseries_loads_q = pd.DataFrame()
    timeseries_gens = pd.DataFrame()
    
    # define min and max change of nominal output (p and q)
    nom_change_max = 0.5
    nom_change_min = 0.2
    
    # noise parameters (for load and gen timeseries)
    mean = 0
    std_dev = 0.1
    
    # determine nominal p and q for loads depending on scenario choice
    for index, load in net.load.iterrows():
        if scenario == 'high load':
            nominal_p = load['p_mw'] + np.random.uniform(nom_change_min*load['p_mw'], nom_change_max*load['p_mw']) 
            nominal_q = load['q_mvar'] + np.random.uniform(nom_change_min*load['q_mvar'], nom_change_max*load['q_mvar'])
            
            
        elif scenario == 'low load':
            nominal_p = load['p_mw'] - np.random.uniform(nom_change_min*load['p_mw'], nom_change_max*load['p_mw']) 
            nominal_q = load['q_mvar'] - np.random.uniform(nom_change_min*load['q_mvar'], nom_change_max*load['q_mvar'])
        
        else:
            nominal_p = load['p_mw']
            nominal_q = load['q_mvar'] 

         
        # create timeseries by adding noise to nominal values     
        noise_p = np.random.normal(mean, std_dev*nominal_p, size = timesteps)
        noise_q = np.random.normal(mean, std_dev*nominal_q, size = timesteps)
        
        timeseries_loads_p[load['name']] = np.ones(timesteps)*nominal_p + noise_p
        timeseries_loads_q[load['name']] = np.ones(timesteps)*nominal_q + noise_q
        
     # determine nominal p for generators depending on scenario choice      
    for index, gen in net.gen.iterrows():
        if scenario == 'gen disconnect' and gen['name']=='Winlock':
            gen['in_service'] = False
            
        nominal_p = gen['p_mw']
        
        noise_p = np.random.normal(mean, std_dev*nominal_p, size = timesteps)
        timeseries_gens[gen['name']] = np.ones(timesteps)*nominal_p + noise_p
    
    # disconnect line depending on scenario choice
    for index, line in net.line.iterrows():
        if scenario == 'line disconnect' and line['name']=='Troy-Maple':
            line['in_service'] = False
     
    
    # create timeseries datasource for timeseries simulation in PandaPower
    load_profiles_p = DFData(timeseries_loads_p)
    load_profiles_q = DFData(timeseries_loads_q)
    gen_profiles = DFData(timeseries_gens)
    
    

    return net, load_profiles_p, load_profiles_q, gen_profiles
    
