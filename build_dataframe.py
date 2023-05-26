# -*- coding: utf-8 -*-
"""
Created on Thu May 25 13:50:11 2023

@author: Alice
"""

#This script imports created csv files, marks the scenario they belong to and add dataframes together to common data set
import pandas as pd


#Import csv file and convert to dataframe, add info on scenario
def import_df(el,typ):
    df=pd.read_csv(r'C:/Users/Alice/OneDrive - Lund University/Dokument/GitHub/Assignment2/res_bus\test_%s_%s.csv' %(el,typ) ,';'  ) 
    df=df.iloc[:,1:]
    df['Scenario1']=[typ for _ in range(len(df))]
    return df

scens=['high','low','gendisc','linedisc']
vm=[]
va=[]
for scen in scens:
    vm.append(import_df('vm_pu',scen))
    va.append(import_df('va_degree',scen))
#Create dataframes for voltage magnitude resp. voltage angle
df_vm=vm[0].append(vm[1]).append(vm[2]).append(vm[3])
df_va=va[0].append(va[1]).append(va[2]).append(va[3])
#Merge dataframes
df_vm.index=[i for i in range(len(df_vm))]
df_va.index=[i for i in range(len(df_va))]
df_va.columns=[9,10,11,12,13,14,15,16,17,'Scenario']
df_all=pd.merge(df_vm,df_va,left_on=df_vm.index,right_on=df_va.index)
df_all=df_all.drop(['key_0','Scenario1'],axis=1)

#Save to csv
# df_all.to_csv(r'C:/Users/Alice/OneDrive - Lund University/Dokument/GitHub/Assignment2/testing_set.csv')