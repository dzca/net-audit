#!/bin/bash
#######################################################################
#
# This script will package the server application
#
#######################################################################
SERVER_NAME=esm
DIST_DIR=dist
if [ -d "dist" ]
then
	rm -fr dist
fi

mkdir -p dist

################################################################################
# tar package.
################################################################################
time_stamp=`date +"%Y_%m_%d_%H_%M_%S"`
# make package
patch_name=$SERVER_NAME-`date +"%Y_%m_%d_%H_%M_%S"`.tbz
echo "patch_name: $patch_name"
tar jcvf $DIST_DIR/${patch_name} * --exclude "doc" --exclude "test" --exclude ".svn" --exclude "dist" --exclude "make.sh" --exclude "*.old" --exclude "*.pyc" --exclude "design"
md5sum $DIST_DIR/${patch_name} > $DIST_DIR/${patch_name}.md5
