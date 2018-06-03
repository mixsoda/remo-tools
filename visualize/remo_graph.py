import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


#read data from cvs to pandas data frame
df = pd.read_csv('temp.txt', names=['time', 'temp'])
df.time = pd.to_datetime(df.time,format='%Y-%m-%dT%H:%M:%SZ')
df.time = df.time + dt.timedelta(hours=9)

df2 = pd.read_csv('hu.txt', names=['time', 'hu'])
df2.time = pd.to_datetime(df2.time,format='%Y-%m-%dT%H:%M:%SZ')
df2.time = df2.time + dt.timedelta(hours=9)

#output stats
print('Temperature::')
print(df.describe())
print('Humidity::')
print(df2.describe())

#plots
fig = plt.figure()

ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)

ax1.set_title('Living Room')
ax2.set_xlabel('Time')

#temperature
ax1.plot(df['time'],df['temp'], color='red')
ax1.set_ylabel('Temperature')
ax1.set_ylim([10,30])


#humidity
ax2.plot(df2['time'],df2['hu'], color='blue')
ax2.set_ylabel('Humidity')
ax2.set_ylim([10,70])

#layout x-axis
days = mdates.AutoDateLocator()
daysFmt = mdates.DateFormatter("%d %b")
ax2.xaxis.set_major_locator(days)
ax2.xaxis.set_major_formatter(daysFmt)
fig.autofmt_xdate(rotation=45)

plt.show()