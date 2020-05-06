# sprawlmapdemo

Repo for sprawlmap region pages mockup & miscellaneous data explorations.

## Demo
* [Canada](canada/page.html)
* [ ] TODO: make it dynamic -- flask app?

## Programs

* `time_graphs.py` is a cmd line program taking a city name as input and outputs a html file with the plotly graphs. 
* `plots.py` has methods to generate plots for city, regional and national levels.

## Data

* `FUA_master_ultra_wide_with_contextual_comparisons.pandas` is the data aggregated over GHSL FUA geometries. Each row also has data for the FUA's region (identified by `id_1` and `name_1`) and country (identified by `iso` and `name_0`).

  

