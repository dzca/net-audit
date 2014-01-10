#!/usr/bin/python

import unittest
from query.query_parser import QueryParser
from datetime import datetime

class UtQueryParser(unittest.TestCase):
    '''complex query test driver'''
    
    @property
    def parser(self):
        parser = QueryParser() 
        return parser
    
    def test_empty(self):
        data = ''
        result = self.parser.parse(data)
        expected_result = []
        self.assertEqual(result, expected_result)
        
    def test_equals_1(self):
        data = 'ip = 10.30.2.1'
        result = self.parser.parse(data)
        expected_result = {'ip' : '10.30.2.1'}
        self.assertEqual(result, expected_result)
    
    def test_greater_than(self):
        data = 'size >= 567'
        result = self.parser.parse(data)
#        print result
        expected_result = {'size': {'$gte': 567}}
        self.assertEqual(result, expected_result)
        
    def test_ip_in(self):
        data = 'ip in ( 10.30.2.1, 130.2.3.2 )'
        result = self.parser.parse(data)
        expected_result = {'ip': {'$in': ['10.30.2.1', '130.2.3.2']}}
        self.assertEqual(result, expected_result)
        
    def test_domain_in(self):
        data = 'domain in ( \'aa.com\',\'bb.ca\',\'cc.ca\' )'
        result = self.parser.parse(data)
        expected_result = {'domain': {'$in': ['aa.com', 'bb.ca', 'cc.ca']}}
        self.assertEqual(result, expected_result)
        
    def test_number_and_ip_1(self):
        data = 'domain in ( \'aa.com\',\'bb.ca\',\'cc.ca\' ) and size = 346 and ip=122.34.5.67 '
        result = self.parser.parse(data)
#        print 'result=',result
        expected_result = {'ip': '122.34.5.67', 'domain': {'$in': ['aa.com', 'bb.ca', 'cc.ca']}, 'size': 346}
        self.assertEqual(result, expected_result)
        
    def test_number_and_ip_2(self):
        data = 'domain in ( \'aa.com\',\'bb.ca\',\'cc.ca\' ) and ip=122.34.5.67  and size = 346'
        result = self.parser.parse(data)
#        print result
        expected_result = {'ip': '122.34.5.67', 'domain': {'$in': ['aa.com', 'bb.ca', 'cc.ca']}, 'size': 346}
        self.assertEqual(result, expected_result)
        
    def test_time_in_day_expression(self):
        data = 'time in 1992-12-23'
        start_time = datetime.strptime('1992-12-23T00:00:00Z', "%Y-%m-%dT%H:%M:%SZ")
        end_time = datetime.strptime('1992-12-23T23:59:59Z', "%Y-%m-%dT%H:%M:%SZ")
        expected_result = {'create_time': {'$gte':start_time, '$lte':end_time}}
        result = self.parser.parse(data)
#        print result
        self.assertEqual(result, expected_result)
        
    def test_time_in_month_expression(self):
        data = 'time in 2009-04'
        start_time = datetime.strptime('2009-04-01T00:00:00Z', "%Y-%m-%dT%H:%M:%SZ")
        end_time = datetime.strptime('2009-04-30T23:59:59Z', "%Y-%m-%dT%H:%M:%SZ")
        expected_result = {'create_time': {'$gte':start_time, '$lte':end_time}}
        result = self.parser.parse(data)
#        print result
        self.assertEqual(result, expected_result)
    
    def test_time_range(self):
        data = 'create_time >2012-11-25T21:49:00Z and create_time <= 2012-11-25T21:49:13Z'
        start_time = datetime.strptime('2012-11-25T21:49:00Z', "%Y-%m-%dT%H:%M:%SZ")
        end_time = datetime.strptime('2012-11-25T21:49:13Z', "%Y-%m-%dT%H:%M:%SZ")
        expected_result = {'create_time': {'$lte': end_time, '$gt': start_time}}
        result = self.parser.parse(data)
#        print result
        self.assertEqual(result, expected_result)

    def test_like(self):
        data = 'domain like \'^twitter.com\''
        expected_result = { 'domain' : {'$regex':'^twitter.com'}}
        result = self.parser.parse(data)
#        print result
        self.assertEqual(result, expected_result)

    def test_time_in_month_year_end(self):
        data = 'time in 2012-12'
        start_time = datetime.strptime('2012-12-01T00:00:00Z', "%Y-%m-%dT%H:%M:%SZ")
        end_time = datetime.strptime('2012-12-31T23:59:59Z', "%Y-%m-%dT%H:%M:%SZ")
        expected_result = {'create_time': {'$gte':start_time, '$lte':end_time}}
        result = self.parser.parse(data)
#        print result
        self.assertEqual(result, expected_result)