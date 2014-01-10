#!/bin/bash

CUR_DIR=`pwd`

TEST_DIR_BASE=$CUR_DIR/../
JUSTNIFFER_JSON=$TEST_DIR_BASE/samples/justniffer/esm_events.json

#echo $JUSTNIFFER_JSON
mongoimport -d esm -c events --file $JUSTNIFFER_JSON