#!/usr/local/bin/python3

""" Input a city name to create a html file with plotly graphs.

Usage:
    time_graphs.py <city>

"""

from docopt import docopt
import plotly.graph_objects as go
import pandas as pd
import plotly.offline 
import sys

args = docopt(__doc__)
sprawl = pd.read_csv('cities-sndi.csv')
input = args['<city>']
ind, = sprawl.query('city == @input').index

city = pd.DataFrame()
city["year"] = ["<1990", "1990-1999", "2000-2013"]
city["sndi"] = [sprawl.iloc[ind,2], sprawl.iloc[ind,3],sprawl.iloc[ind,4]]
city["nodal-deg"] = [sprawl.iloc[ind,6], sprawl.iloc[ind,7],sprawl.iloc[ind,8]]
city["nodes"] = [sprawl.iloc[ind,10], sprawl.iloc[ind,11],sprawl.iloc[ind,12]]

cityname = sprawl.iloc[ind,0]

fig = go.Figure()
fig1 = go.Figure()
fig2 = go.Figure()

fig.add_trace(go.Scatter(
    x=city['year'], 
    y=city['sndi'],
    mode='lines+markers',
    name="SNDI",
    hoverinfo="y"
))

fig.add_trace(go.Scatter(
    x=city['year'],
    y=[sprawl.iloc[ind,5]] * len(city['year']),
    name="stock",
    hoverinfo="y",
    line=dict(
        color='grey',
        dash='dashdot'
    )
))

fig1.add_trace(go.Scatter(
    x=city['year'], 
    y=city['nodal-deg'],
    name="Nodal Degree",
    hoverinfo="y",
))

fig1.add_trace(go.Scatter(
    x=city['year'],
    y=[sprawl.iloc[ind,9]] * len(city['year']),
    name="stock",
    hoverinfo="y",
    line=dict(
        color='grey',
        dash='dashdot'
    )
))


fig2.add_trace(go.Scatter(
    x=city['year'], 
    y=city['nodes'],
    name="Nodes",
    hoverinfo="y",
))

fig2.add_trace(go.Scatter(
    x=city['year'],
    y=[sprawl.iloc[ind,13]] * len(city['year']),
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
    title_text='Sprawl index in {}, {}'.format(cityname,sprawl.iloc[ind,1]),
    yaxis_title='Sprawl (SNDi)',
    xaxis_title='Year'
)

fig1.update_layout(
    height = 600,
    width = 800,
    title_text='Nodal degree in {}, {}'.format(cityname,sprawl.iloc[ind,1]),
    yaxis_title='Nodal degree',
    xaxis_title='Year'
)

fig2.update_layout(
    height = 600,
    width = 800,
    title_text='Nodes in {}, {}'.format(cityname,sprawl.iloc[ind,1]),
    yaxis_title='Nodes',
    xaxis_title='Year'
)

# fig.write_html("plotly/{}-sndi.html".format(cityname))
fig_div = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')
fig1_div = plotly.offline.plot(fig1, include_plotlyjs=False, output_type='div')
fig2_div = plotly.offline.plot(fig2, include_plotlyjs=False, output_type='div')

html_divs = open("{}-plotly.html".format(cityname.replace(" ",'')), 'a+')
html_divs.write('<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>')
html_divs.write(fig_div)
html_divs.write(fig1_div)
html_divs.write(fig2_div)
html_divs.close()

#TODO regional (country) comparison 