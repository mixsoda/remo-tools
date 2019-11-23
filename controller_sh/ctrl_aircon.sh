#!/bin/bash

# useage ::
# ctrl_aircon (on|off) mode [temp]
# mode (c|w)
# temp temperature

TOKEN=`cat ../token.txt`
APPLIANCE_ID=`cat ../aircon_id.txt`

MODE_NAME=""
TEMPSTR=""

case $1 in
    "off"  ) POWER="button=power-off" ;;
    "on"  ) POWER="button=" ;;
    * )    exit ;;
esac  

if [ $# -eq 3 ]; then 
    case $2 in
        "cool" | "c" ) MODE_NAME="operation_mode=cool&" ;;
        "warm" | "w"  ) MODE_NAME="operation_mode=warm&" ;;
        * )    exit ;;
    esac
fi


if [ $# -eq 3 ]; then 
    TEMPSTR="=${3}&"
fi

echo "command :: ${MODE_NAME}${TEMPSTR}${POWER}"

#get remo sensor datadevices
result=`curl -s -X POST "https://api.nature.global/1/appliances/${APPLIANCE_ID}/aircon_settings" -d "${MODE_NAME}${TEMPSTR}${POWER}" -k -H "Authorization: Bearer ${TOKEN}"`

echo ${result}