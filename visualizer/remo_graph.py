#
# Nature remo sensor data visualizer
#

#import and initialize
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.style.use('ggplot') 

#read data from cvs to pandas data frame
df_temp = pd.read_csv('temp.txt', names=['time', 'temp'])
df_temp.time = pd.to_datetime(df_temp.time,format='%Y-%m-%dT%H:%M:%SZ')
df_temp.time = df_temp.time + dt.timedelta(hours=9)

df_hu = pd.read_csv('hu.txt', names=['time', 'hu'])
df_hu.time = pd.to_datetime(df_hu.time,format='%Y-%m-%dT%H:%M:%SZ')
df_hu.time = df_hu.time + dt.timedelta(hours=9)

df_il = pd.read_csv('il.txt', names=['time', 'il'])
df_il.time = pd.to_datetime(df_il.time,format='%Y-%m-%dT%H:%M:%SZ')
df_il.time = df_il.time + dt.timedelta(hours=9)

#data marge
df = pd.merge(df_temp, df_hu, how='outer', on='time')
df = pd.merge(df, df_il, how='outer', on='time')
df = df.sort_values('time')
df = df.reset_index(drop=True)
df = df.interpolate().resample('8H', on='time').mean()

#output stats
#print('Temperature::')
#print(df_temp.describe())
#print('Humidity::')
#print(df2.describe())

#plots
df.plot(subplots=True, title='Nature Remo sensor data (all)')

plt.show()