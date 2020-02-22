#%%
#
# Nature remo sensor data visualizer
#

#import and initialize
import numpy as np
import pandas as pd
from datetime import datetime
import datetime as dt
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#plt.style.use('ggplot') 
plt.style.use('dark_background') 

#read data from cvs to pandas data frame
df_temp = pd.read_csv('../logging/logs/temp.txt', names=['time', 'temp'])
df_temp.time = pd.to_datetime(df_temp.time,format='%Y-%m-%dT%H:%M:%SZ')
df_temp.time = df_temp.time + dt.timedelta(hours=9)

df_hu = pd.read_csv('../logging/logs/hu.txt', names=['time', 'hu'])
df_hu.time = pd.to_datetime(df_hu.time,format='%Y-%m-%dT%H:%M:%SZ')
df_hu.time = df_hu.time + dt.timedelta(hours=9)

df_il = pd.read_csv('../logging/logs/il.txt', names=['time', 'il'])
df_il.time = pd.to_datetime(df_il.time,format='%Y-%m-%dT%H:%M:%SZ')
df_il.time = df_il.time + dt.timedelta(hours=9)

#data marge
df = pd.merge(df_temp, df_hu, how='outer', on='time')
df = pd.merge(df, df_il, how='outer', on='time')
df = df.sort_values(by='time').set_index('time')


df_week = df[datetime.now()-dt.timedelta(weeks=1):datetime.now()]
df = df.interpolate().resample('8H').mean().interpolate()
df_week = df_week.interpolate()

#df_il = df_il.set_index('time')
#df_il = df_il.resample('1H').mean().interpolate().resample('1D').sum()
#df_il = df_il.resample('1D').max()

#plots
df.plot(subplots=True, title='Nature Remo sensor data (all)')
plt.savefig("visualize_sensor_data_all_"+str(dt.date.today())+".png")
df_week.plot(subplots=True, title='Nature Remo sensor data (week)')
plt.savefig("visualize_sensor_data_week_"+str(dt.date.today())+".png")
#df_il.plot()
plt.show()