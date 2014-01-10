#!/usr/bin/python

import ply.yacc as yacc
from query_lexer import QueryLexer
from datetime import timedelta
from datetime import datetime
import calendar
#################################
# 
#logical_expression  : expression 
#                    | logical_expression AND expression
#
#expression  : relation_expression
#            | in_expression
#            | time_expression
#            | like_expression
#
#like_expression     : ID LIKE STRING
#
#time_expression     : ID IN DAY
#                    | ID IN MONTH
#
#relation_expression : ID EQ factor
#                    | ID GT factor
#                    | ID LT factor
#                    | ID GE factor
#                    | ID LE factor
#
#in_expression : ID IN LPAREN factors RPAREN
#
#factors : factor
#        | factors COMMA factor
#
#factor  : STRING
#        | IP
#        | NUMBER
#        | TIME
#        | DAY
#################################
#1)    ip in (10.30.2.1, 130.2.3.2) =>
#        {'ip': {'$in' : ['10.30.2.1', '130.2.3.2']} }
#2)    domain = 'abc.com'
#3)    
#
#4)    time in 2009-06 => {'create_time': {'$gte':start_time, '$lte':end_time}
# http://stackoverflow.com/questions/42950/get-last-day-of-the-month-in-python
class QueryParser:
    
    def __init__(self):
        self.debugfile = "query_parser.log"
#        self.tabmodule = "query_parser.txt"
        
        self.lexer = QueryLexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self,write_tables=0,debug=0,
                  debugfile=self.debugfile)
#                  tabmodule=self.tabmodule)
    
    def p_logical_expression(self,t):
        '''logical_expression : logical_expression AND expression'''
        has_duplicated_keys = False
        for key in t[3].keys():
            if t[1].has_key(key):
                has_duplicated_keys = True
                t3_value = t[3][key]
                t1_value = t[1][key]
                t1_value.update(t3_value)
                
        if not has_duplicated_keys:
            t[1].update(t[3])
        t[0] = t[1]
            
        
    def p_logical_expression_base(self,t):
        '''logical_expression  : expression'''
        t[0] = t[1]
#        print 'p_logical_expression_base-> t1',t[1]
        
    def p_expression(self,t):
        '''
        expression  : relation_expression
                    | in_expression
                    | time_expression
                    | like_expression
        '''
        t[0] = t[1]
    
    def p_like_expression(self, t):
        '''like_expression : ID LIKE STRING'''
        t[0] = { t[1] : {'$regex' : t[3] } }
#        print t[0]

    def p_relation_expression(self,t):
        '''
        relation_expression : ID NE factor
                            | ID GE factor
                            | ID LE factor 
                            | ID EQ factor
                            | ID GT factor
                            | ID LT factor
                            
        '''
        if t[2] == '=':
            t[0] = { t[1] : t[3] }
        elif t[2] == '!=':
            t[0] = { t[1] : { '$ne' : t[3]}}
        elif t[2] == '>=':
            t[0] = { t[1] : { '$gte' : t[3]}}
        elif t[2] == '<=':
            t[0] = { t[1] : { '$lte' : t[3]}}
        elif t[2] == '>':
            t[0] = { t[1] : { '$gt' : t[3]}}
        elif t[2] == '<':
            t[0] = { t[1] : { '$lt' : t[3]}}
        else:
            print 'logic expression error'
            
        
    def p_in_expression(self,t):
        '''in_expression : ID IN LPAREN factors RPAREN'''        
#        t[0] = ('p_in_expression(t)', t[1],t[2],t[3],t[4],t[5])
#        print t[2], t[3]
        in_clause_dict = { t[1]: {'$' + t[2] : t[4]} }
        t[0] = in_clause_dict
#        self.result = t[0]

    def p_factors(self, t):
        '''factors : factors COMMA factor'''
#        t[0] = ('calling p_factors(t)', t[1],t[2],t[3])
#        print t[0]
        t[1].append(t[3])
        t[0] = t[1]
        
    def p_factors_base(self,t):
        '''factors : factor'''
#        t[0] = 'calling p_factors_base(t)',t[1]
#        print t[0]
        t[0] = [t[1]]
    
    def p_factor(self,t):
        '''factor : IP
                  | STRING
                  | NUMBER
                  | TIME
                  | DAY
        '''
#        t[0] = ('calling p_factor(t)',t[1])
#        print 'p_factor->',t[1]
        t[0] = t[1]
    
    def p_time_expression(self,t):
        '''time_expression      : time_in_day_expression
                                | time_in_month_expression
        '''
        t[0] = t[1]
    
    def p_time_in_day_expression(self,t):
        '''time_in_day_expression : ID IN DAY'''
        start_time = t[3]
        end_time = t[3] + timedelta(hours = 23, minutes=59, seconds=59)
#        x = datetime.strftime(end_time, "%Y-%m-%dT%H:%M:%SZ")
#        print x
        time_between_expression = {'create_time': {'$gte':start_time, '$lte':end_time}}
        t[0] = time_between_expression
        
    def p_time_in_month_expression(self,t):
        '''time_in_month_expression : ID IN MONTH'''
        # parse t[3] to get year and month
        year = int(t[3][0:4])
        month = int(t[3][-2:])
        start_end_tuple = calendar.monthrange(year,month)
        end_date = str(start_end_tuple[1])
        # set the first day of the month
        start_time = datetime.strptime(str(year) + '-' + str(month) + '-01T00:00:00Z', "%Y-%m-%dT%H:%M:%SZ")
        # set the first day of next month and create last day by subtracting 1 day from the first day of next month
        end_time = datetime.strptime(str(year) + '-' + str(month) + '-' + end_date + 'T23:59:59Z', "%Y-%m-%dT%H:%M:%SZ")
        time_between_expression = {'create_time': {'$gte':start_time, '$lte':end_time}}
        t[0] = time_between_expression
        
    def p_error(self,t):
        print 'Syntax error at "%s"' % t.value if t else 'NULL'
        global current_state
        current_state = None
        
    def parse(self,data):
        if data:
            return self.parser.parse(data,self.lexer.lexer,0,0,None)
        else:
            return []
        
def test():
    data = 'domain in ( \'aa.com\',\'bb.ca\',\'cc.ca\' ) and size = 346 and ip=122.34.5.67 '   
    ql = QueryParser()
    x = ql.parse(data)
    print x
         
if __name__ == "__main__":test()
