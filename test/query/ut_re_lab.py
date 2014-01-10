#!/usr/bin/python
import unittest,re
from re_lab import ReLab

class UtReLab(unittest.TestCase):
    
    def setUp(self):
        self.re_lab = ReLab()
    
    def test_digit_pattern(self):
        line = '33445.33';
        pattern =  self.re_lab.digit_pattern()
        match_object = pattern.match(line)
        self.assertEquals('33445', match_object.group(), 'number not equals')
#        match_object = re.match(r'[0-9]+',line)
#        if match_object:
#            value = match_object.group()
#            print value
#        else:
#            print 'no match'

    def test_year_pattern(self):
        line = '2012-11-25, 2012-11-26)'
        match_object = re.match(r'[0-9][0-9][0-9][0-9]',line)
        if match_object:
            value = match_object.group()
            print value
        else:
            print 'no match for year'
            
    #2012-11-25T21:49:00Z and 2012-11-25T21:49:13Z and ip=10.30.13.15
    
    def test_month_pattern(self):
        line = '2012-11-25, 2012-11-26)'
        match_object = re.match(r'^([0-9]{4})-?(1[0-2]|0[1-9])',line)
        if match_object:
            value = match_object.group()
            print value
        else:
            print 'no match for month'
            
    def test_day_pattern(self):
        line = '2012-11-25, 2012-11-26)'
        match_object = re.match(r'([0-9]{4})-(1[0-2]|0[1-9])-(3[0-1]|0[1-9]|[1-2][0-9])',line)
        if match_object:
            value = match_object.group()
            print value
        else:
            print 'no match for day'
    
    def test_time_pattern(self):
        line = '2012-11-25T21:49:00Z and 2012-11-25T21:49:13Z'
        match_object = re.match(r'([0-9]{4})-(1[0-2]|0[1-9])-(3[0-1]|0[1-9]|[1-2][0-9])T(2[0-3]|[01]?[0-9]):([0-5]?[0-9]):([0-5]?[0-9])Z',line)
        if match_object:
            value = match_object.group()
            print value
        else:
            print 'no match for time'
    
    def test_ip_pattern(self):
        line = '10.30.2.124/24 terp'
#        ^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$

        ip_pattern=r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
        match_object = re.match(ip_pattern,line)
        
        if match_object:
            value = match_object.group()
            print value
        else:
            print 'no match for ip'