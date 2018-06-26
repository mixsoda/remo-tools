#!/bin/bash
CDIR=`dirname ${0}`
cd ${CDIR}/

TOKEN=`cat ../token.txt`
NOW=`date +"%Y-%m-%dT%T"`

#get remo sensor data
curl -s -X GET "https://api.nature.global/1/devices" -H "accept: application/json" --header "Authorization: Bearer ${TOKEN}" > logs/out_rawdata.json

#get number of sensor data
sensor_num=`../lib/parsrj.sh logs/out_rawdata.json | grep "newest_events" | wc -l`
sensor_num=`expr ${sensor_num} / 2`

#get firmware_version
firm_var=`../lib/parsrj.sh logs/out_rawdata.json | grep "firmware_version" | cut -d" " -f2`
firm_date=`../lib/parsrj.sh logs/out_rawdata.json | grep "0].updated_at" | cut -d" " -f2` 

#perse sensor data using parsrj.sh
#https://github.com/ShellShoccar-jpn/Parsrs
hu_value=`../lib/parsrj.sh logs/out_rawdata.json | grep "newest_events.hu.val" | cut -d" " -f2`
hu_updated=`../lib/parsrj.sh logs/out_rawdata.json | grep "newest_events.hu.created_at" | cut -d" " -f2`
il_value=`../lib/parsrj.sh logs/out_rawdata.json | grep "newest_events.il.val" | cut -d" " -f2`
il_updated=`../lib/parsrj.sh logs/out_rawdata.json | grep "newest_events.il.created_at" | cut -d" " -f2`
temp_value=`../lib/parsrj.sh logs/out_rawdata.json | grep "newest_events.te.val" | cut -d" " -f2`
temp_updated=`../lib/parsrj.sh logs/out_rawdata.json | grep "newest_events.te.created_at" | cut -d" " -f2`

#check state of air-con
AIRCON_POWER=`../utils/get_aircon_settings.sh button`
if [ ${AIRCON_POWER} = "power-off" ]; then 
    AIRCON_POWER="OFF"
    AIRCON_MODE="NaN"
    AIRCON_TEMP="NaN"
else
    AIRCON_POWER="ON"
    AIRCON_MODE=`../utils/get_aircon_settings.sh mode`
    AIRCON_TEMP=`../utils/get_aircon_settings.sh temp`
fi

#output csv
echo "$il_updated, $il_value" >> logs/il.txt
echo "$hu_updated, $hu_value" >> logs/hu.txt
echo "$temp_updated, $temp_value" >> logs/temp.txt

echo "$firm_date, $firm_var" >> logs/firmware.txt
echo "$NOW, $sensor_num" >> logs/sensor_num.txt

echo "$NOW, ${AIRCON_POWER}, ${AIRCON_MODE}, ${AIRCON_TEMP}" >> logs/aircon_state.txt
