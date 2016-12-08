#!/usr/bin/python
"""
End to End testing script.   This script, but not the test cases that it runs, is released under MIT licesne

The MIT License (MIT)
Copyright (c) 2016: Ed Kuzemchak
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation 
files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE 
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR 
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

"""
Usage:  end-to-end.py  [test names] [-harness]
If no test names are given, all the tests in the end-to-end/ directory are run

Running:
For each test, the following actions are performed
- The contents of common/ are copied to the temp/ directory
- The contents of input/ are copied to the temp/ directory
- The script 'runtest.py' is executed with the temp/ directory as the CWD
- if '-harness' is given, for each file in golden/, the same file in temp/ is copied to golden (reharnessing the golden result)
- For each file in golden/ the file is compared to the same named file in temp/
"""

import os
import glob
import shutil
import sys
from subprocess import Popen, PIPE, STDOUT

def main():
    thisdir = os.path.dirname(os.path.realpath(__file__))
    endtoenddir = os.path.join(thisdir, 'end-to-end')
    tempdir = os.path.join(thisdir, 'temp')
    harness = False
    
    ### CONFIGURATION SETTINGS ###
    # The application to test - the path is relative to tempdir
    testapplication = '..\\bin\\testapp.py'
    # An application to compare logs.  FC works OK on Windows
    # A gool alternative is DiffUtils: http://gnuwin32.sourceforge.net/packages/diffutils.htm
    compare = '..\\tools\FC.bat'
    ### END OF CONFIGURATION SETTINGS ###

    failures = []

    if '-harness' in sys.argv:
        harness = True
        print '**************************'
        print '*  Harnesessing Goldens  *'
        print '**************************'
    
    if len(sys.argv) > (2 if harness else 1):
        # Run those tests given in the arguments
        testdirs = sys.argv[1:]
    else:
        # Run all the tests in the end-to-end dir
        testdirs = [d for d in os.listdir(endtoenddir) if os.path.isdir(os.path.join(endtoenddir, d))]

            
    for test in testdirs:
        if test == '-harness':
            continue
            
        if not os.path.exists(os.path.join(endtoenddir, test, 'readme.txt')):
            print '*** Invalid test name - no readme.txt found in: ' + test
            continue
        
        print ''
        print '**************************'
        print '*  Executing: ' + test

        # If the file contains a readme - echo it here
        if (os.path.exists(os.path.join(endtoenddir, test, 'readme.txt'))):
            readme = open(os.path.join(endtoenddir, test, 'readme.txt'), 'r')
            try:
                for line in readme:
                    # Print each line
                    print '*  ' + line.rstrip()
            finally:
                readme.close()

        # Clean out temp/ dir
        for file in glob.glob(tempdir + '/*'):
            os.remove(file)

        # Copy common/* to temp/
        for file in glob.glob(os.path.join(thisdir, 'common') + '/*'):
            shutil.copy(file, tempdir)

        # Copy input/* to temp/
        for file in glob.glob(os.path.join(endtoenddir, test, 'input') + '/*'):
            shutil.copy(file, tempdir)

        # Copy scripts/* to temp/
        for file in glob.glob(os.path.join(endtoenddir, test, 'scripts') + '/*'):
            shutil.copy(file, tempdir)

        # Run the runtest.py script from temp/ with testapplication as argv[1]
        testfile = '"' + os.path.join(tempdir, 'runtest.py') + '"'
        cmd = testfile + ' ' + testapplication
        os.chdir(tempdir)
        #print cmd
        stat = os.system('"' + cmd + '"')
        
        # Harness support
        if harness == True:
            # For each file in Golden, copy the same file from temp/ to Golden/
            for file in glob.glob(os.path.join(endtoenddir, test, 'golden') + '/*'):
                fname = os.path.split(file)[1]
                print '*  Harnessing: ' + fname
                shutil.copy(os.path.join(tempdir, fname), file) 
            
        
        if stat == 0 or stat == 4:
            # For each file in Golden, compare the file with the same file in temp/
            passed = True
            for file in glob.glob(os.path.join(endtoenddir, test, 'golden') + '/*'):
                fname = os.path.split(file)[1]
                cmd = compare +  ' "' + os.path.join(tempdir, fname) + '"  "' + file + '"'
                print '*  Comparing: ' + os.path.split(file)[1]

                #print cmd
                if os.name == 'posix':
                    if os.system(cmd) != 0:
                            passed = False
                else:
                    if os.system('"' + cmd + '"') != 0:
                            passed = False

            if passed:
                print '*  PASSED: ' + test
                print '**************************'
            else:
                print '*  FAILED: ' + test
                print '**************************'
                failures.append(test)
        else:
            print '* EXCEPTION EXECUTING TEST'
            print '**************************'
            failures.append(test)
                
    print ''
    if len(failures) > 0:
        print '*** TEST FAILURES: ' + ', '.join(failures) + ' ****'
    else:
         print '*** ALL TESTS PASSED ****'
    

if __name__ == "__main__":
    main()

