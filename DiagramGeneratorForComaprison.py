"""
this file is used to generate a diagram from the output of the JsonComparator.py file
"""
import json as json
import plotly.graph_objects as go

def loadJson(file):
    with open(file) as f:
        return json.load(f)


settings = json.load(open('settings.json'))["diagramGeneratoForComparison"]

input = loadJson(settings['input'])
data = input["data"]

groups1 = [
        'Single-Rand', 'Single-Homogeneity', 'Single-Completeness',
        'Average-Rand', 'Average-Homogeneity', 'Average-Completeness',
        'Complete-Rand', 'Complete-Homogeneity', 'Complete-Completeness'
    ]
groups = []
if (data != []) : 
    for sources in data:
        for group in groups1:
            groups.append(sources['key'].replace('-Phylum', '')+ ' ' + group)

sources = []
for result in data : 
    result = result['value']
    sources.append(result['single']['rand_score'])
    sources.append(result['single']['homogeneity_score'])
    sources.append(result['single']['completeness_score'])
    sources.append(result['average']['rand_score'])
    sources.append(result['average']['homogeneity_score'])
    sources.append(result['average']['completeness_score'])
    sources.append(result['complete']['rand_score'])
    sources.append(result['complete']['homogeneity_score'])
    sources.append(result['complete']['completeness_score'])

fig = go.Figure()


fig.add_trace(go.Bar(name="ciao", x=groups, y=sources))

message = "Comparison between file 1 - file 2 "+ input["firsrJson"] + " - " + input ["secondJson"]
              
fig.update_layout(
    title={
        'text': message,
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})

fig.show()


