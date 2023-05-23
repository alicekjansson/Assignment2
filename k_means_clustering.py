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


# Initialize centroids by drawing a random value in each column as initial guess
# Input parameters df (dataframe containing data points) and nbr (number of centroids to be calculated)
# Returns list of calculated centroids
def initialize(df,k):
    centroids=[]
    #For 
    for n in k:
        cent=[]
        for i,col in df.items():
            cent.append(col.sample(1))
        centroids.append(cent)
    return centroids

# Divide data points into clusters based on nearest centroid
# Input parameters df (dataframe containing data points), clusters (defined clusters to divide data into) and centroids (centroids of clusters)
# Returns list of clusters containing their data points
def get_clusters(df,clusters,centroids):
    for i,row in df.transpose().items():
        coord=np.array(row)
        min_dist=(None,100)
        n=0
        #Find closest centroid
        for c in centroids:
            dist=np.linalg.norm(c - coord)
            if dist<min_dist[1]:
                min_dist=(n,dist)
            n=n+1
        clusters[min_dist[0]].append(row)
    #Convert clusters to dataframe format then add back to clusters list
    for i,cluster in enumerate(clusters):
        cluster=pd.DataFrame(cluster)
        clusters[i]=cluster
    return clusters

# Calculate new centroids based on the average parameters of each cluster
# Input parameters clusters (defined clusters to divide data into) and centroids (centroids of clusters)
# Returns list of new centroids
def calc_centroids(clusters,centroids):
    for n,cluster in enumerate(clusters):
        cs=[]
        for i,row in cluster.items():
            cs.append(row.mean())
        centroids[n]=np.array(cs)
    return centroids

#Check the frequency of different values in each 
# Input parameters df (dataframe containing data points), col (column defining the type of each data point) 
#                  and clusters (clusters containing given data points)
# Returns list of probabilities of the data points in a cluster being of the same type as the most commonly occuring data type in this cluster
def check_accuracy(df,col,clusters):
    probabilities=[]
    for cluster in clusters:
        types = []
        #First check which types are present at all in cluster
        for i,row in cluster.items():
            if row[col] not in types:
                types.append(row[col])
        #Then calculate how many times each type occurs
        occ=[0 for el in range(len(types))]
        for i,typ in enumerate(types):
            for el in cluster:
                kind=cluster[col]
                if typ == kind:
                    occ[i]+=1
        
        #Then calculate the probability of each data point being of the most common type
        freq=[occurence/len(cluster) for occurence in occ]
        probabilities.append(freq.max())
    return probabilities


#Decide number of clusters to be used and randomly generate first centroids
k=3        
centroids=initialize(df,k)
#Run algorithm
dist=1
while dist > 0.01:   
    clusters=[ [] for el in range(18)] 
    #Divide data points into clusters       
    clusters=get_clusters(df,clusters,centroids)
    cent_old=centroids
    #Calculate new centroids
    centroids=calc_centroids(clusters,centroids)
    #Calculate distance of new centroids to old
    dist=np.linalg.norm(cent_old-centroids)
    
#Check accuracy
probabilities=check_accuracy(clusters)


    
    