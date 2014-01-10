#!/usr/bin/python

import unittest, ConfigParser, os

class UtConfig(unittest.TestCase):
    '''complex query test driver'''
    
    config = ConfigParser.ConfigParser()

    def setUp(self):
        test_root_path = os.getcwd() + '/..'
        config_path = test_root_path + '/../etc/http.ini'
        self.config.read(config_path)
    
    def testGetIp(self):
        ip = self.config.get('network', 'ip')
        self.assertEqual(ip, '%%IP_ADDRESS%%')