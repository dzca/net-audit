net-audit
=========

python application for auditing internet access in a Local Network (LAN)

### software environment
- Ubuntu Linux
- Python 2.7

### contents
- doc documents for install justniffer agent
- design key design decisions



############################################################################
#
# Components
#
############################################################################
da -- [data achive]: directory to store history files, split by year->month->day
dl -- [data loader]: raw log data write into this directory and rotated into $number.gz files by log rotator.
dp -- [data parser]: parse the gz files and write into mongodb
lm -- [log monitor]: manage zip files


############################################################################
#
# System work flow (ubuntu)
# []- process
# {}- files
############################################################################
[1] raw log file [squid]-> [syslog-ng]-> {raw directory: /opt/esm/dl/inbox/squid/audit.log}
[2] {raw directory} -> [crontab+logrotate+script] ->
        { move *gz files into inbox(/opt/esm/dp/inbox/squid/) }
        { move *gz files into inbox(/opt/esm/da/squid/$rotate_time) }
[3] {*.gz in dp/inbox/squid/} -> [crontab call] -> LogMonitor -> File Parser -> database

FileMonitor process flow
[] each time a rotate.sh get called, a timstamped folder
    will be created, and .gz files will be stored there. as 1.gz, 2.gz
[] list tomstamped folders under  dp inbox/$device/,
    process form the earliest one
[] check if *.gz file exisiting in the folder, if not, del the folder
[] if yes, unzip file, parse file, and insert the data into db
[] remove the processed folder, go to the next one

############################################################################
#
# networking (ubuntu)
#
############################################################################

[Gatewway]               +-------[pfsense]---------+               [syslog-ng/PC]
192.168.1.1              |                         |                     |
     +               em0:(WAN:DHCP)              em1:(LAN)              eht0
     +-------------- 192.168.1.114              10.30.13.1 -----------10.30.13.11

############################################################################
#
# syslog-ng (ubuntu)
#
############################################################################
[1]dpkg -s syslog-ng
[2]/etc/init.d/syslog-ng {start|stop|restart|reload|force-reload}
[3]config file: /etc/syslog-ng/syslog-ng.conf
@version: 3.2

options { chain_hostnames(off); flush_lines(0); use_dns(no); use_fqdn(no);
          owner("root"); group("adm"); perm(0640); stats_freq(0);
          bad_hostname("^gconfd$");
};
# local source
#source s_src { unix-dgram("/dev/log"); internal();
#             file("/proc/kmsg" program_override("kernel"));
#};

source s_net { udp(); };

filter f_web_access { host("10.30.13.1"); };
destination df_web_access { file("/opt/esm/dl/raw/www/access.log"); };
log { source(s_net); filter(f_web_access);destination(df_web_access); };

############################################################################
#
# squid (pfsense)
#
############################################################################
erase the cache
sqiud -k shutdown
/usr/local/sbin/squid -z

custom config:
access_log udp://10.30.13.11:514
file format: [1]epico time sec, [2]client IP, [3]access method, [5]URL

logformat minimal %ts %>a %rm %ru
access_log udp://10.30.13.11:514 minimal

############################################################################
#
# log rotate
#
############################################################################
log rotate is started by cron tab
[1]start crontab service
#/etc/init.d/cron start

[2]rotate.sh
#!/bin/bash
ROTATE_CONFIG=$1

/usr/sbin/logrotate -s logstatus $ROTATE_CONFIG

EXITVALUE=$?
if [ $EXITVALUE != 0 ]; then
    /usr/bin/logger -t logrotate "ALERT exited abnormally with [$EXITVALUE]"
fi
exit 0

[3] /opt/esm/conf/rotate.conf
/opt/esm/dl/raw/www/www.log {
        size 10k
        copytruncate
        create 700 root root
        rotate 10
        postrotate
                /etc/init.d/syslog-ng reload > /dev/null 2>&1 || true
                endscript
        compress
}

[4]/etc/crontab
#rotate file every 30 minutes
*/1 * * * * root ./rotate.sh /opt/esm/conf/rotate.conf

logrotate.sh code
############################################################
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
DEVICES=("www")

for device in "${DEVICES[@]}"
do
	######### rotate log files ########
	/usr/sbin/logrotate -s logstatus $SERVER_ROOT/conf/$device-rotate.conf
	EXITVALUE=$?
	if [ $EXITVALUE != 0 ]; then
	    /usr/bin/logger -t logrotate "ALERT: rotate $device log exited abnormally with [$EXITVALUE]"
	fi

	######### move log file to dp and da ########
    #echo "testing $SFM_ROOT/dl/inbox/$device/"
    count=`ls -1 $SFM_ROOT/dl/inbox/$device/*.gz 2>/dev/null | wc -l`
    if [ $count != 0 ]
    then
        rotate_time=$(date +'%Y%m%d%H%M%S')
        mkdir -p $SERVER_ROOT/dp/inbox/$device/$rotate_time
        mkdir -p $SERVER_ROOT/da/$device/$rotate_time
        cp $SERVER_ROOT/dl/inbox/$device/*.gz $SERVER_ROOT/dp/inbox/$device/$rotate_time/
        # move to archive folder
        mv $SERVER_ROOT/dl/inbox/$device/*.gz $SERVER_ROOT/da/$device/$rotate_time/
    fi
done

exit 0
############################################################
run every n minutes
echo "* */$n * * * root cd $SERVER_ROOT/bin;./rotate.sh justniffer&" >> /etc/crontab
