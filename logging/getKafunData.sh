#!/bin/bash
CDIR=`dirname ${0}`
cd ${CDIR}/

#URL::Aichi environmental research center
TARGET_URL='http://kafun.taiki.go.jp/mobile/Data[52310100].html'

#file name setting (input)
ORIGINAL_FILE_NAME='kafun_raw_temp.txt'
TODAY_DATA_ONLY_FILE_NAME='kafun_data_temp.txt'

#file name setting (output)
LOG_FILE='logs/kafun.txt'
FLAG_FILE='logs/kafun_alert.txt'

#variable
NOW=`date +"%Y-%m-%dT%T"`
NOWDAY=`date +"%Y-%m-%d"`
KAFUN_FLAG='0'

############

#get kafun raw data
curl -s --globoff ${TARGET_URL} > ${ORIGINAL_FILE_NAME}
sleep 5

#create current kafun data file (temp)
cat ${ORIGINAL_FILE_NAME} | head -n 14 | tail -n 1 > ${TODAY_DATA_ONLY_FILE_NAME}

#calc file size
FILESIZE=`ls -l | grep ${TODAY_DATA_ONLY_FILE_NAME} | sed -e "s/  */ /g" | cut -d' ' -f 5`

#get kafun data (24=0-9, 25=10-99, 26=100-999, 27=1000-9999)
case "${FILESIZE}" in
        "24" )  AMOUNT_KAFUN=`cut -b 13 ${TODAY_DATA_ONLY_FILE_NAME}` ;;
        "25" )  AMOUNT_KAFUN=`cut -b 13-14 ${TODAY_DATA_ONLY_FILE_NAME}` ;;
        "26" )  AMOUNT_KAFUN=`cut -b 13-15 ${TODAY_DATA_ONLY_FILE_NAME}` 
                KAFUN_FLAG='1' ;;
        "27" )  AMOUNT_KAFUN=`cut -b 13-16 ${TODAY_DATA_ONLY_FILE_NAME}`
                KAFUN_FLAG='1' ;;
        * ) AMOUNT_KAFUN='0' ;;
esac

echo ${NOW}, ${AMOUNT_KAFUN} >> ${LOG_FILE}

LAST_ALERT=''
LAST_ALERT=`cat ${FLAG_FILE} | tail -n 1 | grep ${NOWDAY} | cut -d'-' -f1 | wc -c`
if [ ${KAFUN_FLAG} = '1' ] && [ ${LAST_ALERT} -eq 0 ]; then 
        echo ${NOWDAY} >> ${FLAG_FILE}
fi