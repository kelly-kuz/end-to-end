#! /usr/bin/python
#
# Example test application for end-to-end.py
#
# Simply count words and characters in a text file provided as argv[1]
# report the word count to STDOUT and char count to 'count.txt'
#
import sys

file = open(sys.argv[1])
wordcount = 0
charcount = 0

for word in file.read().split():
	wordcount += 1
	charcount += len(word)

print 'Word count: ' + str(wordcount)

out=open('count.txt', 'w')
out.write('Char count: ' + str(charcount))
out.close()
