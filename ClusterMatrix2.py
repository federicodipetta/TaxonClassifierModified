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
    np.random.seed(42)
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
        if distances.loc[k].loc['FileName1'].replace("_16S", "").replace("_18S", "").replace(".ct","").replace(".bpseq.txt", "") not in index_of:
            continue
        if distances.loc[k].loc['FileName2'].replace("_16S", "").replace("_18S", "").replace(".ct","").replace(".bpseq.txt", "") not in index_of:
            continue
        i = index_of[distances.loc[k].loc['FileName1'].replace("_16S", "").replace("_18S", "").replace(".ct","").replace(".bpseq.txt", "")]
        j = index_of[distances.loc[k].loc['FileName2'].replace("_16S", "").replace("_18S", "").replace(".ct","").replace(".bpseq.txt", "")]
        value = distances.loc[k].loc['SERNADistance']
        distance_matrix[i][j] = value
        distance_matrix[j][i] = value
        
    # Determine the number of clusters as distinct labels in molecules
    n_clusters = len(set(label_of.values()))

    # Read the true lables assigned to every Id 
    labels_true = list(label_of.values())

    # Execute clustering with single linkage and determines the predicted labels for each molecule
    model = KMeans(n_clusters=n_clusters, init='k-means++', algorithm='elkan')
    model.fit(distance_matrix)
    #model = AgglomerativeClustering(n_clusters=n_clusters, metric='precomputed', linkage ='single').fit(distance_matrix)
    labels_pred = model.fit_predict(distance_matrix)
    json["auto"] = {
        "rand_score": metrics.rand_score(labels_true, labels_pred),
        "homogeneity_score": metrics.homogeneity_score(labels_true, labels_pred),
        "completeness_score": metrics.completeness_score(labels_true, labels_pred),
        "completeness_score": metrics.completeness_score(labels_true, labels_pred),
        "predicted": [
            {
                "Id": molecules.loc[i].loc['Id'],
                "Organism": molecules.loc[i].loc['Organism'],
                "Taxon": molecules.loc[i].loc['Taxon'],
                "Predicted": str(labels_pred[i]),
                "True": str(labels_true[i])
            } for i in range(len(molecules))
        ]
    }
    # Execute clustering with complete linkage and determines the predicted labels for each molecule
    # model = AgglomerativeClustering(n_clusters=n_clusters, metric='precomputed', linkage ='average').fit(distance_matrix)
    # labels_pred = model.fit_predict(distance_matrix)
    # json["average"] = {
    #     "rand_score": metrics.rand_score(labels_true, labels_pred),
    #     "homogeneity_score": metrics.homogeneity_score(labels_true, labels_pred),
    #     "completeness_score": metrics.completeness_score(labels_true, labels_pred),
    #     "completeness_score": metrics.completeness_score(labels_true, labels_pred),
    #     "predicted": [
    #         {
    #             "Id": molecules.loc[i].loc['Id'],
    #             "Organism": molecules.loc[i].loc['Organism'],
    #             "Taxon": molecules.loc[i].loc['Taxon'],
    #             "Predicted": str(labels_pred[i]),
    #             "True": str(labels_true[i])
    #         } for i in range(len(molecules))
    #     ]
    # }
    # # Execute clustering with average linkage and determines the predicted labels for each molecule
    # model = AgglomerativeClustering(n_clusters=n_clusters, metric='precomputed', linkage ='complete').fit(distance_matrix)
    # labels_pred = model.fit_predict(distance_matrix)
    # json["complete"] = {
    #     "rand_score": metrics.rand_score(labels_true, labels_pred),
    #     "homogeneity_score": metrics.homogeneity_score(labels_true, labels_pred),
    #     "completeness_score": metrics.completeness_score(labels_true, labels_pred),
    #             "predicted": [
    #         {
    #             "Id": molecules.loc[i].loc['Id'],
    #             "Organism": molecules.loc[i].loc['Organism'],
    #             "Taxon": molecules.loc[i].loc['Taxon'],
    #             "Predicted": str(labels_pred[i]),
    #             "True": str(labels_true[i])
    #         } for i in range(len(molecules))
    #     ]
    # }
    return json
    #return generate_clustering_results(labels_true, n_clusters, "DATI PER "+ file_moleculus + " E " + file_benchMarck)



#this part is for testing what happen with a random matrix
def generate_random_clusters(n_elements, n_clusters):
    # Genera assegnazioni casuali di cluster per ciascun elemento
    return np.random.randint(0, n_clusters, size=(n_elements, n_elements))

def perturb_distance_matrix(distance_matrix, noise_level=0.01):
    noise = np.random.normal(0, noise_level, distance_matrix.shape)
    perturbed_matrix = distance_matrix + noise
    np.fill_diagonal(perturbed_matrix, 0)  # Mantieni le diagonali a zero
    return np.abs(perturbed_matrix)  # Evita distanze negative

def clustering_with_linkage(distance_matrix, n_clusters, linkage):
    """Esegue il clustering gerarchico con un determinato tipo di linkage."""
    model = AgglomerativeClustering(n_clusters=n_clusters, metric='precomputed', linkage=linkage)
    labels_pred = model.fit_predict(distance_matrix)
    return labels_pred

def optimize_clustering(labels_true, n_clusters, n_iterations=100000000, noise_level=0.3):
    distance_matrix = generate_random_clusters(len(labels_true), n_clusters)
    
    """Esegue clustering con perturbazioni casuali e seleziona il miglior risultato."""
    best_results = {
        "single": {"rand_score": 0},
        "average": {"rand_score": 0},
        "complete": {"rand_score": 0}
    }

    for i in range(n_iterations):
        perturbed_matrix = perturb_distance_matrix(distance_matrix, noise_level)
        for linkage in ['single', 'average', 'complete']:
            labels_pred = clustering_with_linkage(perturbed_matrix, n_clusters, linkage)

            rand = metrics.rand_score(labels_true, labels_pred)
            homogeneity = metrics.homogeneity_score(labels_true, labels_pred)
            completeness = metrics.completeness_score(labels_true, labels_pred)

            result = {
                "rand_score": rand,
                "homogeneity_score": homogeneity,
                "completeness_score": completeness
            }

            # Aggiorna il miglior risultato se il rand_score è migliore
            if rand > best_results[linkage]["rand_score"]:
                best_results[linkage] = result

    return best_results

def generate_clustering_results(labels_true, n_clusters, title, n_iterations=10000, noise_level=0.1):
    """Genera i risultati del clustering con ottimizzazione casuale."""
    results = optimize_clustering(labels_true, n_clusters, n_iterations, noise_level)
    result_json = {
        "title": title,
        "single": results["single"],
        "average": results["average"],
        "complete": results["complete"]
    }
    return result_json
