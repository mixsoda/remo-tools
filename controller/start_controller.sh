#!/bin/bash
CDIR=`dirname ${0}`
cd ${CDIR}/

LOG_FILE=logs/log_`date +"%Y%m%d"`.txt
LOG_ERR_FILE=logs/log_err.txt
/home/pi/berryconda3/bin/python ctrl_main.py  >> ${LOG_FILE}  2>> ${LOG_ERR_FILE}
