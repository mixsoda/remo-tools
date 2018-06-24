#!/bin/bash
CDIR=`dirname ${0}`
FILE=${CDIR}"/logs/il.txt"
echo `tail -n 1 ${FILE} | cut -d' ' -f 2`