#!/usr/bin/python

##################################################################
# monitor dp inbox folder for new zipped log file, 
# call ParserFactory for create Parsers.
# Parser instance will load the log data into database 
##################################################################

# [] each time a rotate.sh get called, a timstamped folder 
#    will be created, and .gz files will be stored there. as 1.gz, 2.gz
# [] list tomstamped folders under  dp inbox/$device/, 
#    process form the earliest one
# [] check if *.gz file exisiting in the folder, if not, del the folder
# [] if yes, unzip file, parse file, and insert the data into db
# [] remove the processed folder, go to the next one


import os,glob,sys

from dp.parser_factory import ParserFactory
from utils.logger import Logger
from datetime import datetime

class FileMonitor:
    
    logger = Logger().getLogger("dp.FileMonitor")
        
    def __init__(self, device_name):
        "One monitor instance monitor one specified devices"
        self.parser = ParserFactory.createParser(device_name)
        self.inbox_path = ParserFactory.getInboxPath(device_name)
        self.device_name = device_name
        
        #start log current time in debugger
        current_time = datetime.time(datetime.now())
        current_time_string = current_time.strftime('%Y/%m/%d %H:%M:%S')
        self.logger.info('Starting File Monitor [' + device_name + '] at ' + current_time_string)
        
    def getParser(self):
        return self.parser    
    
    def setInboxPath(self, path):
        ''' method for testing use '''
        self.inbox_path = path
        
    def processInbox(self):
        '''process sub directory under inbox , scan directories in ascend order, 
        unzip the *.gz log file, parse it and insert into db, remove the empty directory
        '''
        
        # sort time stamped folder
        sorted_directories = self.sortSubDirectories()
        for directory_name in sorted_directories:
            self.logger.info('Processing sub folder ' + directory_name + ' under inbox/ ' + self.device_name)
            timestamped_dir_path = os.path.join(self.inbox_path, directory_name)
            if FileMonitor.HasZipFile(timestamped_dir_path):
                self.logger.debug(directory_name + ' is not empty')
                self.parseZippedFiles(timestamped_dir_path)
            else:
                self.logger.debug(directory_name + ' is empty')
                self.logger.info('deleting folder ' + directory_name)
                FileMonitor.DelDirectory(timestamped_dir_path)
                
    def parseZippedFiles(self,directory):
        sorted_files = FileMonitor.SortFiles(directory)
        for fileName in sorted_files:
            filePath = os.path.join(directory, fileName)
            self.logger.info('Processing zipped log ' + filePath)
            self.parser.processZippedFile(filePath)
        FileMonitor.DelDirectory(directory)
    
    ###########################################################################
    # Unit Testable methods below
    ###########################################################################

    def sortSubDirectories(self):
        '''Return a list of directories by ascend order,(start form the smallest
        number)'''

        self.logger.debug('Sorting directory ' + self.inbox_path)
        file_list = []
        for file_name in os.listdir(self.inbox_path):
            if os.path.isdir(os.path.join(self.inbox_path, file_name)):
                file_list.append(file_name)

        file_list.sort()
        return file_list
    
    @staticmethod
    def SortFiles(directory):
        '''Return a list of files sorted in Descend order'''
        
        zip_file_list = []
        # file_list = glob.iglob(os.path.join(directory, "*.gz"))
        for fileName in os.listdir(directory):
            #if os.path.isfile(file):
            zip_file_list.append(fileName)
                
        zip_file_list.sort()
        zip_file_list.reverse()
        return zip_file_list
    
    @staticmethod
    def HasZipFile(directory):
        '''Return true if the oldest directory contains a type of files,
        e.g. type=gz will check *.gz'''
        
        zip_file_list = glob.glob(os.path.join(directory, "*.gz"))
        # print "zip_file_list = " + str(len(zip_file_list))
        return (len(zip_file_list) != 0 )
    
    @staticmethod
    def DelDirectory(path):
        "delete a directory under the monitored directory"
        
        if os.path.exists(path):
            os.rmdir(path)
            
def run(device_name):
    file_monitor = FileMonitor(device_name)
    parser = file_monitor.getParser()
#    print dir(parser)
#    print parser.getDeviceName()
    file_monitor.processInbox()

if __name__ == '__main__':
    device_name = sys.argv[1]
    run(device_name)