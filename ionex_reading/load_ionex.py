from laika import AstroDog
from laika.gps_time import GPSTime
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

def setup_map(ax,dn=None):
    """
    Sets up the map

    :param ax: Input axis
    :return: instance of Basemap
    """
    # m = Basemap(projection='kav7', lon_0=0, resolution='c', ax=ax)
    #m.drawparallels(np.arange(-90., 91., 30.), labels=[0, 0, 0, 0])
    #m.drawmeridians(np.arange(-180., 181., 60.), labels=[0, 0, 0, 0])
    # m.shadedrelief(scale=0.35)

    m = Basemap(projection='mill', lat_0 = 40, lon_0 = 0, resolution = 'c', ax=ax)
    m.shadedrelief(scale = 0.5)
    # m.drawcoastlines()
    # m.drawcountries()
    # m.drawstates()
    #m.fillcontinents(color='coral', lake_color='aqua')
    m.drawparallels(np.arange(-90., 120., 30.))
    m.drawmeridians(np.arange(0., 420., 60.))
    if dn:
        m.nightshade(dn)
    #m.drawmapboundary(fill_color='aqua')
    return m


time = GPSTime.from_datetime(datetime(2019,5,31,11,0,0))

dog = AstroDog()

ionex_map = dog.get_ionex(time)

# print(dog.get_ionex(time).get_TEC((5,5), time))

# Setup map:
fig = plt.figure(1, figsize=(18, 12))
plt.clf()
ax = fig.add_subplot(111)
m = setup_map(ax)

lon_bins = np.linspace(-180, 180, 73)
lat_bins = np.linspace(-90, 90, 37)

# print(lon_bins, lat_bins)

tec = []

for i in lat_bins:
    tmp = []
    for j in lon_bins:
        tmp.append(ionex_map.get_TEC( (i,j), time ))
    tec.append(tmp)

tec = np.array(tec)
yy, xx = np.meshgrid(lat_bins, lon_bins)

xx, yy = m(xx, yy)

m.pcolormesh(xx, yy, tec.transpose(), cmap='YlGnBu', alpha=0.8)

plt.show()
