# TRIM

This is the code repository for the Python implementation of the TRip dIversity Measure - TRIM -  which determines the degree of regularity in fine-grained movement behaviour.
TRIM effectively quantify the diversity of an individual's movement behaviour between an origin-destination pair. This measure can categorize users based on the diversity of their movement, including in scenarios where the number of individuals' trips is small. 


# Usage

The level of spatial granularity, i.e., size of the grid cells, can be specified in the params.py, where the default granularity is set to 2 km by 2 km cells. The maximum height of the prefix tree, i.e., budget, can also be set in the same file (MAX_B).

The code is using a subset of GeoLife data expressed as a set of grid cell IDs (geoLife-mapped-level*.txt). The distance between every pair of grid cells is also arealy computed and stored in pairDist-level*.csv.
