#!/usr/bin/python

##################################################################
# Factory class to create Parser instance
##################################################################

from dp.squid_parser import SquidParser
from dp.justniffer_parser import JustNifferParser

class ParserFactory:
    parser_map={
             'squid':SquidParser(),
             'justniffer':JustNifferParser()
             }
    
    inbox_map={
               'squid':'/opt/esm/dp/inbox/squid/',
               'justniffer':'/opt/esm/dp/inbox/justniffer/'
               }
    
    @staticmethod
    def createParser(device_name):
        return ParserFactory.parser_map.get(device_name)
    
    @staticmethod
    def getInboxPath(device_name):
        return ParserFactory.inbox_map.get(device_name)
    
def test():
    parser = ParserFactory.createParser('squid')
    print dir(parser)
    print parser.getDeviceName()
    print parser.getParserName()
    print ParserFactory.getInboxPath('squid')
    
if __name__ == '__main__':test()