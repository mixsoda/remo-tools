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

#plt.style.use('ggplot')

#function definition
def calc_optime(df, group_priod) :
    df2 = df.groupby(pd.Grouper(freq=group_priod))

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
    print(optime)

    return optime

#%%
#read data from cvs to pandas data frame
df = pd.read_csv('../logging/logs/aircon_state.txt', names=['time', 'power', 'mode', "temp"])
df.time = pd.to_datetime(df.time,format='%Y-%m-%dT%H:%M:%S')
df.time = df.time + dt.timedelta(hours=9)
df = df.set_index('time')

df_temp = pd.read_csv('../logging/logs/temp.txt', names=['time', 'temp'])
df_temp.time = pd.to_datetime(df_temp.time,format='%Y-%m-%dT%H:%M:%SZ')
df_temp.time = df_temp.time + dt.timedelta(hours=9)
df_temp = df_temp.set_index('time')
df_temp_1w_mean = df_temp.resample("W").mean().rename(columns={'temp': 'mean'})
df_temp_1w_max = df_temp.resample("W").max().rename(columns={'temp': 'max'})
df_temp_1w_min = df_temp.resample("W").min().rename(columns={'temp': 'min'})

df_temp_1w_all = df_temp_1w_mean.join(df_temp_1w_max, how='outer').join(df_temp_1w_min, how='outer')
print(df_temp_1w_all)

#%%
#Air-Con Operating time (hours/day)
ax = calc_optime(df,"1D").plot(kind='area', color=['steelblue', 'lightsteelblue', 'tomato'], stacked=True,linewidth = 0.0)
ax.xaxis_date()
ax.set_ylabel('Operating time (hours/day)')
#plt.savefig("visualize_aircon_uptime_"+str(dt.date.today())+".png")
plt.show()

#%%
#Air-Con Operating time (hours/week)
w = 7.0
optime = calc_optime(df,"1W")
fig, ax = plt.subplots()

sb_cool = ax.bar(optime.index, optime.cool, width=w, color='steelblue')
sb_dry = ax.bar(optime.index, optime.dry, width=w, color='lightsteelblue')
sb_warm = ax.bar(optime.index, optime.warm, width=w, color='tomato')

ax.xaxis_date()
ax.set_ylabel('Operating time (hours/week)')
plt.legend((sb_cool, sb_dry, sb_warm), ('cool', 'dry', 'warm'))
plt.title("Air Conditioner Operating time")

fig.autofmt_xdate()
plt.savefig("visualize_aircon_uptime_week_"+str(dt.date.today())+".png")
plt.show()


#%%
w = 7.0
optime = calc_optime(df,"1W")
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

ax1.set_title("Air Conditioner Operating time and Room Temperature")

sb_cool = ax1.bar(optime.index, optime.cool, width=w, color='steelblue')
sb_dry = ax1.bar(optime.index, optime.dry, width=w, color='lightsteelblue')
sb_warm = ax1.bar(optime.index, optime.warm, width=w, color='tomato')

ax1.legend((sb_cool, sb_dry, sb_warm), ('cool', 'dry', 'warm'))
ax1.xaxis_date()
ax1.set_ylabel('Uptime (hours/week)')

line_temp = ax2.plot(df_temp_1w_all.index, df_temp_1w_all["mean"], color="limegreen")
line_temp_fill = ax2.fill_between(df_temp_1w_all.index, df_temp_1w_all["max"], df_temp_1w_all["min"], alpha=0.25, color="palegreen")
ax2.set_ylabel('RT (℃)')

fig.autofmt_xdate()
plt.savefig("visualize_aircon_uptime_temp_"+str(dt.date.today())+".png")
plt.show()


#%%
