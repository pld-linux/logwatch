#!/bin/sh
#########
#---{ Initial values: }---#
SERVICE_RUN_NICE_LEVEL="0"
OUTPUT="unformated"
DATE=`/bin/date +%F`

#---{ Fetch configuration: }---#
if [ -f /etc/sysconfig/logwatch ]; then
	. /etc/sysconfig/logwatch
fi

#---{ main part }---#
if [ "${OUTPUT_LOCATION}" ]; then
	umask 0022
	nice -n ${SERVICE_RUN_NICE_LEVEL} /usr/sbin/logwatch --output=${OUTPUT} --save="${OUTPUT_LOCATION}/${DATE}.html"
else
	nice -n ${SERVICE_RUN_NICE_LEVEL} /usr/sbin/logwatch --output=${OUTPUT}
fi
