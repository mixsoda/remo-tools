#%%
#
# Aggregate and visualize the nature remo motion sensor data
#

#import and initialize
import numpy as np
import pandas as pd
from datetime import datetime
import datetime as dt
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#read data from cvs to pandas data frame
df_mo = pd.read_csv('mo.txt', names=['time', 'motion'])
df_mo.time = pd.to_datetime(df_mo.time,format='%Y-%m-%dT%H:%M:%SZ')
df_mo.time = df_mo.time + dt.timedelta(hours=9)
df_mo = df_mo.set_index('time')

df_mo["weekday"] = df_mo.index.weekday
df_mo["hour"] = df_mo.index.hour

#%%
#add dummy data
for i in range(24):
    df_mo.loc[i] = [0, i%7, i%23]

#%%
df_mo_pivot = df_mo.pivot_table(index=["weekday"], columns=["hour"], values="motion", aggfunc=sum)
df_mo_pivot.fillna(0, inplace=True)
print(df_mo_pivot)

#%%
plt.imshow(df_mo_pivot, cmap="YlGn")
ax = plt.gca()

# ticks
ax.set_xticks(np.arange(0, 24, 3))
ax.set_yticks(np.arange(0, 7, 2))
ax.set_xticks(np.arange(-.5, 24, 1), minor=True)
ax.set_yticks(np.arange(-.5, 7, 1), minor=True)

ax.spines["right"].set_color("none")
ax.spines["top"].set_color("none")
ax.spines["bottom"].set_color("none")
ax.spines["left"].set_color("none")

ax.grid(which='minor', color='white', linestyle='-', linewidth=2)
ax.set_yticklabels(['Mon', 'Wed', 'Fri', 'Sun'])
plt.tick_params(which='both', bottom=False, left=False, labelsize=8)
plt.title("Motion sensor", fontsize=10)

plt.show()