import unittest
from dp.squid_parser import SquidParser

class UtSquidParser(unittest.TestCase):
    
    def setUp(self):
        self.parser = SquidParser()
    
    def testValidateLine(self):
        line = '1352521070 10.30.13.11 GET http://www.sunlife.ca/static/plan/plan_overrideGW.css'        
        result = self.parser.validateLine(line)
        self.assertEqual(result, line, "should be a valid line")

    def testInvalidLine(self):
        line = 'Nov  9 23:17:46 10.30.13.1 1352521070 10.30.13.11 GET http://www.sunlife.ca/static/slfglobal/styles/globalweb.css'
        result = self.parser.validateLine(line)
        self.assertTrue(result is None,"should be an invalid line")
        
    def testParseTime(self):
        ''' time should be 2012/11/09 23:17:50 '''
        epoch_time = '1352521070'
        parsed_time = self.parser.parseTime(epoch_time);
        #print parsed_time.strftime("%Y/%m/%d %H:%M:%S")
        result = parsed_time.strftime("%Y/%m/%d %H:%M:%S")
        
        self.assertEqual(result, '2012/11/09 23:17:50', "time(EST) should be 2012/11/09 23:17:50")

    def testParseUrl(self):
        '''sample URL: http://www.sunlife.ca/static/plan/plan_overrideGW.css'''
        url = 'http://www.sunlife.ca/static/plan/plan_overrideGW.css'
        result = self.parser.parseDomain(url)
        self.assertEqual(result, 'www.sunlife.ca', "domain should be www.sunlife.ca")
        
    def testParseLine(self):
        '''Sample data: 1352521070 10.30.13.11 GET http://www.sunlife.ca/static/plan/plan_overrideGW.css'''
        line_to_parse = '1352521070 10.30.13.11 GET http://www.sunlife.ca/static/plan/plan_overrideGW.css'
        event = self.parser.parseLine(line_to_parse)
        
        event_time = event['create_time'].strftime("%Y/%m/%d %H:%M:%S")
        self.assertEqual(event_time, '2012/11/09 23:17:50', "time(EST) should be 2012/11/09 23:17:50")        
        self.assertEqual(event['ip'], '10.30.13.11', "IP should be 10.30.13.11")
        self.assertEqual(event['domain'], 'www.sunlife.ca', "domain should be www.sunlife.ca")
        
if __name__ == '__main__': unittest.main()