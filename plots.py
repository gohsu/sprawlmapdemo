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


def to_htmlfile_wlink(arg, arg_lat, arg_lon):
    # write image as html
    htmlfile = open("{}.html".format(arg.replace(" ", "")), 'a+')
    htmlfile.write(
        '<p>See {} on the <a target=”_blank” href="https://sprawlmap.org/#5/{}/{}">sprawlmap</a>.</p>'.format(arg,
                                                                                                              arg_lat,
                                                                                                              arg_lon))
    htmlfile.write((mpld3.fig_to_html(fig)))
    htmlfile.close()


def to_htmlfile(arg, fig):
    # write image as html
    htmlfile = open("{}.html".format(arg.replace(" ", "")), 'a+')
    htmlfile.write((mpld3.fig_to_html(fig)))
    htmlfile.close()


def plot_city(arg_city):  # returns the plot as a Figure object
    city_df = fua_df.query('efua_name == @arg_city')
    city_df = city_df.sort_values(by=["fua_p_2015"], ascending=False)
    city = city_df.head(1)  # largest FUA represents that city
    if city.empty:
        exit("City not found.")
    # fill data
    loc_pca = np.array(city[loc_pca_cols].values.reshape(-1))
    id1_pca = np.array(city[id1_pca_cols].values.reshape(-1))
    iso_pca = np.array(city[iso_pca_cols].values.reshape(-1))
    # make the plot
    fig, ax = plt.subplots()
    xs = np.arange(4)
    ax.set_xticks(xs)
    ax.set_xticklabels(labels=years)
    mask = np.isfinite(loc_pca)
    ax.plot(xs[mask], loc_pca[mask], color='red', marker='o', lw=2, label=arg_city)
    mask_id1 = np.isfinite(id1_pca)
    ax.plot(xs[mask_id1], id1_pca[mask_id1], color='navy', marker='o', markersize=5, lw=1, label="Regional ({})".format(city['name_1'].values[0]))
    mask_iso = np.isfinite(iso_pca)
    ax.plot(xs[mask_iso], iso_pca[mask_iso], color='blue', marker='o', markersize=5, lw=1, label="National ({})".format(city['name_0'].values[0]))
    ax.set_title('SNDi in {}'.format(arg_city))
    ax.set_ylabel('SNDi')
    ax.set_xlabel('Years')
    ax.legend()
    fig.tight_layout()
    return fig


def plot_regional(arg_region):  # returns the plot as a Figure object
    region_df = fua_df[fua_df["name_1"] == arg_region]
    region_df = region_df[region_df["name_0"] == region_df["cntry_name"]]  # make sure cities are from the same country
    region_df = region_df.sort_values(by=["fua_p_2015"], ascending=False)  # sort by population size for comparison
    # make the plot
    fig, ax = plt.subplots()
    xs = np.arange(4)
    ax.set_xticks(xs)
    ax.set_xticklabels(labels=years)
    id1_pca = np.array(region_df[id1_pca_cols].head(1).values.reshape(-1))
    mask_id1 = np.isfinite(id1_pca)
    ax.plot(xs[mask_id1], id1_pca[mask_id1], color="red", marker='o', lw=2, label=arg_region)
    # cities for comparison
    cities_list = region_df["efua_name"].unique()
    if len(cities_list) > 5:
        cities_list = cities_list[0:4]  # only take (up to) 4 most populous cities
    for i in range(0, len(cities_list)):
        this_city = cities_list[i]
        city_query = region_df.query('efua_name == @this_city').head(1)
        city_pca = np.array(city_query[loc_pca_cols].values.reshape(-1))
        mask_city = np.isfinite(city_pca)
        ax.plot(xs[mask_city], city_pca[mask_city], marker='o', markersize=5, lw=1.5, label=this_city)
    ax.set_title('SNDi in {}'.format(arg_region))
    ax.set_ylabel('SNDi')
    ax.set_xlabel('Years')
    ax.legend()
    fig.tight_layout()
    return fig


def plot_national(arg_country):  # returns the plot as a Figure object
    country_df = fua_df[fua_df["name_0"] == arg_country]
    country_df = country_df.groupby(["name_1"]).head(1)  # get a row for each region
    # plot the region's sndi
    fig, ax = plt.subplots()
    xs = np.arange(4)
    ax.set_xticks(xs)
    ax.set_xticklabels(labels=years)
    iso_pca = np.array(country_df[iso_pca_cols].head(1).values.reshape(-1))
    mask_iso = np.isfinite(iso_pca)
    ax.plot(xs[mask_iso], iso_pca[mask_iso], color="red", marker='o', lw=2, label=arg_country)
    # plot regions for comparison
    random_regions_list = np.random.choice(country_df["name_1"], 4)
    ax.set_xticks(ticks=range(0, len(years)))
    ax.set_xticklabels(labels=years)
    for i in range(0, len(random_regions_list)):
        this_region = random_regions_list[i]
        region_query = country_df.query('name_1 == @this_region').head(1)
        region_pca = np.array(region_query[id1_pca_cols].values.reshape(-1))
        mask_region = np.isfinite(region_pca)
        ax.plot(xs[mask_region], region_pca[mask_region], marker='o', markersize=5, lw=1.5, label=this_region)
    ax.set_title('SNDi in {}'.format(arg_country))
    ax.set_ylabel('SNDi')
    ax.set_xlabel('Years')
    ax.legend()
    fig.tight_layout()
    return fig


if __name__ == '__main__':
    # import docopt
    # # find particular row
    # args = docopt(__doc__)

    fua_df = pd.read_pickle("data/FUA_master_ultra_wide_with_contextual_comparisons.pandas")

    # set up cols for data
    loc_pca_cols = []
    id1_pca_cols = []
    iso_pca_cols = []
    year_cols = ["1975", "1990", "2000", "2014"]
    incremental = True  # TODO: arg?
    mode = "inc_"
    if not incremental:
        mode = "cum_"
    for year in year_cols:
        loc_pca_cols.append("pca1_" + mode + year)
        id1_pca_cols.append("id1_pca1_" + mode + year)
        iso_pca_cols.append("iso_pca1_" + mode + year)

    years = ["<1975", "1976-1990", "1991-2000", "2001-2014"]  # for x-axis labelling

    plt.style.use('seaborn')
    params = {'axes.titlesize': 20,
              'axes.labelsize': 16,
              'xtick.labelsize': 12,
              'ytick.labelsize': 12,
              'legend.fontsize': 12}
    plt.rcParams.update(params)

    plot_national("United States").show()

    # arg = args['<location>']
    # if args["-r"]:
    #     plot_regional(arg)
    # elif args["-n"]:
    #     plot_national(arg)
    # else:
    #     plot_city(arg)
