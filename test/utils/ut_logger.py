#!/usr/bin/python

import unittest
from utils.logger import Logger

class UtLogger(unittest.TestCase):
    
    def setUp(self):
        self.logger = Logger().getLogger("test.utils.UtLogger")
        
    def testLogger(self):
        self.logger.debug("1")
        self.logger.info("2")
        self.logger.warn("3")
        self.logger.error("4")
        self.logger.critical("5")
        
if __name__ == '__main__': unittest.main()