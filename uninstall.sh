#/bin/bash

#################################################################
# Uninstall the directories for Server
#################################################################
SERVICES=("reportd" "nifferd")

#clean crontab
sed -i '/esmdp\.sh/d' /etc/crontab
#sed -i '/test\.sh/d' /etc/crontab
sed -i '/justniffer/d' /etc/crontab

#unistall init.d
for svc in "${SERVICES[@]}"
do
	echo "removing $svc"
	service $svc stop
	update-rc.d -f $svc remove
	rm -f /etc/init.d/$svc
done

cd /opt
rm -fr /opt/esm