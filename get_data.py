from metnocharts import collection
from shapely import wkb
import binascii
import numpy as np
import geopandas as gpd
from matplotlib import pyplot as plt
import sys
import datetime
import calendar

def get_extents(timestamp, collection):
    year = timestamp.year
    month = timestamp.month
    day = timestamp.day
    weekday = timestamp.weekday()
    if (calendar.day_name[weekday] == 'Saturday' or calendar.day_name[weekday] == 'Sunday'):
        time_delta = datetime.timedelta(days=2)
        timestamp += time_delta
    try:
        query = " ".join(("with a as ( select * from sval_bmask ),",
                          "b as ( select ice_type, geom from merged_charts where",
                          "extract(YEAR from dates)={} and".format(year),
                          "extract(MONTH from dates)={} and".format(month),
                          "extract(DAY from dates)={} and".format(day),
                          "( ice_type = 'Fast Ice' or ice_type = 'Very Close Drift Ice' ) )",
                          "select st_union(b.geom) as geom from a, b where st_overlaps(a.wkb_geometry, b.geom)"))

        ndf = coll.to_gpd(query)
        mask = gpd.GeoDataFrame.from_file('buffer_mask')
        mask.to_crs({'init': 'epsg:4326'}, inplace=True)
        df_intersection = gpd.overlay(mask, ndf, how='intersection')
        df_intersection.to_file('test')
        ofilename = 'test-{}-{}'.format(timestamp.year, timestamp.month)
        print(ofilename)
        df_intersection.to_file(ofilename)
        return df_intersection
    except:
        pass

coll = collection.ChartsCollection('newcharts',
                                   'chartsuser',
                                   'icecharts',
                                   dbtype='postgres'
                                   )
coll._connect()

year=range(2000, 2018)
months=[1,2,3,4,5,6,7]
day=15
d = 15

dates = [datetime.datetime(y, m, d) for y in year for m in months]
for date in dates:
    res = get_extents(date, coll)
