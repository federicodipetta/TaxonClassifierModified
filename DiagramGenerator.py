"""
this class is used to generate the diagram for comparing algorithm
please insert the json files in the jsonResults folder
"""
import plotly.graph_objects as go
import json as json
import matplotlib.pyplot as plt
import numpy as np
import AutomaticClasterMatrix as acm
dir = 'JsonResults'
patterns = ['*.json']
files = []

for pattern in patterns:
    files.append(acm.find_files(pattern, dir))
files = np.array(files).flatten()
# data to plot


groups1 = [
        'Single-Rand', 'Single-Homogeneity', 'Single-Completeness',
        'Average-Rand', 'Average-Homogeneity', 'Average-Completeness',
        'Complete-Rand', 'Complete-Homogeneity', 'Complete-Completeness'
        ]
tmp = files[0]
files[0] = files[1]
files[1] = tmp
data = []
for file in files:
    with open(file) as f:
        data.append(json.load(f))
groups = []
if (data != []) : 
    for tmp in data[0]['data']:
        for group in groups1:
            groups.append(tmp['key'].replace('-Phylum', '')+ ' ' + group)
print("grups",len(groups))
sources = []
for x in data:
    x = x['data']
    tmp = []
    for bench in x : 
        tmp.append(bench['single']['rand_score'])
        tmp.append(bench['single']['homogeneity_score'])
        tmp.append(bench['single']['completeness_score'])
        tmp.append(bench['average']['rand_score'])
        tmp.append(bench['average']['homogeneity_score'])
        tmp.append(bench['average']['completeness_score'])
        tmp.append(bench['complete']['rand_score'])
        tmp.append(bench['complete']['homogeneity_score'])
        tmp.append(bench['complete']['completeness_score'])
    sources.append(tmp)
    
fig = go.Figure()

for i in range(len(sources)):
    fig.add_trace(go.Bar(name=files[i].replace("JsonResults\\",""), x=groups, y=sources[i]))

fig.update_layout(barmode='group')

fig.show()