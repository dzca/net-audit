#!/usr/bin/python

import unittest
import sys
from datetime import datetime

from db.mongodb import MongoDB
from pymongo import Connection
from pymongo.errors import ConnectionFailure

class UtMongoDB(unittest.TestCase):
    '''Unit Test driver for db.mongodb.MongoDB'''
    
    db = MongoDB('esm')
        
    def tearDown(self):
        "Delete seed data from testing database"
        try:
            connection = Connection(host="localhost", port=27017)
        except ConnectionFailure, e:
            sys.stderr.write("Could not connect to MongoDB: %s" % e)
            sys.exit(1)
            
        db_handler = connection["esm"]
        assert db_handler.connection == connection
        db_handler['justniffer_events'].drop()
        connection.end_request()


    def test_insert_events(self):
        events = []
        time_string = "2012/09/17 23:14:43"
        time = datetime.strptime(time_string, "%Y/%m/%d %H:%M:%S")
        event = {'create_time': time, 'ip': '10.30.26.112', 'domain':'news.bbcimg.co.uk', 
                 'size':253,'path':'/view/3_0_6/cream/hi/shared/global.css'}
        events.append(event)
        
        time_string = "2012/09/17 23:14:44"
        time = datetime.strptime(time_string, "%Y/%m/%d %H:%M:%S")
        event = {'create_time': time, 'ip': '10.30.26.116', 'domain':'news.bbcimg.co.uk',
                 'size':1043,'path':'/view/3_0_6/cream/hi/shared/global.css'}
        events.append(event)
        self.db.insertBulk(events, 'justniffer_events')
        
        count = self.db.count('justniffer_events')
        self.assertEqual(count, 2, "inserted events should be 2")
        
        
if __name__ == '__main__': unittest.main()