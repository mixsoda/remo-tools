#!/bin/bash
#
CDIR=`dirname ${0}`
cd ${CDIR}/

curl -s -X GET https://holidays-jp.github.io/api/v1/date.json > ../controller/conf/holiday.json