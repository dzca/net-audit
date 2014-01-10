#!/usr/bin/python

import logging.config
import yaml

class Logger:
    '''Configuration file Loader'''
    
    def __init__(self):
        #File config
        #logging.config.fileConfig('/opt/esm/etc/logging.conf')
        log_config = yaml.load(open('/opt/esm/etc/logging.yaml', 'r'))
        log_config.setdefault('version', 1)
        logging.config.dictConfig(log_config)
        
    def getLogger(self, name):
        return logging.getLogger(name)

def test():
    logger = Logger().getLogger("Logger test")
    logger.debug("1")
    logger.info("2")
    logger.warn("3")
    logger.error("4")
    logger.critical("5")
    
if __name__ == "__main__":test()
