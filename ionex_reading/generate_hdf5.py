from laika import AstroDog
from laika.gps_time import GPSTime
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.basemap import Basemap

# def setup_map(ax,dn=None):
#     """
#     Sets up the map
#
#     :param ax: Input axis
#     :return: instance of Basemap
#     """
#     # m = Basemap(projection='kav7', lon_0=0, resolution='c', ax=ax)
#     #m.drawparallels(np.arange(-90., 91., 30.), labels=[0, 0, 0, 0])
#     #m.drawmeridians(np.arange(-180., 181., 60.), labels=[0, 0, 0, 0])
#     # m.shadedrelief(scale=0.35)
#
#     m = Basemap(projection='mill', lat_0 = 40, lon_0 = 0, resolution = 'c', ax=ax)
#     m.shadedrelief(scale = 0.5)
#     # m.drawcoastlines()
#     # m.drawcountries()
#     # m.drawstates()
#     #m.fillcontinents(color='coral', lake_color='aqua')
#     m.drawparallels(np.arange(-90., 120., 30.))
#     m.drawmeridians(np.arange(0., 420., 60.))
#     if dn:
#         m.nightshade(dn)
#     #m.drawmapboundary(fill_color='aqua')
#     return m


start = datetime(2003,1,1,0,0,0)
end = datetime(2016,1,1,0,0,0)

daterange = pd.date_range(start,end,freq='2H')

for timestamp in daterange.to_pydatetime():

    print(timestamp)
    time = GPSTime.from_datetime(timestamp)

    dog = AstroDog()

    ionex_map = dog.get_ionex(time)

    print(dog.get_ionex(time).get_TEC((5,5), time))

    # Setup map:
    fig = plt.figure(1, figsize=(18, 12))
    plt.clf()
    ax = fig.add_subplot(111)

    lon_bins = np.linspace(-180, 180, 73)
    lat_bins = np.linspace(-90, 90, 73)

    # print(lon_bins, lat_bins)
