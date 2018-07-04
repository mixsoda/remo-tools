#!/bin/bash
CDIR=`dirname ${0}`
cd ${CDIR}/

TOKEN=`cat ../token.txt`
TARGET_AIRCON_ID=`cat ../aircon_id.txt`
CONF_FILE='ctrl_config.txt'
LOG_FILE=logs/log_`date +"%Y%m%d"`.txt

NOW=`date +"%Y-%m-%dT%T"`
NOW_DATE=`date +"%Y-%m-%d"`
NOW_UNIXTIME=`date +%s`

RETRY_TIME=615 #sec
STARTUP_TIME=0
REQUIRE_MODE="OFF"

#check today is holiday(sat,sun,national holiday) or not
TODAY=`date +"%Y-%m-%d"`
DOW=`date +"%w"`
JPHOLIDAY=`cat ../holiday.json | grep ${TODAY} | wc -l`
HOLIDAY=0

if [ ${DOW} -eq 0 -o ${DOW} -eq 6 -o ${JPHOLIDAY} -eq 1 ]; then 
    HOLIDAY=1
fi

#check room enviroment
RTEMP=`../logging/get_temp.sh  | cut -d'.' -f 1`
RHU=`../logging/get_hu.sh`
RIL=`../logging/get_il.sh  | cut -d'.' -f 1`

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
    TRIGGER_TEMP=`echo ${conf_str} | cut -d',' -f 4 | sed -e 's/C$//g' | sed 's/^[ \t]*//'`
    REQUEST_RUNMODE=`echo ${conf_str} | cut -d',' -f 5 | cut -d'-' -f 1 | sed 's/^[ \t]*//'`
    REQUEST_RUNTEMP=`echo ${conf_str} | cut -d',' -f 5 | cut -d'-' -f 2 | sed -e 's/C$//g'  | sed 's/^[ \t]*//'`

    case "${TRIGGER_DAY_TYPE}" in
        "WEEK_DAY" )  TRIGGER_DAY_TYPE=0 ;;
        "HOLIDAY" ) TRIGGER_DAY_TYPE=1 ;;
        * ) echo "[READ_CONF_ERROR]" TIME=${NOW}, TRIGGER_DAY_TYPE=${TRIGGER_DAY_TYPE}  >> ${LOG_FILE}
            exit ;;
    esac
    
    #check time trigger
    STARTUP_UNIXTIME=`date +%s --date "${NOW_DATE} ${TRIGGER_HOUR}:${TRIGGER_MIN}"`
    if [ ${NOW_UNIXTIME} -ge ${STARTUP_UNIXTIME} ] && [ ${NOW_UNIXTIME} -le `expr ${STARTUP_UNIXTIME} + ${RETRY_TIME}` ]; then
        STARTUP_TIME=1
    fi

    #check temp trigger
    if [ ${REQUEST_RUNMODE} = "COOLER" ] && [ ${RTEMP} -ge ${TRIGGER_TEMP} ]; then 
        REQUIRE_MODE="COOLER"
    fi
    if [ ${REQUEST_RUNMODE} = "WARMER" ] && [ ${RTEMP} -le ${TRIGGER_TEMP} ]; then 
        REQUIRE_MODE="WARMER"
    fi

    #Logging
    #echo "[DEBUG_TRIGGER]" DAY_TYPE=${TRIGGER_DAY_TYPE}, HOUR=${TRIGGER_HOUR}, MIN=${TRIGGER_MIN}, TEMP=${TRIGGER_TEMP}, RUNMODE=${REQUEST_RUNMODE}, RUNTEMP=${REQUEST_RUNTEMP} >> ${LOG_FILE}

    #check signal send conditions (date, time, temp)
    if [ ${HOLIDAY} -ne ${TRIGGER_DAY_TYPE} ] || [ ${STARTUP_TIME} -eq 0 ] || [ ${REQUIRE_MODE} = "OFF" ] ; then 
        continue
    fi

    #check state of air-con
    AIRCON_POWER=`./get_aircon_settings.sh button`
    if [ ${AIRCON_POWER} = "power-off" ]; then 
        AIRCON_POWER="OFF"
    else
        AIRCON_POWER="ON"
        AIRCON_MODE=`./get_aircon_settings.sh mode`
        AIRCON_TEMP=`./get_aircon_settings.sh temp`
    fi

    #send IR-signal
    if [ ${AIRCON_POWER} = "OFF" ]; then 
        if [ ${REQUIRE_MODE} = "COOLER" ]; then
            ./ctrl_aircon.sh on cool ${REQUEST_RUNTEMP}
            echo "[**COOLER-SEND**]" TIME=${NOW}, REQUIRE_MODE=${REQUIRE_MODE} REQUEST_RUNTEMP=${REQUEST_RUNTEMP} >> ${LOG_FILE}
            exit
        else
            #./ctrl_aircon.sh on warm ${REQUEST_RUNTEMP}
            echo "[**WARMER-SEND**]" TIME=${NOW}, REQUIRE_MODE=${REQUIRE_MODE} REQUEST_RUNTEMP=${REQUEST_RUNTEMP} >> ${LOG_FILE}
            #exit
        fi
    else
        if [ ${AIRCON_MODE} = ${REQUIRE_MODE} ] && [ ${AIRCON_TEMP} = ${REQUEST_RUNTEMP} ] ; then
            echo "[ALREADY_RUN_REQUIRE_SETTING]" TIME=${NOW}, RUN_MODE=${AIRCON_MODE}, AIRCON_TEMP=${AIRCON_TEMP} >> ${LOG_FILE}
        else
            if [ ${REQUIRE_MODE} = "COOLER" ]; then
                ./ctrl_aircon.sh on cool ${REQUEST_RUNTEMP}
                echo "[**COOLER-TEMP-CHANGE**]" TIME=${NOW}, RUN_MODE=${AIRCON_MODE}, AIRCON_TEMP=${AIRCON_TEMP} >> ${LOG_FILE}
                exit
            else
                #./ctrl_aircon.sh on warm ${REQUEST_RUNTEMP}
                echo "[**WARMER-TEMP-CHANGE**]" TIME=${NOW}, RUN_MODE=${AIRCON_MODE}, AIRCON_TEMP=${AIRCON_TEMP} >> ${LOG_FILE}
                #exit
            fi
        fi
    fi
done < ${CONF_FILE}

#Logging
echo "[CHECK]" TIME=${NOW}, HOLIDAY=${HOLIDAY}, RT=${RTEMP}, RH=${RHU}, RIL=${RIL}, STARTUP_TIME=${STARTUP_TIME}, REQUIRE_MODE=${REQUIRE_MODE} >> ${LOG_FILE}