# -*- coding: utf-8 -*-
"""
Created on Tue May 23 08:39:02 2023

@author: ielmartin
"""

import pandas as pd
import pandapower as pp
import pandapower.plotting as plot

def create_network(plot_network=False):
    
    net = pp.create_empty_network()
    #create buses
    bus_voltage = 110
    
    bus1 = pp.create_bus(net, name='Clark',vn_kv=bus_voltage)
    bus2 = pp.create_bus(net, name='Amherst',vn_kv=bus_voltage)
    bus3 = pp.create_bus(net, name='Winlock',vn_kv=bus_voltage)
    bus4 = pp.create_bus(net, name='Bowman',vn_kv=bus_voltage)
    bus5 = pp.create_bus(net, name='Troy',vn_kv=bus_voltage)
    bus6 = pp.create_bus(net, name='Maple',vn_kv=bus_voltage)
    bus7 = pp.create_bus(net, name='Grand',vn_kv=bus_voltage)
    bus8 = pp.create_bus(net, name='Wautaga',vn_kv=bus_voltage)
    bus9 = pp.create_bus(net, name='Cross',vn_kv=bus_voltage)
    
    #create loads
    load5 = pp.create_load(net, bus5, p_mw=90, q_mvar=30, name = net.bus.at[bus5,'name'])
    load7 = pp.create_load(net, bus7, p_mw=100, q_mvar=35, name = net.bus.at[bus7,'name'])
    load9 = pp.create_load(net, bus9, p_mw=125, q_mvar=50, name = net.bus.at[bus9,'name'])
    
    #create generators
    gen1 = pp.create_gen(net, bus1, p_mw=0, name = net.bus.at[bus1,'name'], slack=True)
    gen2 = pp.create_gen(net, bus2, p_mw=163, name = net.bus.at[bus2,'name'])
    gen3 = pp.create_gen(net, bus3, p_mw=85, name = net.bus.at[bus3,'name'])
    
    #create lines
    line_length = 10
    line_type = '149-AL1/24-ST1A 110.0' 
    line14 = pp.create_line(net, bus1, bus4, length_km = line_length, std_type= line_type, name = net.bus.at[bus1,'name']+'-'+net.bus.at[bus4,'name'])
    line28 = pp.create_line(net, bus2, bus8, length_km = line_length, std_type= line_type, name = net.bus.at[bus2,'name']+'-'+net.bus.at[bus8,'name'])
    line36 = pp.create_line(net, bus3, bus6, length_km = line_length, std_type= line_type, name = net.bus.at[bus3,'name']+'-'+net.bus.at[bus6,'name']) 
    line45 = pp.create_line(net, bus4, bus5, length_km = line_length, std_type= line_type, name = net.bus.at[bus4,'name']+'-'+net.bus.at[bus5,'name'])
    line49 = pp.create_line(net, bus4, bus9, length_km = line_length, std_type= line_type, name = net.bus.at[bus4,'name']+'-'+net.bus.at[bus9,'name']) 
    line56 = pp.create_line(net, bus5, bus6, length_km = line_length, std_type= line_type, name = net.bus.at[bus5,'name']+'-'+net.bus.at[bus6,'name'])
    line67 = pp.create_line(net, bus6, bus7, length_km = line_length, std_type= line_type, name = net.bus.at[bus6,'name']+'-'+net.bus.at[bus7,'name'])
    line78 = pp.create_line(net, bus7, bus8, length_km = line_length, std_type= line_type, name = net.bus.at[bus7,'name']+'-'+net.bus.at[bus8,'name'])
    line89 = pp.create_line(net, bus8, bus9, length_km = line_length, std_type= line_type, name = net.bus.at[bus8,'name']+'-'+net.bus.at[bus9,'name']) 
    
    #optional network plot
    if plot_network == True:
        plot.simple_plot(net, plot_loads = True, plot_gens=True)
    
    return net
                       
net = create_network()