"""
this class is used to generate the diagram for comparing algorithm
please insert the json files in the jsonResults folder
"""
import plotly.graph_objects as go
import json as json
import matplotlib.pyplot as plt
import numpy as np
import os
import glob

# Get the directory from the input
settings = json.load(open('settings.json'))["diagramGenerator"]
dir = settings["dir"]

# Find JSON files more safely
files = glob.glob(os.path.join(dir, "*.json"))

if len(files) < 2:
    print("Warning: Meno di 2 file JSON trovati")

# Load data
data = []
for file in files:
    print(f"Caricamento file: {file}")
    with open(file) as f:
        data.append(json.load(f))

if not data:
    print("Error: Nessun dato caricato")
    exit(1)

# Trova tutti gli esperimenti unici attraverso tutti i dataset
all_experiments = set()
for dataset in data:
    for experiment in dataset['data']:
        all_experiments.add(experiment['key'])

# Ordina gli esperimenti per avere un ordine consistente
all_experiments = sorted(list(all_experiments))

print(f"Esperimenti trovati: {all_experiments}")

# Create groups
groups = []
groups1 = [
    #'Single-Rand', 'Single-Homogeneity', 'Single-Completeness',
    #'Average-Rand', 'Average-Homogeneity', 'Average-Completeness',
    'Complete-Rand', 'Complete-Homogeneity', 'Complete-Completeness'
]

# Create group names based on ALL experiments found
for experiment_key in all_experiments:
    experiment_name = experiment_key.replace('-Phylum', '')
    for group in groups1:
        groups.append(f"{experiment_name} {group}")

print("Groups:", len(groups))

# Extract sources data
sources = []
for i, dataset in enumerate(data):
    print(f"\nProcessing dataset {i+1}: {os.path.basename(files[i])}")
    dataset_values = []
    
    # Crea un dizionario per accesso rapido agli esperimenti
    exp_dict = {exp['key']: exp for exp in dataset['data']}
    
    for experiment_key in all_experiments:
        if experiment_key in exp_dict:
            bench = exp_dict[experiment_key]
            print(f"  title: {bench['title']}")
            values = [
                # bench['single']['rand_score'],
                # bench['single']['homogeneity_score'],
                # bench['single']['completeness_score'],
                # bench['average']['rand_score'],
                # bench['average']['homogeneity_score'],
                # bench['average']['completeness_score'],
                bench['complete']['rand_score'],
                bench['complete']['homogeneity_score'],
                bench['complete']['completeness_score']
            ]
            #print(f"  {experiment_key}: Single rand = {bench['single']['rand_score']}")
        else:
            # Se l'esperimento non esiste in questo dataset, usa valori zero
            values = [0] * 9
            print(f"  {experiment_key}: MANCANTE (usando zeri)")
        
        dataset_values.extend(values)
    
    sources.append(dataset_values)

# Debug: mostra i primi valori di ogni source
print("\n=== PRIMI VALORI DI OGNI SOURCE ===")
for i, source in enumerate(sources):
    print(f"Source {i+1} (primi 9 valori): {source[:9]}")

# Create the plot
fig = go.Figure()

for i, source in enumerate(sources):
    file_name = os.path.basename(files[i]).replace('.json', '')
    fig.add_trace(go.Bar(name=file_name, x=groups, y=source))

fig.update_layout(
    barmode='group',
    title='Comparison of Clustering Algorithms',
    xaxis_title='Experiments and Metrics',
    yaxis_title='Score',
    xaxis={'tickangle': 45}
)

fig.show()