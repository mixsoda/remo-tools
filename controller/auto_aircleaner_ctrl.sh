#!/bin/bash
CDIR=`dirname ${0}`
cd ${CDIR}/

CONF_FILE='ctrl_aircleaner_config.txt'
ALERT_FILE='../logging/logs/kafun_alert.txt'
LOG_FILE=logs_aircleaner/log_`date +"%Y%m%d"`.txt

NOW=`date +"%Y-%m-%dT%T"`
NOW_DATE=`date +"%Y-%m-%d"`
NOW_UNIXTIME=`date +%s`

RETRY_TIME=45 #sec

#check today is holiday(sat,sun,national holiday) or not
TODAY=`date +"%Y-%m-%d"`
DOW=`date +"%w"`
JPHOLIDAY=`cat ../holiday.json | grep ${TODAY} | wc -l`
HOLIDAY=0

if [ ${DOW} -eq 0 -o ${DOW} -eq 6 -o ${JPHOLIDAY} -eq 1 ]; then 
    HOLIDAY=1
fi

#initialize
STARTUP_TIME=0
TURN_ON_FLAG=0

#check kafun alert flag
LAST_KAFUN_ALERT_DATE=`tail -n 1 ${ALERT_FILE}`
if [ ${LAST_KAFUN_ALERT_DATE} = ${NOW_DATE} ]; then
    TURN_ON_FLAG=1
fi

#read config
while read conf_str; do
    #parse config
    if [ `echo ${conf_str} | cut -c 1` = "#" ]; then
        #echo "comment"
        continue
    fi
    TRIGGER_DAY_TYPE=`echo ${conf_str} | cut -d',' -f 1`
    TRIGGER_HOUR=`echo ${conf_str} | cut -d',' -f 2 | sed 's/^[ \t]*//'`
    TRIGGER_MIN=`echo ${conf_str} | cut -d',' -f 3 | sed 's/^[ \t]*//'`

    case "${TRIGGER_DAY_TYPE}" in
        "WEEK_DAY" )  TRIGGER_DAY_TYPE=0 ;;
        "HOLIDAY" ) TRIGGER_DAY_TYPE=1 ;;
        * ) echo "[READ_CONF_ERROR]" TIME=${NOW}, TRIGGER_DAY_TYPE=${TRIGGER_DAY_TYPE}  >> ${LOG_FILE}
            exit ;;
    esac
    
    #check time trigger
    STARTUP_UNIXTIME=`date +%s --date "${NOW_DATE} ${TRIGGER_HOUR}:${TRIGGER_MIN}"`
    if [ ${TRIGGER_DAY_TYPE} -eq ${HOLIDAY} ] && [ ${NOW_UNIXTIME} -ge ${STARTUP_UNIXTIME} ] && [ ${NOW_UNIXTIME} -le `expr ${STARTUP_UNIXTIME} + ${RETRY_TIME}` ]; then
        STARTUP_TIME=1
    fi

    #set send signal type
    if [ ${STARTUP_TIME} -eq 1 ]; then 
        TRIGGER_MODE=`echo ${conf_str} | cut -d',' -f 4 | sed 's/^[ \t]*//'`
    fi
done < ${CONF_FILE}

#send IR Signal
if [ ${STARTUP_TIME} -eq 1 ] && [ ${TURN_ON_FLAG} -eq 1 ]; then
    case "${TRIGGER_MODE}" in
        "on" )
            ./ctrl_aircleaner.sh on
            echo "[**STARTUP-AIR-CLEANER**]" TIME=${NOW} MODE=${TRIGGER_MODE} >> ${LOG_FILE} ;;
        "turbo" )
            ./ctrl_aircleaner.sh on
            sleep 10
            ./ctrl_aircleaner.sh turbo
            echo "[**STARTUP-AIR-CLEANER-TURBO**]" TIME=${NOW} MODE=${TRIGGER_MODE} >> ${LOG_FILE} ;;
        "auto_off" )
            ./ctrl_aircleaner.sh auto_off
            echo "[**ENABLE AUTO-OFF-TIMER**]" TIME=${NOW} MODE=${TRIGGER_MODE} >> ${LOG_FILE} ;;
    esac
fi

#Logging
echo "[CHECK]" TIME=${NOW}, HOLIDAY=${HOLIDAY}, STARTUP_TIME=${STARTUP_TIME}, TURN_ON_FLAG=${TURN_ON_FLAG}  >> ${LOG_FILE}