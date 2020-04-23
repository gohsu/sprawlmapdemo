#!/usr/local/bin/python3
""" Input a location name to create a html file with comparison plots.

Usage:
    plots.py <location>
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import mpld3
from docopt import docopt

fua_df = pd.read_csv("data/FUA_master_pca.csv", encoding='utf-8')

def missing_values(data,clr):
    if 1 <= len(data) <= 4:
        data_copy = np.copy(data)
        if ~np.isfinite(data[2]):
            data_copy[2] = data_copy[3]
        if ~np.isfinite(data[1]):
            data_copy[1] = data_copy[2]
        if ~np.isfinite(data[0]):
            data_copy[0] = data_copy[1]
        mask = np.isfinite(data_copy)
        line, = plt.plot(years, data_copy[mask], lw=1, ls="--", color=clr)

# column names:
loc_pca_cols = ["pca1_cum_1975","pca1_cum_1990", "pca1_cum_2000", "pca1_cum_2014"]
id1_pca_cols = ["id1_pca1_cum_1975","id1_pca1_cum_1990", "id1_pca1_cum_2000", "id1_pca1_cum_2014"]
iso_pca_cols = ["iso_pca1_cum_1975","iso_pca1_cum_1990", "iso_pca1_cum_2000", "iso_pca1_cum_2014"]

# find particular row
args = docopt(__doc__)
input = args['<location>']
city = fua_df.query('efua_name == @input').head(1)
if city.empty:
    exit("Location not found.")

# fill data
loc_pca = np.array(city[loc_pca_cols].values.reshape(-1))
id1_pca = np.array(city[id1_pca_cols].values.reshape(-1))
iso_pca = np.array(city[iso_pca_cols].values.reshape(-1))
years = ["<1975", "1976-1990","1991-2000", "2001-2014"]

# make the plot
fig, ax = plt.subplots()
plt.xticks(ticks=range(0,len(years)), labels=years)
if ~np.all(np.isnan(loc_pca)):  # if we have data for the local sndi, plot
    missing_values(loc_pca, "red")
    plt.plot(years, loc_pca, color='red', marker='o', label=input)
missing_values(id1_pca, "navy")
plt.plot(years, id1_pca, color='navy', marker='o', lw=1.5, label="Regional ({})".format(city['name_1'].values[0]))
missing_values(iso_pca, "blue")
plt.plot(years, iso_pca, color='blue', marker='o', lw=1.5, label="National ({})".format(city['name_0'].values[0]))
ax.set_title('Cumulative SNDi over time')
ax.set_ylabel('SNDi')
ax.set_xlabel('Years')
plt.legend()
fig.tight_layout()

# write image as html
html = open("{}.html".format(input.replace(" ","")), 'a+')
html.write((mpld3.fig_to_html(fig)))
