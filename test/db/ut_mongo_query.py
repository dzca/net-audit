#!/usr/bin/python

import unittest,pymongo
from db.mongodb import MongoDB
from query.query_parser import QueryParser

from utils.logger import Logger
import subprocess, os

class UtMongoQuery(unittest.TestCase):
    '''complex query test driver'''
    
    logger = Logger().getLogger("test.UtMongoQuery")
    db = MongoDB('esm')
    
    
    def setUp(self):
#        self.logger.debug('UtMongoQuery.setUp()')
        current_path = os.getcwd()
        self.runBash(current_path+'/import.sh')

    def tearDown(self):
#        self.logger.debug('UtMongoQuery.tearDown()')
        self.db.removeAll('events')
    
    def runBash(self,file_name):
        '''run a shell script.'''
        try:
            subprocess.call([file_name], shell=True)
        except OSError, e:
            self.logger.exception("bash script "+file_name+" execution failed:" + e)
            
    def test_count(self):
        stat_quest = 'time in 2012-11-25 and domain like \'twitter.com\''
        query = QueryParser().parse(stat_quest)
        count = self.db.count('events', query)
        self.assertEqual(count, 7)
    
    def test_find(self):
        quest = 'create_time >=2012-11-25T21:49:00Z and create_time <= 2012-11-25T21:49:13Z'
        query = QueryParser().parse(quest)
        events = self.db.find('events',25,1, 'create_time',pymongo.DESCENDING, query)

        i = 1
        for event in events:
            event_time = event.get('create_time').strftime("%Y/%m/%d %H:%M:%S")
            domain = event.get('domain')
            ip = event.get('ip')
            size = event.get('size')
            print '['+str(i)+',' + ip + ',' + domain + ',' + event_time +',' + str(size) +']'
            i+=1

    def test_group(self):
        quest = 'create_time >=2012-11-25T21:49:00Z and create_time <= 2012-11-25T21:49:13Z'
        query = QueryParser().parse(quest)
        results = self.db.countSize('events', query)
        for doc in results:
            print doc
