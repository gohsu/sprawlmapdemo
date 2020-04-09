#!/usr/local/bin/python3

""" Input a location name to create a html file with plotly graphs.

Usage:
    time_graphs.py [options] <name>

Options:
    -c    If country. By default, city.
"""

from docopt import docopt
import plotly.graph_objects as go
import pandas as pd
import plotly.offline 
import sys

args = docopt(__doc__)
is_country = args['-c']
sprawl = pd.read_csv('cities-sndi.csv')
if is_country:
    sprawl = pd.read_csv('countries-sndi.csv')

input = args['<name>']
try:
    ind, = sprawl.query('city == @input').index
except pd.core.computation.ops.UndefinedVariableError:
    pass
if is_country:
    ind, = sprawl.query('country == @input').index

location = pd.DataFrame()
location["year"] = ["<1990", "1990-1999", "2000-2013"]
location["sndi"] = [sprawl.iloc[ind,2], sprawl.iloc[ind,3],sprawl.iloc[ind,4]]
location["nodal-deg"] = [sprawl.iloc[ind,6], sprawl.iloc[ind,7],sprawl.iloc[ind,8]]
location["nodes"] = [sprawl.iloc[ind,10], sprawl.iloc[ind,11],sprawl.iloc[ind,12]]
if is_country:
    location["sndi"] = [sprawl.iloc[ind,1], sprawl.iloc[ind,2],sprawl.iloc[ind,3]]
    location["nodal-deg"] = [sprawl.iloc[ind,5], sprawl.iloc[ind,6],sprawl.iloc[ind,7]]
    location["nodes"] = [sprawl.iloc[ind,9], sprawl.iloc[ind,10],sprawl.iloc[ind,11]]
name = sprawl.iloc[ind,0]

fig = go.Figure()
fig1 = go.Figure()
fig2 = go.Figure()

fig.add_trace(go.Scatter(
    x=location['year'], 
    y=location['sndi'],
    mode='lines+markers',
    name="SNDI",
    hoverinfo="y"
))

if is_country:
    fig.add_trace(go.Scatter(
        x=location['year'],
        y = [sprawl.iloc[ind,4]] * len(location['year']),
        name="stock",
        hoverinfo="y",
        line=dict(
            color='grey',
            dash='dashdot'
        )
    ))
else:
    fig.add_trace(go.Scatter(
        x=location['year'],
        y=[sprawl.iloc[ind,5]] * len(location['year']),
        name="stock",
        hoverinfo="y",
        line=dict(
            color='grey',
            dash='dashdot'
        )
    ))


fig1.add_trace(go.Scatter(
    x=location['year'], 
    y=location['nodal-deg'],
    name="Nodal Degree",
    hoverinfo="y",
))

if is_country:
    fig1.add_trace(go.Scatter(
        x=location['year'],
        y=[sprawl.iloc[ind,8]] * len(location['year']),
        name="stock",
        hoverinfo="y",
        line=dict(
            color='grey',
            dash='dashdot'
        )
    ))
else:
    fig1.add_trace(go.Scatter(
        x=location['year'],
        y=[sprawl.iloc[ind,9]] * len(location['year']),
        name="stock",
        hoverinfo="y",
        line=dict(
            color='grey',
            dash='dashdot'
        )
    ))


fig2.add_trace(go.Scatter(
    x=location['year'], 
    y=location['nodes'],
    name="Nodes",
    hoverinfo="y",
))

if is_country:
    fig2.add_trace(go.Scatter(
        x=location['year'],
        y=[sprawl.iloc[ind,12]] * len(location['year']),
        name="stock",
        hoverinfo="y",
        line=dict(
            color='grey',
            dash='dashdot'
        )
    ))
else:
    fig2.add_trace(go.Scatter(
        x=location['year'],
        y=[sprawl.iloc[ind,13]] * len(location['year']),
        name="stock",
        hoverinfo="y",
        line=dict(
            color='grey',
            dash='dashdot'
        )
    ))


fig.update_layout(
    height = 600,
    width = 800,
    title_text='Sprawl index in {}'.format(name),
    yaxis_title='Sprawl (SNDi)',
    xaxis_title='Year'
)

fig1.update_layout(
    height = 600,
    width = 800,
    title_text='Nodal degree in {}'.format(name),
    yaxis_title='Nodal degree',
    xaxis_title='Year'
)

fig2.update_layout(
    height = 600,
    width = 800,
    title_text='Nodes in {}'.format(name),
    yaxis_title='Nodes',
    xaxis_title='Year'
)

# fig.write_html("plotly/{}-sndi.html".format(cityname))
fig_div = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')
fig1_div = plotly.offline.plot(fig1, include_plotlyjs=False, output_type='div')
fig2_div = plotly.offline.plot(fig2, include_plotlyjs=False, output_type='div')

html_divs = open("{}-plotly.html".format(name.replace(" ",'')), 'a+')
html_divs.write('<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>')
html_divs.write(fig_div)
html_divs.write(fig1_div)
html_divs.write(fig2_div)
html_divs.close()

#TODO regional (country) comparison 