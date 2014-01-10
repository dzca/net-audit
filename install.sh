#/bin/bash

#################################################################
# Install the directories for Server (esm) 
#################################################################
SERVER_NAME=esm
SERVER_ROOT=/opt/$SERVER_NAME
ROTATE_EVERY_MIN=3

DEVICES=("justniffer")
SERVICES=("dl" "dp" "da")

##################################################################
# utility functions begine
##################################################################

_make_dir()
{
    directory=$1
    if [ ! -d $directory ]
    then
        echo "making $directory"
        mkdir -p $directory
    fi
}

_mv_file()
{
	file=$1
	directory=$2
	
	pushd $directory > /dev/null
	if [ ! -e "$file.bak" ]
	then
		mv $file $file.bak
	fi
	popd > /dev/null
	mv conf/$file $directory/
}

##################################################################
# utility functions end
##################################################################

#initialize system directories
for service in "${SERVICES[@]}"
do
    echo "create directory for $service..."
    _make_dir "$SERVER_ROOT/$service/inbox/"
    for device in "${DEVICES[@]}"
    do
        _make_dir "$SERVER_ROOT/$service/inbox/$device"
    done
done

_make_dir $SERVER_ROOT/etc
_make_dir $SERVER_ROOT/bin
_make_dir $SERVER_ROOT/py
_make_dir $SERVER_ROOT/logs

cp -v uninstall.sh $SERVER_ROOT/

# copy configurations
cp -v etc/*.conf $SERVER_ROOT/etc/
cp -v etc/*.yaml $SERVER_ROOT/etc/
cp -v etc/*.ini $SERVER_ROOT/etc/
cp -R -v src/* $SERVER_ROOT/py/
chmod -R +x $SERVER_ROOT/py

cp -v bash/rotate.sh $SERVER_ROOT/bin/
cp -v bash/esmdp.sh $SERVER_ROOT/bin/
#cp -v bash/test.sh $SERVER_ROOT/bin/
chmod -R +x $SERVER_ROOT/bin

ip_address=$(ifconfig | grep "inet addr:" | grep -v 127.0.0.1 | sed -e 's/inet addr://g' | awk '{print $1}')
sed -i "s/%%IP_ADDRESS%%/$ip_address/g" $SERVER_ROOT/etc/http.ini

##################################################################
# update the config files for services
##################################################################
cp bash/python.sh /etc/profile.d/
chmod +x /etc/profile.d/python.sh
source /etc/profile.d/python.sh

# copy init.d daemons
cp -v etc/nifferd /etc/init.d/
chmod o+x /etc/init.d/nifferd
update-rc.d nifferd defaults
service nifferd start

cp -v etc/reportd /etc/init.d/
chmod o+x /etc/init.d/reportd
update-rc.d reportd defaults
service reportd start

#mongoimport -d esm -c users --file etc/esm_users.json

##################################################################
# setup logrotate in crontab
# run every 30 minutes:
# 0,30 * * * * root /opt/esm/bin/rotate.sh
##################################################################
echo "*/$ROTATE_EVERY_MIN * * * * root /opt/esm/bin/rotate.sh justniffer" >> /etc/crontab
echo "*/$ROTATE_EVERY_MIN * * * * root /opt/esm/bin/esmdp.sh" >> /etc/crontab
#echo "*/$ROTATE_EVERY_MIN * * * * root /opt/esm/bin/test.sh" >> /etc/crontab
