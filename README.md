# end-to-end
A simple framework for regression testing command line applications

This simple framework can execute command line applications on Windows and Linux, provide input files, and capture
standard output, standard error, and output files.

Tests are organized as one test per subdirectory.  Adding a new test involves only adding a new subdirectory for the test, with
test inputs and golden results.

An example is provided with a simple program (testapp.py) that counts words and characters in text files, and two tests for
the program.  To run the example, simply run 'end-to-end.py'


Requirements:
	Python 2.7

Running tests:
	end-to-end.py  [tests]
	
Example:
	end-to-end         - will run all tests in the end-to-end directory
	end-to-end t1 t2   - will run tests t1, t2, t3
	

Test Setup:
	Each test contains 3 directories and an optional readme.txt file
	input\     - Test inputs
	scripts\   - Test scripts
	golden\    - Golden test results
	readme.txt - Test purpose
	
	A readme.txt in each test may be provided to document the test purpose. If provided, it is printed during the test run.
	
	In addition, the common\ directory contains input and script files that are common to all tests.  These common files may be overridded by files in input\ and scripts\ directories.
	
	The temp\ directory is used for running each test
	
	Each test must have a script named 'runtest.py' to run the test.  This is the only requirement.
	
Testing Process:
	When a test is run, the following occurs
	1) The temp\ directory is cleared out
	2) The contents of common\, input\ and scripts\ are copied to temp\, in that order
	3) The script 'runtest.py' is executed in the temp\ directory, performing the test
	4) Each file in golden\ is compared with the same named file in temp\, differences are failures
	
Expected Output:
	Output is to stdout.  Each test prints PASSED or FAILED.  If failed, the difference is printed.
	Example:
	
		**************************
		*  Executing: test1
		*  Test 1: A simple test with a single line of text
		*  Comparing: count.txt
		*  Comparing: runtest.log
		*  PASSED: test1
		**************************

		**************************
		*  Executing: test2
		*  Test 2: An example of a failing test (incorrect result is harnessed)
		*  Comparing: count.txt
		Comparing files...\TEMP\count.txt and ...\GOLDEN\COUNT.TXT
		***** ...\TEMP\count.txt
		Char count: 54
		***** ...\GOLDEN\COUNT.TXT
		Char count: 55
		*****
		*  Comparing: runtest.log
		*  FAILED: test2
		**************************
