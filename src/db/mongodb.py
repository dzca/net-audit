#!/usr/bin/python

import sys,pymongo

from pymongo import Connection
from pymongo.errors import ConnectionFailure
from bson.code import Code

class MongoDB:
    '''Manage database layer for Mongodb'''
    
    def __init__(self,db_name):
#        print "MongoDB constructor"
        self.db_name = db_name
        self.db_host = 'localhost'
    
    def insertBulk(self,docs,table_name):
        "insert a list of events map"
        try:
            connection = Connection(host=self.db_host, port=27017)
        except ConnectionFailure, e:
            sys.stderr.write("Could not connect to MongoDB: %s" % e)
            sys.exit(1)
            
        db_handler = connection[self.db_name]
        
        assert db_handler.connection == connection
        db_handler[table_name].insert(docs, safe=True)
        connection.end_request()
        
    def count(self, table_name, query={}):
        try:
            connection = Connection(host=self.db_host, port=27017)
        except ConnectionFailure, e:
            sys.stderr.write("Could not connect to MongoDB: %s" % e)
            sys.exit(1)
        db_handler = connection[self.db_name]
        
        assert db_handler.connection == connection
        count = db_handler[table_name].find(query).count()
        connection.end_request()
        return count
    
    def removeAll(self, table_name):
        try:
            connection = Connection(host=self.db_host, port=27017)
        except ConnectionFailure, e:
            sys.stderr.write("Could not connect to MongoDB: %s" % e)
            sys.exit(1)
            
        db_handler = connection[self.db_name]
        
        assert db_handler.connection == connection
        db_handler[table_name].remove()
        connection.end_request()
    
    def find(self, table_name, page_size, page_num, sort_field, sort_direction=pymongo.DESCENDING,query={}):
        
        #    name like '%m%' ==> db.users.find({"name": /.*m.*/}) db.collectionname.find({'files':{'$regex':'^File'}})
        try:
            connection = Connection(host=self.db_host, port=27017)
        except ConnectionFailure, e:
            sys.stderr.write("Could not connect to MongoDB: %s" % e)
            sys.exit(1)
            
        db_handler = connection[self.db_name]
        assert db_handler.connection == connection
        if page_num > 1:
            events_doc = db_handler[table_name].find(query).sort([(sort_field,sort_direction)]).limit(page_size).skip(page_size * (page_num-1) )
        else:
            events_doc = db_handler[table_name].find(query).sort([(sort_field,sort_direction)]).limit(page_size)
        connection.end_request()
#        if event_count_doc:
#            print "Successfully fetch document:" + str(event_count_doc["index"])
        return events_doc
        
    def countSize(self,table_name,query={}):
        '''count download size group by source ip'''
        try:
            connection = Connection(host=self.db_host, port=27017)
        except ConnectionFailure, e:
            sys.stderr.write("Could not connect to MongoDB: %s" % e)
            sys.exit(1)
            
        db_handler = connection[self.db_name]
        assert db_handler.connection == connection

        key={"ip":True}
        initial = {"size":0}
        reducer = Code('function(doc, prev) {prev.size = prev.size + doc.size;}')
        download_size_doc = db_handler[table_name].group(key,query,initial,reducer)
        connection.end_request()
        return download_size_doc
    
    def get_user(self,user_name):
        '''get users by name'''
        try:
            connection = Connection(host=self.db_host, port=27017)
        except ConnectionFailure, e:
            sys.stderr.write("Could not connect to MongoDB: %s" % e)
            sys.exit(1)
            
        db_handler = connection[self.db_name]
        assert db_handler.connection == connection

        users_doc = db_handler['users'].find({'username' : user_name})
        connection.end_request()
        return users_doc
    
def test():
    db = MongoDB('esm')
    num_of_events = db.count('events')
    print 'num_of_events = ' + str(num_of_events)
    
if __name__ == "__main__":test()
    
