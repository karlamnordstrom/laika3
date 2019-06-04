from laika import AstroDog
from laika.gps_time import GPSTime
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.basemap import Basemap

import sys
sys.path.insert(0, '../../')
from inputs import getSpWxData

start = datetime(2003,1,1,0,0,0)
# end = datetime(2016,1,1,0,0,0)
end = datetime(2003,2,1,0,0,0)

lon_bins = np.linspace(-180, 180, 73)
lat_bins = np.linspace(-90, 90, 73)

subbins = len(lon_bins) * len(lat_bins)
daterange = pd.date_range(start,end,freq='2H')
num_entries = len(daterange) * subbins

data = np.empty(num_entries, dtype=[('lat', 'f2'), ('lon', 'f2'), ('f107', 'f2'), ('kp', 'f2'), ('time', 'f2'), ('doy', 'f2'), ('tec', 'f2')])

for idx, timestamp in enumerate(daterange.to_pydatetime()):

    print(timestamp)
    time = GPSTime.from_datetime(timestamp)

    dog = AstroDog()
    ionex_map = dog.get_ionex(time)

    doy = timestamp.timetuple().tm_yday
    fTime = timestamp.hour + timestamp.minute/60.
    kp, dts = getSpWxData.getKp(timestamp)
    f107, dts = getSpWxData.getF107(timestamp)

    # This is embarrassingly slow, but can't do much better without rewriting IonexMap in laika
    sub_idx = 0
    for lat in lat_bins:
        for lon in lon_bins:
            tec = dog.get_ionex(time).get_TEC((lat,lon), time)
            data[subbins*idx + sub_idx] = lat,lon,f107,kp,fTime,doy,tec
            sub_idx = sub_idx + 1

df = pd.DataFrame(data)
print(df)
df.to_pickle('data_pd.pkl')
