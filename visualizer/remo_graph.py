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
#plt.style.use('dark_background') 

#read data from cvs to pandas data frame
df_temp = pd.read_csv('../logging/logs/temp.txt', names=['time', 'temp'])
df_temp.time = pd.to_datetime(df_temp.time,format='%Y-%m-%dT%H:%M:%SZ')
df_temp.time = df_temp.time + dt.timedelta(hours=9)
df_temp = df_temp.set_index('time')

df_hu = pd.read_csv('../logging/logs/hu.txt', names=['time', 'hu'])
df_hu.time = pd.to_datetime(df_hu.time,format='%Y-%m-%dT%H:%M:%SZ')
df_hu.time = df_hu.time + dt.timedelta(hours=9)
df_hu = df_hu.set_index('time')

df_il = pd.read_csv('../logging/logs/il.txt', names=['time', 'il'])
df_il.time = pd.to_datetime(df_il.time,format='%Y-%m-%dT%H:%M:%SZ')
df_il.time = df_il.time + dt.timedelta(hours=9)
df_il = df_il.set_index('time')

#extract last week data
df_all = df_temp.join(df_hu, how='outer').join(df_il, how='outer')
df_lastweek = df_all[datetime.now()-dt.timedelta(weeks=1):datetime.now()]
print(df_lastweek)

#smoothing, max, min
df_temp_smooth_mean = df_temp.resample("W").mean().rename(columns={'temp': 'temp_mean'})
df_temp_smooth_max = df_temp.resample("W").max().rename(columns={'temp': 'temp_max'})
df_temp_smooth_min = df_temp.resample("W").min().rename(columns={'temp': 'temp_min'})

df_hu_smooth_mean = df_hu.resample("W").mean().rename(columns={'hu': 'hu_mean'})
df_hu_smooth_max = df_hu.resample("W").max().rename(columns={'hu': 'hu_max'})
df_hu_smooth_min = df_hu.resample("W").min().rename(columns={'hu': 'hu_min'})

df_il_smooth_mean = df_il.resample("W").mean().rename(columns={'il': 'il_mean'})
df_il_smooth_max = df_il.resample("W").max().rename(columns={'il': 'il_max'})
df_il_smooth_min = df_il.resample("W").min().rename(columns={'il': 'il_min'})

df_temp_smooth_all = df_temp_smooth_mean.join(df_temp_smooth_max, how='outer').join(df_temp_smooth_min, how='outer')
df_hu_smooth_all = df_hu_smooth_mean.join(df_hu_smooth_max, how='outer').join(df_hu_smooth_min, how='outer')

#%%
df_lastweek_smooth = df_lastweek.interpolate('time')
#df_lastweek_smooth.index = df_lastweek_smooth.index.round('15min')
print(df_lastweek_smooth)

#%%
df_all_smooth = df_temp_smooth_mean.join(df_hu_smooth_mean, how='outer').join(df_il_smooth_max, how='outer')
print(df_all_smooth)

#%%
# resampling & interpolate illuminance each 10min
df_il_10min = df_il.resample('10min').mean().interpolate('time')
df_il_sum = (100*df_il_10min/(256*6*24*7)).resample('1W').sum().rename(columns={'il': 'sum_il'})
print(df_il_10min)


#%%
#visualize data
#all
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
cmap = plt.get_cmap("Set2")
ax1.set_title("Sensor data (All period, Temp, Humidity, Illuminance)")

ax1.plot(df_temp_smooth_all.index, df_temp_smooth_all["temp_mean"], color=cmap(1))
ax1.fill_between(df_temp_smooth_all.index, df_temp_smooth_all["temp_max"], df_temp_smooth_all["temp_min"], alpha=0.3, color=cmap(1))
ax1.set_ylabel('RT (℃)')
ax1.xaxis_date()

ax2.plot(df_hu_smooth_all.index, df_hu_smooth_all["hu_mean"], color=cmap(2))
ax2.fill_between(df_hu_smooth_all.index, df_hu_smooth_all["hu_max"], df_hu_smooth_all["hu_min"], alpha=0.3, color=cmap(2))
ax2.set_ylabel('H (%)')
ax2.xaxis_date()

ax3.plot(df_il_sum.index, df_il_sum["sum_il"], "--", alpha=0.3, color=cmap(3))
ax3.fill_between(df_il_sum.index, 0, df_il_sum["sum_il"], alpha=0.3, color=cmap(3))
ax3.set_ylabel('Σil / week')

ax4 = ax3.twinx()
ax4.plot(df_il_smooth_max.index, (100*df_il_smooth_max["il_max"]/256), color=cmap(4))
ax4.set_ylabel('max_il (%)')
ax4.xaxis_date()

fig.autofmt_xdate()
plt.savefig("visualize_sensor_data_all_"+str(dt.date.today())+".png")
plt.show()

#last week
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
cmap = plt.get_cmap("Set2")

ax1.set_title("Sensor data (Last week, Temp, Humidity, Illuminance)")
ax1.plot(df_lastweek_smooth.index, df_lastweek_smooth["temp"], color=cmap(1))
ax1.set_ylabel('RT (℃)')
ax1.xaxis_date()

ax2.plot(df_lastweek_smooth.index, df_lastweek_smooth["hu"], color=cmap(2))
ax2.set_ylabel('H (%)')
ax2.xaxis_date()

ax3.plot(df_lastweek_smooth.index, df_lastweek_smooth["il"], color=cmap(4))
ax3.set_ylabel('il')
ax3.xaxis_date()

fig.autofmt_xdate()
plt.savefig("visualize_sensor_data_week_"+str(dt.date.today())+".png")
plt.show()


#%%
