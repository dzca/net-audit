#!/usr/bin/python

import gzip, os
from datetime import datetime

class Parser:
    '''File monitor call parser.parse to handle files'''
    
    device_map={'justniffer':1,
                'squid':2
    }
    
    def getParserName(self):
        return self.parser_name
    
    def getDeviceName(self):
        return self.device_name
    
    def unzip(self, file_path):
        "Unzip the zipped log file, return list of lines"
        
        # print "unzip file " + self.filePath
        f = gzip.open(file_path, 'rb')
        file_content = f.readlines()
        f.close()
        return file_content
    
    def processZippedFile(self,filePath):
        '''Process zipped file and remove it'''
        
        self.logger.debug("processing zipped file " + filePath)
        # unzip the file and return list of lines
        log_lines = self.unzip(filePath)        
        # parse file
        self.parse(log_lines)        
        #remove parsed file
        if os.path.isfile(filePath):
            os.unlink (filePath)
            
    def parseTime(self, epoch_time_str):
        #print epoch_time_str
        epoch_time = float(epoch_time_str)
        return datetime.fromtimestamp(epoch_time)
    
    def validateLine(self,line_to_validate):
        ''' a valid line must started from a epoch time(digits)'''
        stripped_line = line_to_validate.strip()
        if not stripped_line[0].isdigit():
            self.logger.debug("Encountered invalidate line:"+ stripped_line)
            return None
        else:
            return stripped_line