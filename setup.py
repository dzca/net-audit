#!/usr/bin/python
from distutils.core import setup

setup(name='Enterprise Security Monitor',
	version='1.0',
	description='ESM modules',
	author='dike.zhang',
	package_dir = {'' : 'src'}, 
    packages = ['db', 'dp','utils','yaml'] 
)
