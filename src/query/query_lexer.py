#!/usr/bin/python

import re
from datetime import datetime
import ply.lex as lex

# ------------------------------------------------------------
# query_lexer.py
#
# tokenizer for log query expression 
# ------------------------------------------------------------

class QueryLexer:
    reserved = {
    'in':'IN',
#    'between':'BETWEEN',
    'like':'LIKE',
    'and':'AND'
            }

    tokens = [
        'IP',
        'TIME',
        'DAY',
        'MONTH',
        'NUMBER',
        'STRING',
        'ID',
        'COMMA',
        'LPAREN',
        'RPAREN',
        'GT',
        'LT',
        'GE',
        'LE',
        'EQ',
        'NE'
    ] + list(reserved.values())

    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_COMMA = r','
#    t_BETWEEN = r'between'
    t_IN = r'in'
    t_LIKE = r'like'
    t_AND = r'and'
    t_IP = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
#    t_TIME = r'([0-9]{4})-(1[0-2]|0[1-9])-(3[0-1]|0[1-9]|[1-2][0-9])T(2[0-3]|[01]?[0-9]):([0-5]?[0-9]):([0-5]?[0-9])Z'    #2012-11-25T21:49:00Z
#    t_DAY = r'([0-9]{4})-(1[0-2]|0[1-9])-(3[0-1]|0[1-9]|[1-2][0-9])'     #2012-11-25 
    t_MONTH = r'\b([0-9]{4})-(1[0-2]|0[1-9])\b'   #2012-08
#    t_STRING = r'\'[^\']+\''
    t_NE = r'!='
    t_LE = r'<='
    t_GE = r'>='
    t_LT = r'<'
    t_GT = r'>'
    t_EQ = r'='
#    t_NUMBER = r'\b\d+$'
    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'
    
    def __init__(self):
        self.lexer = lex.lex(module=self,debug=0)
        
    def t_TIME(self,t):
        r'([0-9]{4})-(1[0-2]|0[1-9])-(3[0-1]|0[1-9]|[1-2][0-9])T(2[0-3]|[01]?[0-9]):([0-5]?[0-9]):([0-5]?[0-9])Z'
        t.value = datetime.strptime(t.value, "%Y-%m-%dT%H:%M:%SZ") 
        return t
        
    def t_DAY(self,t):
        r'\b([0-9]{4})-(1[0-2]|0[1-9])-(3[0-1]|0[1-9]|[1-2][0-9])\b'
        t.value = datetime.strptime(t.value, "%Y-%m-%d") 
        return t
        
    def t_NUMBER(self,t):
        r'\b\d+\s+\b|\b\d+$'
        t.value = int(t.value)
        return t

    def t_STRING(self,t):
        r'\'[^\']+\''
        raw_ip = t.value.strip()
        t.value = re.sub("'",'', raw_ip).strip()
        return t
        
    # Check for reserved words
    def t_ID(self,t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value,'ID')
        return t
    
    # Define a rule so we can track line numbers
    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)
    
    # Error handling rule
    def t_error(self,t):
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)
    
def test():
#    data = 'ip in (10.30.2.1, 130.2.3.2)'
#    data = 'domain in ( \'aa.com\',\'bb.ca\' ) and size >=3678'
#    data = 'domain in ( \'aa.com\',\'bb.ca\',\'cc.ca\' ) and size >= 346 and ip=122.34.5.67'
#    data = 'domain in ( \'aa.com\',\'bb.ca\',\'cc.ca\' ) and ip=122.34.5.67 and size >= 346'
#    data = 'domain in ( \'aa.com\',\'bb.ca\',\'cc.ca\' ) and ip=122.34.5.67 and size >= 346 and create_time > 2010-12-19'
    data = 'create_time >=2012-11-25T21:49:00Z and create_time <= 2012-11-25T21:49:13Z and domain like cnncom'
    ql = QueryLexer()
    lexer = ql.lexer
    lexer.input(data)
    while True:
        token = lexer.token()
        if not token: break
        print token
         
if __name__ == "__main__":test()