#!/bin/bash
CDIR=`dirname ${0}`
FILE=${CDIR}"/logs/temp.txt"
echo `tail -n 1 ${FILE} | cut -d' ' -f 2`