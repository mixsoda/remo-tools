#!/bin/bash
CDIR=`dirname ${0}`
cd ${CDIR}/

TOKEN=`cat ../token.txt`
TARGET_AIRCON_ID=`cat ../aircon_id.txt`

#get remo sensor datadevices
curl -s -X GET "https://api.nature.global/1/appliances" -H "accept: application/json" --header "Authorization: Bearer ${TOKEN}" > result_models.json

#get aircon index
aircon_index=`../lib/parsrj.sh result_models.json  | grep ${TARGET_AIRCON_ID} | awk 'match($0, /\$\[[0-9]\]/) { print substr($0,RSTART,RLENGTH) }'`

#output setting
key="${aircon_index}.settings.${1}"

echo `../lib/parsrj.sh result_models.json  | grep -F ${key} | cut -d" " -f 2`