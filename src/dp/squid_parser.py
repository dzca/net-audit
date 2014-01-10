#!/usr/bin/python

#from db.mongodb import MongoDB
from dp.parser import Parser
from urlparse import urlparse
from utils.logger import Logger

class SquidParser(Parser):
    ''' Parse access log for Squid Proxy Server'''
    logger = Logger().getLogger("dp.SquidParser")
        
    def __init_(self):
        print 'init'
#        self.deviceName('squid')
#        self.parser_name='SquidParser'
        #fetch metat_data(time,index) by device_name from database
#        event_count_doc = MongoDB.getLastTime(self.device_name)
#        print event_count_doc
#        if event_count_doc is None:
#            self.last_time = None
#            self.index = 0
#        else:
#            self.last_time = event_count_doc['create_time']
#            self.index = event_count_doc['index']
    
    @property
    def device_name(self):
        return 'squid'
    
    @property
    def parser_name(self):
        return 'SquidParser'
    
    def parse(self, log_lines):
        '''Parse log lines and read it into a list of dictionary'''
        
        events_list = []
#        #read the first line to set the self.time_string"
#        event = self.parseLine(log_lines[0])
#        datetime_in_current_line = event['create_time']
#        if self.last_time is None:
#            self.last_time = datetime_in_current_line
#            self.index = 0
#            MongoDB.createLastTime(self.last_time, self.index)
#            
#        for log_line in log_lines:
#            event = self.parseLine(log_line)
#            datetime_in_current_line = event['create_time']
#            if self.last_time == datetime_in_current_line:
#                self.index += 1
#                event['sequence_id'] = self.index
#            else:
#                self.last_time = datetime_in_current_line
#                self.index = 1
#                MongoDB.setLastTime(self.last_time, self.index)
#                event['sequence_id'] = self.index
#                 
#            events_list.append(event)
#        
#        MongoDB.setLastTime(datetime_in_current_line, self.index)
#        
#        # persist to db
#        MongoDB.insertEvents(events_list)
    
    def parseLine(self, line_to_parse):
        '''parse a line of log, return a dictionary of log
        a sample line:
        Nov  9 23:17:46 10.30.13.1 1352521070 10.30.13.11 GET http://www.sunlife.ca/static/slfglobal/styles/globalweb.css
        1352521070 10.30.13.11 GET http://www.sunlife.ca/static/plan/plan_overrideGW.css        
        '''
        event = None
        validated_line = self.validateLine(line_to_parse)
        
        if validated_line is not None:
            # line validateion returns None
            log_item_list = validated_line.split(' ',3)
            create_time = self.parseTime(log_item_list[0].strip())
            raw_url = log_item_list[3].strip()
            domain = self.parseDomain(raw_url)
            event = {'create_time': create_time,
                 'ip': log_item_list[1], 
                 'method':log_item_list[2],
                 'url':raw_url,
                 'domain':domain
                 }
        else:
            self.logger.debug('Invalid line parsed:' + line_to_parse)
        return event
    
    def validateLine(self,line_to_validate):
        ''' a valid line must started from a epoch time(digits)'''
        stripped_line = line_to_validate.strip()
        if not stripped_line[0].isdigit():
            self.logger.debug("Encountered invalidate line:"+ stripped_line)
            return None
        else:
            return stripped_line

        
    def parseDomain(self, url):
        '''parse a http request and return domain'''
        url_parser = urlparse(url)
        return url_parser.hostname
        