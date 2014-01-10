#!/bin/bash

source /etc/profile.d/python.sh

pushd /opt/esm/py > /dev/null
	./dp/file_monitor.py 'justniffer'
popd > /dev/null	