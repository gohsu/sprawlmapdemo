import pandas as pd
import inflect
import get_data

mode = "incremental"
years = ["<1975", "1976-1990", "1991-2000", "2001-2014"]

# returns description for trend of that city's sndi
def city_desc(arg_city):
    desc=""
    city_df = get_data.get_city_data(arg_city, mode)
    desc += "Overall, the stock level of sprawl in {} is {}. ".format(arg_city, round(city_df.sndi["pca1_stock"], 2))
    if city_df.sndi[0:4].is_monotonic or city_df.sndi[0:4].is_monotonic_decreasing:
        desc += "New street construction in {} has been {} in sprawl over time. ".format(arg_city, city_df.trend[1])
        if city_df.change[1] > city_df.change[3]:
            if city_df.sndi[0:4].is_monotonic:
                desc += "This increase has slowed: between {} and {}, SNDi rose by {} points, but between {} and {}, it rose by just {}. "\
                    .format(years[0],years[1], round(city_df.change[1],2),years[2], years[3], round(city_df.change[3],2))
            elif city_df.sndi[0:4].is_monotonic_decreasing:
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
        if len(no_data) is not 0:
            desc += "Data was not available for the following time periods: {}. ".format(no_data)
    return desc


def ranking_desc(arg_city):
    ranking = get_data.get_city_ranking(arg_city, mode)
    ranking.set_index('uc_nm_mn', inplace=True)
    city_ranks = ranking.loc[arg_city]
    p = inflect.engine()
    desc = "To date, {} is the {}-most sprawling city out of the {} cities in {}. "\
        .format(arg_city, p.ordinal(int(city_ranks["rank_stock"])), ranking.shape[0], get_data.get_region_name_from_city(arg_city))
    desc += "Its ranking has {} overall. "\
        .format("improved" if city_ranks.diff()[1:4].mean() >= 0 else "worsened")
    desc += "In {}, it ranked {}, ".format(years[0],p.ordinal(int(city_ranks[0])))
    duplicated = city_ranks.duplicated()
    if duplicated[1:4].all():
        desc += " and remained in this position since."
    else:
        no_data = []
        for i in range(1, 4):
            if pd.isnull(city_ranks[i]):
                no_data.append(years[i])
            else:
                desc += "ranked {} in {}".format(p.ordinal(int(city_ranks[i])), years[i])
                if i == 3: desc += ". "
                else: desc += " and "
        if len(no_data) is not 0:
            desc += "There was no ranking in these years due to unavailable data: {}".format(no_data)
    return desc

