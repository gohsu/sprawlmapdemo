import pandas as pd

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
    return city_df[loc_pca_cols]


def get_regional_stats(arg_city):  # descriptive statistics for cities in the same region
    this_region = fua_df.query('efua_name == @arg_city').head(1).name_1.item()
    region_df = fua_df[fua_df["name_1"] == this_region]
    return region_df[loc_pca_cols].describe()


def which_percentile(city, regional):
    if city < regional["25%"].item(): return "in the 0 - 25th percentile"
    elif city < regional["50%"].item(): return "in the 25th - 50th percentile"
    elif city < regional["75%"].item(): return "in the 50th - 75th percentile"
    else: return "in the 75th - 100th percentile"


city = "Vancouver"
city_stats_stock = get_city_data(city).pca1_stock.item()
regional_stats_stock = get_regional_stats(city).pca1_stock
print("{} is {} of the {} cities in its region.".format(city, which_percentile(city_stats_stock, regional_stats_stock), str(int(regional_stats_stock["count"]))))



