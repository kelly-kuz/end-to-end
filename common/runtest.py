#!/usr/bin/python
'''
Example run script for the end-to-end test framework
Modify to suit your application

Purpose:
Run the test application (specified by argv[1])

This sample script runs parameters 'input.txt' and redirects the STDOUT and STDERR
to 'runtest.log'
'''
import sys
import os
from subprocess import Popen, PIPE, STDOUT

def runtest():
    testapp = sys.argv[1]

    cmd =  '"' + testapp + '"' + ' input.txt > runtest.log 2>&1'
    stat = os.system('"' + cmd + '"')
    sys.exit(stat)
    
if __name__ == "__main__":
    runtest()
