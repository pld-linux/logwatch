#!/bin/sh
#########
#---{ Initial values: }---#
NICE_LEVEL="0"
OUTPUT="unformated"
DATA=`/bin/date +%F`

#---{ Fetch configuration: }---#
if [ -f /etc/sysconfig/logwatch ]; then
	. /etc/sysconfig/logwatch
fi

#---{ main part }---#
if [ "${OUTPUT_LOCATION}" ]; then
	umask 0022
	nice -n ${NICE_LEVEL} /usr/sbin/logwatch --output=${OUTPUT} --save="${OUTPUT_LOCATION}/${DATA}.html"
else
	nice -n ${NICE_LEVEL} /usr/sbin/logwatch --output=${OUTPUT}
fi

