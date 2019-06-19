from laika import AstroDog
from laika.gps_time import GPSTime
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.basemap import Basemap
import logging as log
log.basicConfig(level=log.DEBUG)

import sys
sys.path.insert(0, '../../inputs/')
import getSpWxData

start = datetime(2003,1,1,0,0,0)
end = datetime(2004,1,1,0,0,0)
# end = datetime(2006,1,1,0,0,0)

num_save = 10

lon_bins = np.linspace(-180, 180, 73)
lat_bins = np.linspace(-90, 90, 73)

subbins = len(lon_bins) * len(lat_bins)
daterange = pd.date_range(start,end,freq='1H')
num_entries = len(daterange) * subbins

data = np.zeros(num_save*subbins, dtype=[('lat', 'f2'), ('lon', 'f2'), ('f107', 'f2'), ('kp', 'f2'), ('time', 'f2'), ('doy', 'f2'), ('tec', 'f2')])

kps, dts1 = getSpWxData.getKp(start,end)
f107s, dts2 = getSpWxData.getF107(start,end)

kp_data = pd.DataFrame(data=list(zip(kps, dts1)), columns=['kp', 'dt'])
kp_data=kp_data.set_index('dt')
f107_data = pd.DataFrame(data=list(zip(f107s, dts2)), columns=['f107', 'dt'])
f107_data=f107_data.set_index('dt')

for idx, timestamp in enumerate(daterange.to_pydatetime()):

    save_idx = idx % num_save

    print(timestamp)
    i_kp = [kp_data.index.get_loc(t, method='nearest') for t in [timestamp]]
    kp = kp_data.iloc[i_kp, :]['kp'][0]
    i_f107 = [f107_data.index.get_loc(t, method='nearest') for t in [timestamp]]
    f107 = f107_data.iloc[i_f107, :]['f107'][0]

    time = GPSTime.from_datetime(timestamp)

    dog = AstroDog()
    ionex_map = dog.get_ionex(time)

    doy = timestamp.timetuple().tm_yday
    fTime = timestamp.hour + timestamp.minute/60.

    sub_idx = 0
    for lat in lat_bins:
        for lon in lon_bins:
            tec = dog.get_ionex(time).get_TEC((lat,lon), time)
            data[subbins*save_idx + sub_idx] = lat,lon,f107,kp,fTime,doy,tec
            sub_idx = sub_idx + 1

    if (idx + 1) % num_save == 0:
        print("Storing results checkpoint...")
        try:
            dataframe = pd.read_pickle('data_pd.pkl')
        except:
            dataframe = pd.DataFrame()
        df_tmp = pd.DataFrame(data)
        df_tmp = df_tmp.loc[(df_tmp['f107'] > 0)]
        dataframe = pd.concat([dataframe,df_tmp], sort=False)
        dataframe.to_pickle('data_pd.pkl')
        data = np.zeros(num_save*subbins, dtype=[('lat', 'f2'), ('lon', 'f2'), ('f107', 'f2'), ('kp', 'f2'), ('time', 'f2'), ('doy', 'f2'), ('tec', 'f2')])

df = pd.DataFrame(data)
df.to_pickle('data_pd.pkl')
