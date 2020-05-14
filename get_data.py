import pandas as pd
import numpy as np


def load_ghs_data():
    return pd.read_pickle("data/GHS_STAT_UC_master_ultra_wide_with_contextual_comparisons_bestGADMmatches.pandas")


def set_mode(arg):
    col_param = ''
    if arg == "incremental":
        col_param = "inc_"
    elif arg == "cumulative":
        col_param = "cum_"
    return col_param


# set up our columns of interest
def set_pca_cols(mode):
    year_cols = ["1975", "1990", "2000", "2014", "stock"]
    loc_pca_cols, id1_pca_cols, iso_pca_cols = [], [], []
    for i in range(0, len(year_cols)):
        param = ""
        if i == len(year_cols)-1:
            param = year_cols[i]
        else:
            param = mode + year_cols[i]
        loc_pca_cols.append("pca1_" + param)
        id1_pca_cols.append("id1_pca1_" + param)
        iso_pca_cols.append("iso_pca1_" + param)
    return {'loc_pca_cols': loc_pca_cols, 'id1_pca_cols': id1_pca_cols, 'iso_pca_cols': iso_pca_cols, 'year_cols':year_cols}
    # get each with pca_cols("mode").get('loc_pca_cols') for instance


# returns 1 row dataframe of city data
def get_city(arg_city):
    ghs_df = load_ghs_data()
    return ghs_df.query('uc_nm_mn == @arg_city').head(1)


# returns the region name of a given city
def get_region_name_from_city(arg_city):
    return get_city(arg_city).name_1.item()


# returns the country name of a given city
def get_country_name_from_city(arg_city):
    return get_city(arg_city).name_0.item()


# returns dataframe of all cities within given region
def get_region(arg_region):
    ghs_df = load_ghs_data()
    return ghs_df[ghs_df["name_1"] == arg_region].groupby(["uc_nm_mn"]).head(1)  # unique UCs


# returns list of names of cities in a region
def get_region_cities_list(arg_region):
    return get_region(arg_region).uc_nm_mn.unique()


# returns city dataframe of sndi data
def get_city_data(arg_city, arg_mode):
    city_df = get_city(arg_city)
    pca_cols = set_pca_cols(set_mode(arg_mode))
    city_transpose_df = city_df[pca_cols.get('loc_pca_cols')].T
    city_transpose_df.rename(columns={city_transpose_df.columns[0]:"sndi"},inplace=True)
    city_transpose_df["change"] = city_transpose_df.diff()
    city_transpose_df["trend"] = np.sign(city_transpose_df.change).map({-1:"decreasing",1:"increasing"})
    return city_transpose_df


# returns dataframe of rankings for cities in the same region
def get_city_ranking(arg_city, arg_mode):  # ranking of cities in the same region (descending, ie 1 = most sprawl)
    region_df = get_region(get_region_name_from_city(arg_city))
    pca_cols = set_pca_cols(set_mode(arg_mode))
    ranking = pd.DataFrame()
    ranking["uc_nm_mn"] = region_df["uc_nm_mn"]
    for i in range(0, 5):
        ranking["rank_{}".format(pca_cols.get('year_cols')[i])] = region_df[pca_cols.get('loc_pca_cols')[i]].rank(method='max', ascending=False)
    return ranking


# returns dataframe of all UCs in the country (repeats allowed)
def get_country(arg_country):
    ghs_df = load_ghs_data()
    return ghs_df[ghs_df["name_0"] == arg_country]


# returns list of names of cities in a region
def get_country_regions_list(arg_country):
    return get_country(arg_country).name_1.unique()