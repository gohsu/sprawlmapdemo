#!/usr/local/bin/python3
""" Input a city name to create a html file with comparison plots.

Usage:
    plots.py [options] <location> 
    
Options:
    -r      regional
    -n      national
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import mpld3
import os
from docopt import docopt

def missing_values(data):
    if 1 <= len(data) <= 4:
        data_copy = np.copy(data)
        if ~np.isfinite(data[2]):
            data_copy[2] = data_copy[3]
        if ~np.isfinite(data[1]):
            data_copy[1] = data_copy[2]
        if ~np.isfinite(data[0]):
            data_copy[0] = data_copy[1]
        mask = np.isfinite(data_copy)
        line, = plt.plot(years, data_copy[mask], lw=1, ls="--", color="grey")

def to_htmlfile_wlink(arg, arg_lat, arg_lon):
    # write image as html
    htmlfile = open("{}.html".format(arg.replace(" ","")), 'a+')
    htmlfile.write('<p>See {} on the <a target=”_blank” href="https://sprawlmap.org/#5/{}/{}">sprawlmap</a>.</p>'.format(arg, arg_lat, arg_lon))
    htmlfile.write((mpld3.fig_to_html(fig)))

def to_htmlfile(arg):
    # write image as html
    htmlfile = open("{}.html".format(arg.replace(" ","")), 'a+')
    htmlfile.write((mpld3.fig_to_html(fig)))

def plot_city(arg_city):
    city = fua_df.query('efua_name == @arg_city').head(1)
    if city.empty:
        exit("Location not found.")

    # fill data
    loc_pca = np.array(city[loc_pca_cols].values.reshape(-1))
    id1_pca = np.array(city[id1_pca_cols].values.reshape(-1))
    iso_pca = np.array(city[iso_pca_cols].values.reshape(-1))

    # make the plot
    if ~np.all(np.isnan(loc_pca)):  # if we have data for the local sndi, plot
        missing_values(loc_pca)
        plt.plot(years, loc_pca, color='red', marker='o', label=arg_city)
    missing_values(id1_pca)
    plt.plot(years, id1_pca, color='navy', marker='o', lw=1.5, label="Regional ({})".format(city['name_1'].values[0]))
    missing_values(iso_pca)
    plt.plot(years, iso_pca, color='blue', marker='o', lw=1.5, label="National ({})".format(city['name_0'].values[0]))
    ax.set_title('Cumulative SNDi over time')
    ax.set_ylabel('SNDi')
    ax.set_xlabel('Years')
    plt.legend()
    fig.tight_layout()
    to_htmlfile(arg_city)


def plot_regional(arg_region):
    region_df = fua_df[fua_df["name_1"]==arg_region]
    # plot the region's pca
    id1_pca = np.array(region_df[id1_pca_cols].head(1).values.reshape(-1))
    plt.plot(years, id1_pca, color="red", label=arg_region)
    cities_list = region_df["efua_name"].unique()
    # plot cities
    for i in range(0, len(cities_list)):
        this_city = cities_list[i]
        city_query = region_df.query('efua_name == @this_city').head(1)
        city_pca = np.array(city_query[loc_pca_cols].values.reshape(-1))
        plt.plot(years, city_pca, label=this_city)
    ax.set_title('Cumulative SNDi over time')
    ax.set_ylabel('SNDi')
    ax.set_xlabel('Years')
    plt.legend(loc='lower center', ncol=4)
    fig.tight_layout()
    to_htmlfile_wlink(arg_region, region_df["id1_geom_centroid_lat"].head(1).values[0], region_df["id1_geom_centroid_lon"].head(1).values[0])
    

def plot_national(arg_country):
    country_df = fua_df[fua_df["name_0"]==arg_country]
    # plot the region's pca
    iso_pca = np.array(country_df[iso_pca_cols].head(1).values.reshape(-1))
    plt.plot(years, iso_pca, color="red", label=arg_country)
    region_list = country_df["name_1"].unique()
    # plot regions
    for i in range(0, len(region_list)):
        this_region = region_list[i]
        region_query = country_df.query('name_1 == @this_region').head(1)
        region_pca = np.array(region_query[id1_pca_cols].values.reshape(-1))
        plt.plot(years, region_pca, label=this_region)
    ax.set_title('Cumulative SNDi over time')
    ax.set_ylabel('SNDi')
    ax.set_xlabel('Years')
    plt.legend(loc='lower center', ncol=4)
    fig.tight_layout()
    to_htmlfile_wlink(arg_country, country_df["iso_geom_centroid_lat"].head(1).values[0], country_df["iso_geom_centroid_lon"].head(1).values[0])
    

fua_df = pd.read_csv("data/FUA_master_pca.csv", encoding='utf-8')

# column names:
loc_pca_cols = ["pca1_cum_1975","pca1_cum_1990", "pca1_cum_2000", "pca1_cum_2014"]
id1_pca_cols = ["id1_pca1_cum_1975","id1_pca1_cum_1990", "id1_pca1_cum_2000", "id1_pca1_cum_2014"]
iso_pca_cols = ["iso_pca1_cum_1975","iso_pca1_cum_1990", "iso_pca1_cum_2000", "iso_pca1_cum_2014"]

years = ["<1975", "1976-1990","1991-2000", "2001-2014"]
fig, ax = plt.subplots()
plt.xticks(ticks=range(0,len(years)), labels=years)

# find particular row
args = docopt(__doc__) 
if args["-r"]:
    arg = args['<location>']
    plot_regional(arg)
elif args["-n"]:
    arg = args['<location>']
    plot_national(arg)
else:
    arg = args['<location>']
    plot_city(arg)
