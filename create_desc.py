import pandas as pd
import numpy as np
import inflect

fua_df = pd.read_pickle("data/FUA_master_ultra_wide_with_contextual_comparisons.pandas")
fua_df["name_1"] = ((fua_df["name_1"]).str.encode('latin-1')).str.decode('utf-8')  # fix encoding problem

# set up cols for data
loc_pca_cols = []
id1_pca_cols = []
iso_pca_cols = []
year_cols = ["1975", "1990", "2000", "2014"]
incremental = True
mode = "inc_"
if not incremental:
    mode = "cum_"

for year in year_cols:
    loc_pca_cols.append("pca1_" + mode + year)
    id1_pca_cols.append("id1_pca1_" + mode + year)
    iso_pca_cols.append("iso_pca1_" + mode + year)
loc_pca_cols.append("pca1_stock")
id1_pca_cols.append("id1_pca1_stock")
iso_pca_cols.append("iso_pca1_stock")
years = ["<1975", "1976-1990", "1991-2000", "2001-2014"]


def get_city_data(arg_city):
    city_df = fua_df.query('efua_name == @arg_city')
    city_df = city_df.sort_values(by=["fua_p_2015"], ascending=False).head(1)
    city_transpose_df = city_df[loc_pca_cols].T
    city_transpose_df.rename(columns={city_transpose_df.columns[0]:"sndi"},inplace=True)
    city_transpose_df["change"] = city_transpose_df.diff()
    city_transpose_df["trend"] = np.sign(city_transpose_df.change).map({-1:"decreasing",1:"increasing"})
    return city_transpose_df


# returns description for trend of that city's sndi
def city_desc(arg_city):
    desc=""
    city_df = get_city_data(arg_city)
    is_increasing = (city_df.trend[1:4] == "increasing")
    is_decreasing = (city_df.trend[1:4] == "decreasing")
    desc += "Overall, the stock level of sprawl in {} is {}. ".format(arg_city, round(city_df.sndi["pca1_stock"], 2))
    if is_increasing.all() or is_decreasing.all():
        desc += "New street construction in {} has been {} in sprawl over time. ".format(arg_city, city_df.trend[1])
        if city_df.change[1] > city_df.change[3]:
            if is_increasing.all():
                desc += "This increase has slowed: between {} and {}, SNDi rose by {} points, but between {} and {}, it rose by just {}. "\
                    .format(years[0],years[1], round(city_df.change[1],2),years[2], years[3], round(city_df.change[3],2))
            elif is_decreasing.all():
                desc += "This decrease has quickened: between {} and {}, SNDi fell by {} points, but between {} and {}, it fell by just {}. "\
                    .format(years[0], years[1], round(abs(city_df.change[1]), 2),years[2], years[3], round(abs(city_df.change[3]),2))
    elif city_df.trend[1] == "increasing" and city_df.trend[3] == "decreasing":
        desc += "In {}, new street layouts initially increased in level of sprawl, until the peak in {}. "\
            .format(arg_city, years[2] if city_df.trend[2] == "increasing" else years[1])
    elif city_df.trend[1] == "decreasing" and city_df.trend[3] == "increasing":
        desc += "In {}, the level of sprawl in new street layouts dipped, increasing in {} onwards. " \
            .format(arg_city, years[1] if city_df.trend[2] == "increasing" else years[2])
    else:
        no_data = []
        for i in range(0,4):
            if pd.isnull(city_df.sndi[i]):
                no_data.append(years[i])
            else:
                desc += "In {}, the SNDi was {}. ".format(years[i], round(city_df.sndi[i],2))
        desc += "Data was not available for the following time periods: {}. ".format(no_data)
    return desc


# returns the region name of a given city
def get_region(arg_city):
    return fua_df.query('efua_name == @arg_city').head(1).name_1.item()


def get_city_ranking(arg_city):  # ranking of cities in the same region (descending, ie 1 = most sprawl)
    this_region = get_region(arg_city)
    region_df = fua_df[fua_df["name_1"] == this_region]
    region_df.set_index("efua_name", inplace=True)
    year_cols.append("stock")
    ranking = pd.DataFrame()
    # ranking["efua_name"] = region_df["efua_name"]
    for i in range(0, 5):
        ranking["rank_{}".format(year_cols[i])] = region_df[loc_pca_cols[i]].rank(method='max', ascending=False).astype(int)
    return ranking


def ranking_desc(arg_city):
    ranking = get_city_ranking(arg_city)
    city_ranks = ranking.loc[arg_city]
    p = inflect.engine()
    desc="{} is the {}-most sprawling city out of the {} cities in {}"\
        .format(arg_city, p.number_to_words(p.ordinal(city_ranks["rank_stock"])), ranking.shape[0], get_region(arg_city))
    #TODO: describe trend in ranking
    return desc

def which_percentile(city, regional):
    if city < regional["25%"].item(): return "in the 0 - 25th percentile"
    elif city < regional["50%"].item(): return "in the 25th - 50th percentile"
    elif city < regional["75%"].item(): return "in the 50th - 75th percentile"
    else: return "in the 75th - 100th percentile"
