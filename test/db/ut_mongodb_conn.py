#!/usr/bin/python

import unittest
import sys
from datetime import datetime

from pymongo import Connection
from pymongo.errors import ConnectionFailure

class UtMongoDBConn(unittest.TestCase):
    '''Test python MongoDB environment setup'''
    
    def setUp(self):
        "Populate seed data into testing database"
        
        try:
            connection = Connection(host="localhost", port=27017)
        except ConnectionFailure, e:
            sys.stderr.write("Could not connect to MongoDB: %s" % e)
            sys.exit(1)
            
        db_handler = connection["sfm"]
        assert db_handler.connection == connection
        
        # table 1 a event_count document
        time_string = "2012/09/17 23:14:43"
        time = datetime.strptime(time_string, "%Y/%m/%d %H:%M:%S")
        event_document = {
            "id" : 1,
            "creat_time" : time,
            "index" : 5
        }
        db_handler.event_count.insert(event_document, safe=True)
        #print "Successfully inserted document: %s" % event_document
        connection.end_request()
#        if db_handler.end_request:
#            print "handler end-request = true"

    def tearDown(self):
        "Delete seed data from testing database"
        
        try:
            connection = Connection(host="localhost", port=27017)
        except ConnectionFailure, e:
            sys.stderr.write("Could not connect to MongoDB: %s" % e)
            sys.exit(1)
            
        db_handler = connection["sfm"]
        assert db_handler.connection == connection
        db_handler.event_count.remove({"id":1}, safe=True)
        connection.end_request()
        
    def test_connection(self):
        "Populate seed data into testing database"
        
        try:
            connection = Connection(host="localhost", port=27017)
        except ConnectionFailure, e:
            sys.stderr.write("Could not connect to MongoDB: %s" % e)
            sys.exit(1)
            
        db_handler = connection["sfm"]
        assert db_handler.connection == connection
        
        event_count_doc = db_handler.event_count.find_one({"id":1})

        self.assertEquals(5, event_count_doc["index"], 'index should be 25')
        print "Successfully get index: %s" % event_count_doc
        connection.end_request()

if __name__ == '__main__': unittest.main()