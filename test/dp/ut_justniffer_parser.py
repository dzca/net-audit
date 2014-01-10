#!/usr/bin/python
import unittest
import os,shutil
from dp.justniffer_parser import JustNifferParser
from utils.logger import Logger
from db.mongodb import MongoDB

class UtJustNifferParser(unittest.TestCase):
    '''A Unit Test for dp.ut_justNiffer_parser.UtJustNifferParser'''

    logger = Logger().getLogger("dp.UtJustNifferParser")
    db = MongoDB('esm')
    
    def setUp(self):
        self.parser = JustNifferParser()
        self.test_root_path = os.getcwd() + '/../'
                
        #copy zipped file form data/$device_name/ to tmp/
        self.temp_dir = os.path.join(self.test_root_path, "tmp")
        
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
        
        zip_data_file = self.test_root_path + 'data/justniffer/audit.log.1.gz'
        shutil.copy2(zip_data_file, self.temp_dir)
                
    def tearDown(self):
        "Delete the test directories"
        
        zip_data_file =  os.path.join(self.temp_dir, 'audit.log.1.gz')
        if os.path.exists(zip_data_file):
            os.unlink (zip_data_file)
            
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    @property
    def sample_path(self):
        sample_path = self.test_root_path + 'samples/' + self.device_name+ '/audit.log.1'
        return sample_path
    
    @property
    def sample_zipped_file_path(self):
        sample_zipped_file_path = self.test_root_path + 'samples/' + self.device_name+ '/audit.log.1'
        return sample_zipped_file_path
    
    def testParseTime(self):
        ''' time should be 2012/11/16 07:52:07'''
        epoch_time = '1353070327'
        parsed_time = self.parser.parseTime(epoch_time);
#        print parsed_time.strftime("%Y/%m/%d %H:%M:%S")
        result = parsed_time.strftime('%Y/%m/%d %H:%M:%S')
        self.assertEqual(result, '2012/11/16 07:52:07', 'time(EST) should be 2012/11/16 07:52:07')
        
    def testParseLine(self):
        '''Sample data: 1353070327 10.30.13.11 news.bbcimg.co.uk 1248 /view/3_0_6/cream/hi/shared/global.css'''
        line_to_parse = '1353070327 10.30.13.11 news.bbcimg.co.uk 1248 /view/3_0_6/cream/hi/shared/global.css'
        event = self.parser.parseLine(line_to_parse)
        
#        print 'size-->'+ str(event['size'])
        event_time = event['create_time'].strftime("%Y/%m/%d %H:%M:%S")
        self.assertEqual(event['device_id'], 1, 'device id should be 1')
        self.assertEqual(event_time, '2012/11/16 07:52:07', 'time(EST) should be 2012/11/16 07:52:07')
        self.assertEqual(event['ip'], '10.30.13.11', 'IP should be 10.30.13.11')
        self.assertEqual(event['size'], '1248', 'size should be 1248')
        self.assertEqual(event['domain'], 'news.bbcimg.co.uk', 'domain should be news.bbcimg.co.uk')
        
    def testParserId(self):
        device_id = self.parser.device_map['justniffer'];
        #print 'device_id=' + str(device_id)
        self.assertEqual(device_id,1, 'device id for justniffer should be 1')

    def testProcessZippedFile(self):
        ''' validate:
            db record count should match
            folder should have one file left
        '''
        
        zip_data_file =  os.path.join(self.temp_dir, 'audit.log.1.gz')
        self.parser.processZippedFile(zip_data_file)
        dir_count = len(os.listdir(self.temp_dir))
        
        self.assertEquals(0, dir_count, 'should be 0 file left')
        
        num_events = self.db.count('events')
#        print 'size-->'+ str(num_events)
        self.db.removeAll('events')
        self.assertEquals(49, num_events, 'audit.log.1 should have 49 documents')

if __name__ == '__main__': unittest.main()