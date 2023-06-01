# -*- coding: utf-8 -*-
"""
Created on Tue May 23 09:29:31 2023

@author: Alice
"""

#This script holds the algorithm for k-means clustering

import pandas as pd
import numpy as np
import time
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Measure time taken
start=time.time()

# Import data
# 0-8 are voltage magnitudes, 9-17 are voltage angles
df=pd.read_csv(r'C:/Users/Alice/OneDrive - Lund University/Dokument/GitHub/Assignment2/learning_set.csv').iloc[:,1:]

# Initialize centroids by drawing a random timestep as initial guess
# Input parameters df (dataframe containing data points) and nbr (number of centroids to be calculated)
# Returns list of calculated centroids
def initialize(df,k):
    centroids=[]
    df=df.drop('Scenario',axis=1)
    dfcentroids=df.sample(k)        #Sample k initial data points
    #Rewrite dataframe as list of arrays
    for n,row in dfcentroids.transpose().items():
        centroids.append(np.array(row))
    return centroids

# Divide data points into clusters based on nearest centroid
# Input parameters df (dataframe containing data points), clusters (defined clusters to divide data into) and centroids (centroids of clusters)
# Returns list of clusters containing their data points
def get_clusters(df,clusters,centroids):
    df1=df.drop('Scenario',axis=1)
    for i,row in df1.transpose().items():
        coord=np.array(row)
        min_dist=(None,100)
        n=0
        #Find closest centroid
        for c in centroids:
            dist=np.linalg.norm(c - coord)
            if dist<min_dist[1]:
                min_dist=(n,dist)
            n=n+1
        clusters[min_dist[0]].append(df.loc[i])
    #Convert clusters to dataframe format then add back to clusters list
    for i,cluster in enumerate(clusters):
        cluster=pd.DataFrame(cluster)
        clusters[i]=cluster
    return clusters

# Calculate new centroids based on the average parameters of each cluster
# Input parameters clusters (defined clusters to divide data into) and centroids (centroids of clusters)
# Returns list of new centroids
def calc_centroids(clusters,centroids):
    new_centroids=list(np.zeros(len(centroids)))
    for n,cluster in enumerate(clusters):
        cluster=cluster.drop('Scenario',axis=1)
        cs=[]
        for i,col in cluster.items():
            cs.append(col.mean())
        new_centroids[n]=np.array(cs)
    return new_centroids

# Check the frequency of different values in each cluster
# Input parameters df (dataframe containing data points), col (column defining the type of each data point) 
#                  and clusters (clusters containing given data points)
# Returns list of probabilities of the data points in a cluster being of the same type as the most commonly occuring data type in this cluster
def check_accuracy(df,col,clusters):
    probabilities=[]
    for cluster in clusters:
        types = []
        #First check which types are present at all in cluster
        for i,row in cluster.transpose().items():
            if row[col] not in types:
                types.append(row[col])
        #Then calculate how many times each type occurs
        occ=[0 for el in range(len(types))]
        for i,typ in enumerate(types):
            for j,el in cluster.transpose().items():
                kind=el[col]
                if typ == kind:
                    occ[i]+=1
        
        #Then calculate the probability of each data point being of the most common type
        freq=[occurence/len(cluster) for occurence in occ]
        probabilities.append(np.max(freq).round(2))
    return probabilities

#Normalize dataframe by subtracting column mean value in each column
def normalize(df):
    for i,col in df.items():
        if i!= 'Scenario':
            df[i] = col-col.mean()
    return df

#Start by normalizing the dataframe
df=normalize(df)

#Decide number of clusters to be used and randomly generate first centroids
k=4 
centroids=initialize(df,k)
#Run algorithm
dist=1000
clusters=[ [] for el in range(k)] 
count=0
while abs(dist) > 0.1:    
    #Divide data points into clusters       
    clusters=get_clusters(df,clusters,centroids)
    #Calculate new centroids
    new_centroids=calc_centroids(clusters,centroids)
    #Calculate distance of new centroids to old
    tot_dist=0
    for i,cent in enumerate(new_centroids):
        tot_dist=tot_dist+np.linalg.norm(cent-centroids[i])
    dist=tot_dist/4
    print(dist)
    centroids=new_centroids.copy()
    count+=1
    
#Check accuracy
probabilities=check_accuracy(df,'Scenario',clusters)

#Check the time it took for the script to run
end=time.time()
print('Time elapsed: ' + str(round(end-start,2)) + 's')
print('The probabilities are: ' + str(probabilities) )
