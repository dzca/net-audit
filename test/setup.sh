#!/bin/bash

scp dustin@10.30.13.11:/opt/dev/projects/net-audit/dist/*.tbz ~/test/
#scp dustin@192.168.153.171:/opt/dev/projects/net-audit/dist/*.tbz ~/test/

pushd ~/test
tar xf *.tbz 
chmod -R +x *
./install.sh
popd
