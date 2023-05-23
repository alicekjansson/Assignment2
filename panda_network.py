# -*- coding: utf-8 -*-
"""
Created on Tue May 23 08:39:02 2023

@author: ielmartin
"""

import pandas as pd
import pandapower as pp
import pandapower.plotting as plot

def create_network():
    
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
    load5 = pp.create_load(net, bus, active_power, name =load_name)
                       