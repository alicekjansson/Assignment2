# -*- coding: utf-8 -*-
"""
Created on Tue May 23 09:56:26 2023

@author: Alice
"""
#This script holds the algorithm of k-nearest neighbour classification


import pandas as pd
import numpy as np
import time
import random
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#Measure time taken
start=time.time()

#Import testing and learning sets
learning=pd.read_csv()
testing=pd.read_csv()

#START BY NORMALIZING DATA SETS!


# Find k nearest neighbours in learning set for this timestep
# Input parameters timestep (this datapoint), k (nbr of nearest neighbours), col (column defining the type of each data point) 
# Return list of k nearest data points
def find_neighbors(timestep,k,col):
    thiscoord=np.array(timestep.drop(col))
    neighbors=[]
    for i,ref in learning.transpose().items():
        coord=np.array(ref.drop(col))
        dist=np.linalg.norm(coord-thiscoord)
        neighbors.append([ref[col],dist])
    neighbors=pd.DataFrame(neighbors,columns=['Type','Dist']).sort_values(by=['Dist'],axis=0).iloc[:k,:]
    return neighbors

def occurances(timestep,typ,col):
    occ=0
    for el in timestep:
        kind=el[col]
        if typ == kind:
            occ[i]+=1
    return occ

#First find list of types
types = []
for i,row in learning.items():
    if row[col] not in types:
        types.append(row[col])

#Find k nearest neighbors and let that classify data point
k=3
pred=[]
for i,timestep in testing.transpose().items():
    neighbors=find_neighbors(timestep,k)
    # print(neighbors)
    most_likely=(False,0)
    for typ in types:
        occurance=occurances(timestep,typ)
        if occurance>most_likely[1]:
            most_likely=(typ,occurance)
    pred.append(most_likely[0])
#Add predicted values to column in testing data set
testing['Predicted']=pred

#Check accuracy of prediction
correct=testing['Species']==testing['Predicted']
accuracy=len([x for x in correct if x==True])/len(correct)


#Check the time it took for the script to run
end=time.time()
print('Time elapsed: ' + str(round(end-start,2)) + 's')
print('The accuracy of prediction is: ' + str(accuracy*100) + '%')