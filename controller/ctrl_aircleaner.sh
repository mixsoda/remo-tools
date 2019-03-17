#!/bin/bash

# useage ::
# ctrl_aircleaner (on|off|turbo)

TOKEN=`cat ../token.txt`
SIGNAL_ID_LIST='../aircleaner_id.txt'

while read signal_str; do
    #skip comment line
    if [ `echo ${signal_str} | cut -c 1` = "#" ]; then
        #echo "comment"
        continue
    fi

    #parse config
    SIGNAL_TYPE=`echo ${signal_str} | cut -d',' -f 1`
    SIGNAL_ID=`echo ${signal_str} | cut -d',' -f 2 | tr -d '\r'`

    if [ $1 = ${SIGNAL_TYPE} ]; then 
        break
    fi
done < ${SIGNAL_ID_LIST}


echo "SIGNAL_TYPE=${SIGNAL_TYPE}; SIGNAL_ID=${SIGNAL_ID}"

#send signal
result=`curl -s -X POST "https://api.nature.global/1/signals/${SIGNAL_ID}/send" -k -H "Authorization: Bearer ${TOKEN}" -o /dev/null -w '%{http_code}'`

echo "RESULT=${result}"