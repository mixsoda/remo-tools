#!/bin/bash
CDIR=`dirname ${0}`
cd ${CDIR}/

TOKEN=`cat ../token.txt`
TARGET_AIRCON_ID=`cat ../aircon_id.txt`
NOW=`date +"%Y-%m-%dT%T"`
NOW_DATE=`date +"%Y-%m-%d"`
NOW_UNIXTIME=`date +%s`

RETRY_TIME=615 #sec
TRIGGER_TIME=0
TRIGGER_MODE="OFF"

#Trigger Conf.
COOLER_TRIGGER_TEMP=25
WARMER_TRIGGER_TEMP=15

COOLER_SETTING=27
WARMER_SETTING=18

ON_DAY_AM_H=07
ON_DAY_AM_M=45

ON_DAY_PM_H=17
ON_DAY_PM_M=45

ON_HOLIDAY_AM_H=09
ON_HOLIDAY_AM_M=00

ON_HOLIDAY_PM_H=18
ON_HOLIDAY_PM_M=00

#休みの日(土,日,祝日)かどうか調べる
TODAY=`date +"%Y-%m-%d"`
DOW=`date +"%w"`
JPHOLIDAY=`cat ../holiday.json | grep ${TODAY} | wc -l`
HOLIDAY=0

if [ ${DOW} -eq 0 -o ${DOW} -eq 6 -o ${JPHOLIDAY} -eq 1 ]; then 
    HOLIDAY=1
fi

#check room enviroment
RTEMP=`../sensor/get_temp.sh  | cut -d'.' -f 1`
RHU=`../sensor/get_hu.sh`
RIL=`../sensor/get_il.sh  | cut -d'.' -f 1`

#エアコン起動判定
#温度
if [ ${RTEMP} -ge ${COOLER_TRIGGER_TEMP} ]; then 
    TRIGGER_MODE="COOLER"
fi
if [ ${RTEMP} -le ${WARMER_TRIGGER_TEMP} ]; then 
    TRIGGER_MODE="WARMER"
fi

#time
if [ ${HOLIDAY} -eq 0 ]; then 
    # 平日
    ON_DAY_AM_UNIXTIME=`date +%s --date "${NOW_DATE} ${ON_DAY_AM_H}:${ON_DAY_AM_M}"`
    ON_DAY_PM_UNIXTIME=`date +%s --date "${NOW_DATE} ${ON_DAY_PM_H}:${ON_DAY_PM_M}"`
    if [ ${NOW_UNIXTIME} -ge ${ON_DAY_AM_UNIXTIME} ] && [ ${NOW_UNIXTIME} -le `expr ${ON_DAY_AM_UNIXTIME} + ${RETRY_TIME}` ]; then
        TRIGGER_TIME=1
    fi
    if [ ${NOW_UNIXTIME} -ge ${ON_DAY_PM_UNIXTIME} ] && [ ${NOW_UNIXTIME} -le `expr ${ON_DAY_PM_UNIXTIME} + ${RETRY_TIME}` ]; then
        TRIGGER_TIME=1
    fi
else
    # 休日
    ON_HOLIDAY_AM_UNIXTIME=`date +%s --date "${NOW_DATE} ${ON_HOLIDAY_AM_H}:${ON_HOLIDAY_AM_M}"`
    ON_HOLIDAY_PM_UNIXTIME=`date +%s --date "${NOW_DATE} ${ON_HOLIDAY_PM_H}:${ON_HOLIDAY_PM_M}"`
    if [ ${NOW_UNIXTIME} -ge ${ON_HOLIDAY_AM_UNIXTIME} ] && [ ${NOW_UNIXTIME} -le `expr ${ON_HOLIDAY_AM_UNIXTIME} + ${RETRY_TIME}` ]; then
        TRIGGER_TIME=1
    fi
    if [ ${NOW_UNIXTIME} -ge ${ON_HOLIDAY_PM_UNIXTIME} ] && [ ${NOW_UNIXTIME} -le `expr ${ON_HOLIDAY_PM_UNIXTIME} + ${RETRY_TIME}` ]; then
        TRIGGER_TIME=0
    fi
fi

#Logging
echo "[CHECK]" TIME=${NOW}, HOLIDAY=${HOLIDAY}, RT=${RTEMP}, RH=${RHU}, RIL=${RIL}, TRIGGER_TIME=${TRIGGER_TIME}, TRIGGER_MODE=${TRIGGER_MODE} >> log.txt

if [ ${TRIGGER_TIME} -eq 0 ] || [ ${TRIGGER_MODE} = "OFF" ] ; then 
    exit
fi

#エアコンのON/OFF状態を調べる
AIRCON_POWER=`./get_aircon_settings.sh button`
if [ ${AIRCON_POWER} = "power-off" ]; then 
    AIRCON_POWER="OFF"
else
    AIRCON_POWER="ON"
fi

if [ ${AIRCON_POWER} = "OFF" ]; then 
    if [ ${TRIGGER_MODE} = "COOLER" ]; then
        echo "[**COOLER-SEND**]" TRIGGER_MODE=${TRIGGER_MODE} COOLER_SETTING=${COOLER_SETTING} >> log.txt
    else
        echo "[**WARMER-SEND**]" TRIGGER_MODE=${TRIGGER_MODE} WARMER_SETTING=${WARMER_SETTING} >> log.txt
    fi
fi