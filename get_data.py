from metnocharts import collection
from shapely import wkb
import binascii
import numpy as np
import geopandas as gpd
from matplotlib import pyplot as plt

def get_extents(query, timestamp, collection):
    return extent_list

coll = collection.ChartsCollection('newcharts',
                                   'chartsuser',
                                   'icecharts',
                                   dbtype='postgres'
                                   )
coll._connect()

shapes = {}

year=2017
month=1
day=30



query = " ".join(("with a as ( select * from sval_bmask ),",
                  "b as ( select ice_type, geom from merged_charts where",
                  "extract(YEAR from dates)={} and".format(year),
                  "extract(MONTH from dates)={} and".format(month),
                  # "extract(DAY from dates)={} and".format(day),
                  "( ice_type = 'Fast Ice' or ice_type = 'Very Close Drift Ice' ) )",
                  "select st_union(b.geom) as geom from a, b where st_overlaps(a.wkb_geometry, b.geom)"))

ndf = coll.to_gpd(query)
mask = gpd.GeoDataFrame.from_file('buffer_mask')
mask.to_crs({'init': 'epsg:4326'}, inplace=True)
df_intersection = gpd.overlay(mask, ndf, how='intersection')
df_intersection.to_file('test')
