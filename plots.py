#!/usr/local/bin/python3
""" Input a city name to create a html file with comparison plots.

Usage:
    plots.py [options] <location> 
    
Options:
    -r      regional
    -n      national
"""

import matplotlib.pyplot as plt
import numpy as np
import random
import get_data

mode = "incremental"
years = ["<1975", "1976-1990", "1991-2000", "2001-2014"]  # for x-axis labelling


def init_pyplot():
    plt.style.use('seaborn')
    params = {'axes.titlesize': 20,
              'axes.labelsize': 16,
              'xtick.labelsize': 12,
              'ytick.labelsize': 12,
              'legend.fontsize': 12}
    plt.rcParams.update(params)


def plot_city(arg_city, arg_mode):  # returns the plot as a Figure object
    init_pyplot()
    city_df = get_data.get_city(arg_city)
    pca_cols = get_data.set_pca_cols(get_data.set_mode(arg_mode))
    loc_pca = city_df[pca_cols.get('loc_pca_cols')].values.reshape(-1)[0:4]  # don't plot stock
    id1_pca = city_df[pca_cols.get('id1_pca_cols')].values.reshape(-1)[0:4]
    iso_pca = city_df[pca_cols.get('iso_pca_cols')].values.reshape(-1)[0:4]
    # make the plot
    fig, ax = plt.subplots()
    xs = np.arange(4)
    ax.set_xticks(xs)
    ax.set_xticklabels(labels=years)
    mask = np.isfinite(loc_pca)
    ax.plot(xs[mask], loc_pca[mask], color='red', marker='o', lw=2, label=arg_city, zorder=10)  # city plot
    mask_id1 = np.isfinite(id1_pca)
    ax.plot(xs[mask_id1], id1_pca[mask_id1], color='navy', marker='o', markersize=5, lw=1, label="Regional ({})".format(get_data.get_region_name_from_city(arg_city)))
    mask_iso = np.isfinite(iso_pca)
    ax.plot(xs[mask_iso], iso_pca[mask_iso], color='blue', marker='o', markersize=5, lw=1, label="National ({})".format(get_data.get_country_name_from_city(arg_city)))
    # ax.set_title('SNDi in {}'.format(arg_city))
    ax.set_ylabel('SNDi')
    ax.set_xlabel('Years')
    ax.legend()
    fig.tight_layout()
    return fig


def plot_regional(arg_region, arg_mode):  # returns the plot as a Figure object
    init_pyplot()
    region_df = get_data.get_region(arg_region)
    if region_df.empty:
        exit("Region not found.")
    pca_cols = get_data.set_pca_cols(get_data.set_mode(arg_mode))
    id1_pca = region_df[pca_cols.get('id1_pca_cols')].values.reshape(-1)[0:4]
    # make the plot
    fig, ax = plt.subplots()
    xs = np.arange(4)
    ax.set_xticks(xs)
    ax.set_xticklabels(labels=years)
    mask_id1 = np.isfinite(id1_pca)
    ax.plot(xs[mask_id1], id1_pca[mask_id1], color="red", marker='o', lw=2, label=arg_region, zorder=10)  # region plot
    # cities for comparison
    cities_list = get_data.get_region_cities_list(arg_region)
    random.shuffle(cities_list)
    if len(cities_list) > 4:
        cities_list = cities_list[0:4]  # get random 4 cities
    for i in range(0, len(cities_list)):
        city_df = get_data.get_city(cities_list[i])
        loc_pca = city_df[pca_cols.get('loc_pca_cols')].values.reshape(-1)[0:4]
        mask_city = np.isfinite(loc_pca)
        ax.plot(xs[mask_city], loc_pca[mask_city], marker='o', markersize=5, lw=1.5, label=cities_list[i])
    # ax.set_title('SNDi in {}'.format(arg_region))
    ax.set_ylabel('SNDi')
    ax.set_xlabel('Years')
    ax.legend()
    fig.tight_layout()
    return fig


def plot_national(arg_country, arg_mode):  # returns the plot as a Figure object
    init_pyplot()
    country_df = get_data.get_country(arg_country)
    if country_df.empty:
        exit("Country not found.")
    country_df = country_df.groupby(["name_1"]).head(1)  # get a row for each region
    pca_cols = get_data.set_pca_cols(get_data.set_mode(arg_mode))
    iso_pca = country_df[pca_cols.get('iso_pca_cols')].values.reshape(-1)[0:4]
    # plot the country's sndi
    fig, ax = plt.subplots()
    xs = np.arange(4)
    ax.set_xticks(xs)
    ax.set_xticklabels(labels=years)
    mask_iso = np.isfinite(iso_pca)
    ax.plot(xs[mask_iso], iso_pca[mask_iso], color="red", marker='o', lw=2, label=arg_country, zorder=10)  # country plot
    # plot regions for comparison
    regions_list = get_data.get_country_regions_list(arg_country)
    random.shuffle(regions_list)
    if len(regions_list) > 4:
        regions_list = regions_list[0:4]  # use random 4 regions
    for i in range(0, len(regions_list)):
        this_region = get_data.get_region(regions_list[i]).head(1)
        id1_pca = this_region[pca_cols.get('id1_pca_cols')].values.reshape(-1)[0:4]
        mask_id1 = np.isfinite(id1_pca)
        ax.plot(xs[mask_id1], id1_pca[mask_id1], marker='o', markersize=5, lw=1.5, label=this_region.name_1.item())
    # ax.set_title('SNDi in {}'.format(arg_country))
    ax.set_ylabel('SNDi')
    ax.set_xlabel('Years')
    ax.legend()
    fig.tight_layout()
    return fig

# if __name__ == '__main__':
    # import docopt
    # # find particular row
    # args = docopt(__doc__)
    # arg = args['<location>']
    # if args["-r"]:
    #     plot_regional(arg)
    # elif args["-n"]:
    #     plot_national(arg)
    # else:
    #     plot_city(arg)

    # loc = "  "  # Case-sensitive!!!!
    # filename = "canada/plots/{}-plot.png".format(loc.replace(" ","").casefold())

    # plot_city(loc).savefig(filename)
    # plot_regional(loc).savefig(filename)
    # plot_national(loc).savefig(filename)