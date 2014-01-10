#!/bin/bash
##########################################################################################
#
# Script called by crontab to rotate log files
# Devices:
#		www -- Internet proxy access logs 
#
# runtime logic
#[1] raw log file [squid]-> [syslog-ng]-> {raw directory: /opt/esm/dl/inbox/www/www.log} 
#[2] {raw directory} -> [crontab+logrotate+script] -> 
#        { move *gz files into inbox(/opt/esm/dp/inbox/www/) }
#        { move *gz files into inbox(/opt/esm/da/www/$rotate_time) }
##########################################################################################
SERVER_NAME=esm
SERVER_ROOT=/opt/$SERVER_NAME
DEVICES=("justniffer")

for device in "${DEVICES[@]}"
do
	######### rotate log files ########
	/usr/sbin/logrotate -s logstatus $SERVER_ROOT/etc/$device-rotate.conf
	EXITVALUE=$?
	if [ $EXITVALUE != 0 ]; then
	    /usr/bin/logger -t logrotate "ALERT: rotate $device log exited abnormally with [$EXITVALUE]"
	fi
	
	######### move log file to dp and da ########
    #echo "testing $SFM_ROOT/dl/inbox/$device/"
    count=`ls -1 $SERVER_ROOT/dl/inbox/$device/*.gz 2>/dev/null | wc -l`
    if [ $count != 0 ]
    then
        rotate_time=$(date +'%Y%m%d%H%M%S')
        mkdir -p $SERVER_ROOT/dp/inbox/$device/$rotate_time
        mkdir -p $SERVER_ROOT/da/inbox/$device/$rotate_time
        cp $SERVER_ROOT/dl/inbox/$device/*.gz $SERVER_ROOT/dp/inbox/$device/$rotate_time/
        # move to archive folder 
        mv $SERVER_ROOT/dl/inbox/$device/*.gz $SERVER_ROOT/da/inbox/$device/$rotate_time/
    fi
done

exit 0
