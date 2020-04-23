# sprawlmapdemo

Repo for sprawlmap region pages mockup & miscellaneous data explorations.

## Demo
* [Canada](canada/canada.html)

## Programs
* `time_graphs.py` is a cmd line program taking a city name as input and outputs a html file with the plotly graphs. 
* `plots.py` is a cmd line program taking an FUA name as input and outputs a html file with regional comparison plots.

## Data
* `city-sndi.csv` from [this](https://sprawl.research.mcgill.ca/publications/2020-PNAS-sprawl/cities-ranked-pca1.html)
* `country-sndi.csv` from [this](https://sprawl.research.mcgill.ca/publications/2020-PNAS-sprawl/countries-ranked-pca1.html)
* `FUA_master_sndi.csv` is the sndi data aggregated over GHSL FUA geometries. Each row also has data for the FUA's region (identified by `id_1` and `name_1`) and country (identified by `iso` and `name_0`). 

