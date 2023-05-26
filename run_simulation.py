# -*- coding: utf-8 -*-
"""
Created on Wed May 24 18:29:03 2023

@author: ielmartin
"""

import numpy as np
import pandas as pd
import pandapower as pp
import pandapower.plotting as plot
from pandapower.timeseries import OutputWriter
from pandapower.timeseries import run_timeseries
from pandapower.control import ConstControl

from panda_network import create_network
from generate_timeseries import timeseries


def create_controllers(net, ds1, ds2, ds3):
    for index, load in net.load.iterrows():
        ConstControl(net, element='load', variable='p_mw', element_index=[index],
                 data_source=ds1, profile_name=load['name'])
        ConstControl(net, element='load', variable='q_mvar', element_index=[index],
                 data_source=ds2, profile_name=load['name'])
        
    for index, gen in net.gen.iterrows():
        ConstControl(net, element='gen', variable='p_mw', element_index=[index],
                 data_source=ds3, profile_name=gen['name'])


#----MAIN PART OF CODE----
#generate pandapower network
net = create_network()

#choose scenario
# scenarios: high load, low load, gen disconnect, line disconnect
scenario = 'line disconnect'

#choose no of timesteps
no_timesteps = 10

#generate timeseries and update network config depending on scenario choice
net, load_profiles_p, load_profiles_q, gen_profiles = timeseries(net, no_timesteps, scenario)

# initate load and generation profiles for timeseries simulation
create_controllers(net, load_profiles_p, load_profiles_q, gen_profiles)

#log results in current folder
ow = OutputWriter(net, output_path="./", output_file_type=".csv")
#initiate log_variables in OutputWriter didn't work. Therefore ugly workaround below
ow.log_variable('res_bus', 'va_degree')
ow.remove_log_variable('res_line','loading_percent')

#run timeseries simulation
time_steps = range(0, no_timesteps)
run_timeseries(net, time_steps)