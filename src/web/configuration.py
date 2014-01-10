#!/usr/bin/python
import ConfigParser

class Configuration:
    def __init__(self, size, count, page):
        self.config = ConfigParser.ConfigParser()
        self.config.read('/opt/esm/etc/http.ini')

    def user(self):
        return self.config.get('access', 'admin')
    
    def passwd(self):
        return self.config.get('access', 'password')