#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TaxonClassifier: execute agglomerative clustering on a set of molecules based on
a distance matrix and evaluate the quality of the clustering w.r.t. a known 
clusterization.

Usage: python3 ClusterMatrix.py <molecule-list-csv-file> <distances-csv-file>

The format of <molecule-list-csv-file> must be <"Id", "Organism", "Taxon"> where
Id is a unique identifier in the file, Organism is a textual description of the 
Id and Taxon is the label associated to Id by a known classification

The format of <distances-csv-file> must be <"Id1", "Id2", "Distance"> where Id1 
and Id2 are two different Ids of the first file and Distance is a floating point
value corresponding to the distance from Id1 and Id2 computed by a chosen 
comparison method. 

The output is given textually as the values of "Rand_score", "Homogeneity_score" 
and "Completeness_score" metrics computed for each executed clustering and for 
each linkage parameter of the clustering algorithm: single, complete and 
average.

@author: Michela Quadrini and Luca Tesei
"""
import math
import sys
import pandas as pd
import numpy as np
from sklearn.metrics import *
from sklearn.cluster import *
from sklearn import metrics
import argparse


# Read the list of molecules
def calculate_ClusterMatrix(file_moleculus, file_benchMarck):
    result = "DATI PER "+ file_moleculus + " E " + file_benchMarck + "\n"
    molecules = pd.read_csv(file_moleculus, sep=";", encoding='latin-1')

    # Create dictionary Id -> Index
    index_of = dict() 
    for i in range(len(molecules)) :
        index_of[molecules.loc[i].loc['Id']] = i

    # Create dictionary Id -> Organism 
    organism_of = dict()
    for i in range(len(molecules)) :
        organism_of[molecules.loc[i].loc['Id']] = molecules.loc[i].loc['Organism'].strip()

    # Create dictionary Id -> Label 
    label_of = dict()
    for i in range(len(molecules)) :
        label_of[molecules.loc[i].loc['Id']] = molecules.loc[i].loc['Taxon'].strip()

    # Read the list of distances
    
    distances = pd.read_csv(file_benchMarck, sep=",")

    # Create Distance Matrix
    s= (len(molecules),len(molecules))
    distance_matrix= np.zeros(s)
    # Populate Distance Matrix
    for k in range(len(distances)) :
        i = index_of[distances.loc[k].loc['FileName1'].replace(".ct","")]
        j = index_of[distances.loc[k].loc['FileName2'].replace(".ct","")]
        value = distances.loc[k].loc['SERNADistance']
        distance_matrix[i][j] = value
        distance_matrix[j][i] = value

    # Determine the number of clusters as distinct labels in molecules
    n_clusters = len(set(label_of.values()))

    # Read the true lables assigned to every Id 
    labels_true = list(label_of.values())

    # Execute clustering with single linkage and determines the predicted labels for each molecule

    model = AgglomerativeClustering(n_clusters=n_clusters, metric='precomputed', linkage ='single').fit(distance_matrix)
    labels_pred = model.fit_predict(distance_matrix)

    # Compute the metrics and print the evaluations

    result += "Method: single\n"
    #print("Labels Pred", list(labels_pred))
    #print("Labels True", list(labels_true))
    result += "Rand_score: " + str(metrics.rand_score(labels_true, labels_pred)) + "\n"
  
    result += "Homogeneity_score: " + str(metrics.homogeneity_score(labels_true, labels_pred)) + "\n"

    result += "Completeness_score: " + str(metrics.completeness_score(labels_true, labels_pred)) + "\n"
        
    # Execute clustering with complete linkage and determines the predicted labels for each molecule

    model = AgglomerativeClustering(n_clusters=n_clusters, metric='precomputed', linkage ='complete').fit(distance_matrix)
    labels_pred = model.fit_predict(distance_matrix)

    # Compute the metrics and print the evaluations
 
    result += "Method: complete\n"
    #print("Labels Pred", list(labels_pred))
    #print("Labels True", list(labels_true))
 
    result += "Rand_score: " + str(metrics.rand_score(labels_true, labels_pred)) + "\n"

    result += "Homogeneity_score: " + str(metrics.homogeneity_score(labels_true, labels_pred)) + "\n"

    result += "Completeness_score: " + str(metrics.completeness_score(labels_true, labels_pred)) + "\n"


    # Execute clustering with average linkage and determines the predicted labels for each molecule

    model = AgglomerativeClustering(n_clusters=n_clusters, metric='precomputed', linkage ='average').fit(distance_matrix)
    labels_pred = model.fit_predict(distance_matrix)

    # Compute the metrics and print the evaluations

    result += "Method: average\n"
    #print("Labels Pred", list(labels_pred))
    #print("Labels True", list(labels_true))

    result += "Rand_score: " + str(metrics.rand_score(labels_true, labels_pred)) + "\n"
   
    result += "Homogeneity_score: " + str(metrics.homogeneity_score(labels_true, labels_pred)) + "\n"

    result += "Completeness_score: " + str(metrics.completeness_score(labels_true, labels_pred)) + "\n"
    return result
# End caluclate_ClusterMatrix

def calculate_ClusterMatrix_json(file_moleculus, file_benchMarck):
    json = { 
        "title" : "DATI PER "+ file_moleculus + " E " + file_benchMarck,
    }
    molecules = pd.read_csv(file_moleculus, sep=";", encoding='latin-1')

    # Create dictionary Id -> Index
    index_of = dict() 
    for i in range(len(molecules)) :
        index_of[molecules.loc[i].loc['Id']] = i

    # Create dictionary Id -> Organism 
    organism_of = dict()
    for i in range(len(molecules)) :
        organism_of[molecules.loc[i].loc['Id']] = molecules.loc[i].loc['Organism'].strip()

    # Create dictionary Id -> Label 
    label_of = dict()
    for i in range(len(molecules)) :
        label_of[molecules.loc[i].loc['Id']] = molecules.loc[i].loc['Taxon'].strip()

    # Read the list of distances
    
    distances = pd.read_csv(file_benchMarck, sep=",")

    # Create Distance Matrix
    s= (len(molecules),len(molecules))
    distance_matrix= np.zeros(s)
    # Populate Distance Matrix
    for k in range(len(distances)) :
        i = index_of[distances.loc[k].loc['FileName1'].replace(".ct","")]
        j = index_of[distances.loc[k].loc['FileName2'].replace(".ct","")]
        value = distances.loc[k].loc['SERNADistance']
        distance_matrix[i][j] = value
        distance_matrix[j][i] = value

    # Determine the number of clusters as distinct labels in molecules
    n_clusters = len(set(label_of.values()))

    # Read the true lables assigned to every Id 
    labels_true = list(label_of.values())

    # Execute clustering with single linkage and determines the predicted labels for each molecule

    model = AgglomerativeClustering(n_clusters=n_clusters, metric='precomputed', linkage ='single').fit(distance_matrix)
    labels_pred = model.fit_predict(distance_matrix)
    json["single"] = {
        "rand_score": metrics.rand_score(labels_true, labels_pred),
        "homogeneity_score": metrics.homogeneity_score(labels_true, labels_pred),
        "completeness_score": metrics.completeness_score(labels_true, labels_pred)
    }
    # Execute clustering with complete linkage and determines the predicted labels for each molecule
    model = AgglomerativeClustering(n_clusters=n_clusters, metric='precomputed', linkage ='average').fit(distance_matrix)
    labels_pred = model.fit_predict(distance_matrix)
    json["average"] = {
        "rand_score": metrics.rand_score(labels_true, labels_pred),
        "homogeneity_score": metrics.homogeneity_score(labels_true, labels_pred),
        "completeness_score": metrics.completeness_score(labels_true, labels_pred)
    }
    # Execute clustering with average linkage and determines the predicted labels for each molecule
    model = AgglomerativeClustering(n_clusters=n_clusters, metric='precomputed', linkage ='complete').fit(distance_matrix)
    labels_pred = model.fit_predict(distance_matrix)
    json["complete"] = {
        "rand_score": metrics.rand_score(labels_true, labels_pred),
        "homogeneity_score": metrics.homogeneity_score(labels_true, labels_pred),
        "completeness_score": metrics.completeness_score(labels_true, labels_pred)
    }
    return json
    