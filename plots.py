#!/usr/local/bin/python3
import pandas as pd
import matplotlib as plt

fua_df = pd.read_csv("FUA_master_sndi.csv")
atlas_cities = pd.read_csv("cities-sndi.csv")

# canada_df = fua_df[fua_df["iso"]=="CAN"]

city_in_atlas = fua_df["efua_name"].isin(atlas_cities["city"])
fua_df[city_in_atlas]