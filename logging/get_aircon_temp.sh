#!/bin/bash
CDIR=`dirname ${0}`
FILE=${CDIR}"/logs/aircon_state.txt"
echo `tail -n 1 ${FILE} | cut -d',' -f 4`