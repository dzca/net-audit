#!/usr/bin/python

import sys,re

class ReLab:
    '''Lab code for regular expression'''
    
    def date_pattern(self):
        pattern = re.compile('')
        return pattern
        
    def year_pattern(self):
        return r''
        
    def digit_pattern(self):
#        return re.compile(r'\b[0-9]+\b')
        return re.compile(r'\b\d+$')
    
def test():
#    pattern = re.compile('')
    line = "Cats are smarter than dogs";

    matchObj = re.match( r'(.*) are(\.*)', line, re.M|re.I)
    
    if matchObj:
       print "matchObj.group() : ", matchObj.group()
       print "matchObj.group(1) : ", matchObj.group(1)
       print "matchObj.group(2) : ", matchObj.group(2)
    else:
       print "No match!!"
       
if __name__ == '__main__':test()