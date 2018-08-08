#%%
#
# Graphing for air-con operation time
#

#import and initialize
import numpy as np
import pandas as pd
from datetime import datetime
import datetime as dt
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.style.use('ggplot') 

#%%
#read data from cvs to pandas data frame
df = pd.read_csv('aircon_state.txt', names=['time', 'power', 'mode', "temp"])
df.time = pd.to_datetime(df.time,format='%Y-%m-%dT%H:%M:%S')
df.time = df.time + dt.timedelta(hours=9)
df = df.set_index('time')
df2 = df.groupby(pd.Grouper(freq='1D'))


optime_count = df2["mode"].value_counts()
optime_cool = pd.DataFrame([], columns=['cool'])
optime_dry = pd.DataFrame([], columns=['dry'])
optime_warm = pd.DataFrame([], columns=['warm'])

for key, value in optime_count.iteritems() :
    if (key[1] == ' cool'):
        df_temp = pd.DataFrame([[15.0*value/60.0]], index=[key[0]], columns=['cool'])
        optime_cool = optime_cool.append(df_temp, sort=True)
    if (key[1] == ' dry'):
        df_temp = pd.DataFrame([[15.0*value/60.0]], index=[key[0]], columns=['dry'])
        optime_dry = optime_dry.append(df_temp, sort=True)
    if (key[1] == ' warm'):
        df_temp = pd.DataFrame([[15.0*value/60.0]], index=[key[0]], columns=['warm'])
        optime_warm = optime_warm.append(df_temp, sort=True)

optime = optime_cool.join(optime_dry, how='outer').join(optime_warm, how='outer')
#pd.concat([optime_cool, optime_dry], join='outer')
#print(optime)

#%%
ax = optime.plot(kind='area', color=['steelblue', 'lightsteelblue', 'tomato'], stacked=True)
#ax.set_xticklabels(optime.index.strftime('%d-%b(%a)'))
ax.set_ylabel('Operating time (hour)')
plt.show()