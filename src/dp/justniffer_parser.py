#!/usr/bin/python

from db.mongodb import MongoDB
from dp.parser import Parser
from utils.logger import Logger

class JustNifferParser(Parser):
    ''' Parse access log for JustNiffer log file
    The log format is:db = MongoDB('esm')
     %request.timestamp(%s) %source.ip %request.header.host %request.url
    
    request command is:
    justniffer -i eth0 -p "port 80 or port 8080" -l "%request.timestamp(%s) 
    %source.ip %request.header.host %request.url" 2>&1 | 
    tee /opt/esm/dl/inbox/justniffer/audit.log
    '''
    
    logger = Logger().getLogger("dp.JustNifferParser")
    db = MongoDB('esm')
    
#    def __init_(self):
#        self.
    
    @property
    def device_name(self):
        return 'justniffer'
    
    @property
    def parser_name(self):
        return 'JustNifferParser'
    
    @property
    def event_table(self):
        return 'events'
    
    def parse(self, log_lines):
        '''Parse log lines and read it into a list of dictionary'''
        events_list = []

        for log_line in log_lines:
            event = self.parseLine(log_line)
            if event is not None:
                self.logger.debug('parsed event==')
                self.logger.debug(event)
                events_list.append(event)
                
        if len(events_list) > 0:
            self.logger.debug('bulk insert events, count=' + str(len(events_list)))
            self.db.insertBulk(events_list,self.event_table)
        
    def parseLine(self, line_to_parse):
        '''parse a line of log, return a dictionary of log
        a sample line:
        1353070327 10.30.13.11 news.bbcimg.co.uk /view/3_0_6/cream/hi/shared/global.css
        '''
        event = None
        validated_line = self.validateLine(line_to_parse)
        
        if validated_line is not None:
            log_item_list = validated_line.split(' ',4)
            create_time = self.parseTime(log_item_list[0].strip())
            device_id = self.device_map[self.device_name]
            event = {'device_id':device_id,
                 'create_time': create_time,
                 'ip': log_item_list[1].strip(), 
                 'domain':log_item_list[2].strip(),
                 'size':int(log_item_list[3].strip()),
                 'path':log_item_list[4].strip()
            }
        else:
            self.logger.error('Invalid line parsed:' + line_to_parse)
        return event
