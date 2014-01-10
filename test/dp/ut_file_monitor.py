#!/usr/bin/python
import unittest
import os,glob,shutil
from dp.file_monitor import FileMonitor
from utils.logger import Logger
from db.mongodb import MongoDB

class UtFileMonitor(unittest.TestCase):
    '''A Unit Test for dp.monitor.Monitor'''

    logger = Logger().getLogger("dp.UtFileMonitor")
    db = MongoDB('esm')
    
    @property
    def device_name(self):
        return 'justniffer'
    
    def setUp(self):
        "Create a list of test files"
#        self.logger.debug("Calling UtFileMonitor.setup()")
        self.test_root_path = os.getcwd() + '/../'
        #create tmp directory
        self.temp_dir = os.path.join(self.test_root_path, "tmp")
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

        self.time_list = ['20120912072912', '20120913072230', '20120912073312']
        
        for fileName in self.time_list:
            path = os.path.join(self.temp_dir, fileName)
            #print "creating directory " + path
            if not os.path.isdir(path):
                os.mkdir(path)
                
        #copy zipped log files
        data_root_dir = os.path.join(self.test_root_path, "data")
        data_dir = os.path.join(data_root_dir, self.device_name)
        
        ziped_log_files = glob.iglob(os.path.join(data_dir, "*.gz"))        
        dest_dir =  os.path.join(self.temp_dir, "20120913072230")
        for fileName in ziped_log_files:
            if os.path.isfile(fileName):
                shutil.copy2(fileName, dest_dir)

    def tearDown(self):
        "Delete the test directories"
        
#        self.logger.debug("Calling UtFileMonitor.tearDown()")
        dest_dir =  os.path.join(self.temp_dir, "20120913072230")
        ziped_log_files = glob.iglob(os.path.join(dest_dir, "*.gz"))
        for fileName in ziped_log_files:
            os.unlink (fileName)

        for fileName in self.time_list:
            path = os.path.join(self.temp_dir, fileName)
            # print "deleting " + path
            if os.path.exists(path):
                os.rmdir(path)
            
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)
        
    def testSortSubDirectories(self):
        expected_list = ['20120912072912', '20120912073312', '20120913072230']
        monitor = FileMonitor(self.device_name)
        monitor.setInboxPath(self.temp_dir)
        # call property setter for testing
        actual_list = monitor.sortSubDirectories()
#        print actual_list
        result = cmp(expected_list, actual_list)
        # print "result:" + str(result)
        self.assertEquals(0, result, 'number not equals')
        
    def testSortFiles(self):
        dest_dir =  os.path.join(self.temp_dir, "20120913072230")
        actual_list = FileMonitor.SortFiles(dest_dir)
        #expected_list = ['audit.log.3.gz','audit.log.2.gz','audit.log.1.gz']
        expected_list = ['audit.log.2.gz','audit.log.1.gz']
        result = cmp(expected_list, actual_list)
        self.assertEquals(0, result, 'sorted files not in descend order')
        
    def testHasZipFile(self):
        dest_dir =  os.path.join(self.temp_dir, "20120913072230")
        
        self.assertTrue(FileMonitor.HasZipFile(dest_dir), 
                         "directory 20120913072230 should not be empty")
        
    def testParseZippedFiles(self):
        '''def parseZippedFiles(self,directory): 47 + 21 = 68'''
        
        test_dir = self.temp_dir + '/20120913072230/'
#        print test_dir
        monitor = FileMonitor(self.device_name)
        monitor.setInboxPath(self.temp_dir)
#        print monitor.__dict__
        monitor.parseZippedFiles(test_dir)
        num_events = self.db.count('events')
        self.db.removeAll('events')
        self.assertEquals(85, num_events, 'events collection should have 85 documents')
        
if __name__ == '__main__': unittest.main()        