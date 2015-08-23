#!/usr/bin/env python

import string
import sys
import os

try:
	import matplotlib.pyplot as plt
except:
	print "No plot library"

def helper():
	print "log file path needed\n"
	exit()

def logread(filename):
	fopen = open(filename, 'r')
	monitors = {}
	contentions = 0
	for line in fopen:
		if line.find("enter monitor") >= 0:
			word = line.split()
			threadid  = word[0].split(':')[0]
			monitorid = word[4]
			if monitorid in monitors and monitors[monitorid] != threadid:
				contentions += 1
			else:
				monitors[monitorid] = threadid
		elif line.find("entered monitor") >= 0:
			word = line.split()
			threadid  = word[0].split(':')[0]
			monitorid = word[4]
			if monitorid in monitors and monitors[monitorid] != threadid:
				contentions += 1
			else:
				monitors[monitorid] = threadid
	fopen.close()
	return (contentions, len(monitors))

def compare(dict1):
	for i in dict1:
		if dict1[i][0] != 0:
			val = dict1[i][0]
			for j in range(len(dict1[i])):
				dict1[i][j] = float(float(dict1[i][j])/float(val))
	return dict1

def printinfo(dict1):
	for i in dict1:
		print i, ": "
		print "\t", dict1[i]
		print "======================================="

if __name__ == '__main__':
	try:
		script, filepath = sys.argv
	except:
		helper()

	lockdict = {}
	contentiondict= {}
	threadlist = [2, 4, 8, 16, 32, 48]
	if not os.path.isfile(filepath):
		for root,dirs,files in os.walk(filepath):
			flist = [os.path.join(root, fs) for fs in files]
			for fp in flist:
				(contentions, monitors) = logread(fp)
				filename  = fp.split('_')[0]
				threadnum = int(fp.split('_')[1])
				index = threadlist.index(threadnum)
				if filename in lockdict:
					lockdict[filename][index] = monitors
					contentiondict[filename][index] = contentions
				else:
					lockdict[filename] = [0,0,0,0,0,0]
					contentiondict[filename] = [0,0,0,0,0,0]
#				print fp, ": "
#				print "\tlock contentions:\t",contentions 
#				print "\ttotal monitors:  \t",monitors
#				print "============================================"
	lockdict = compare(lockdict)
	contentiondict = compare(contentiondict)
	print "Lock info comes:\n----------------------------------------------"
	printinfo(lockdict)
	print "Contention info comes:\n----------------------------------------------"
	printinfo(contentiondict)
	print "DONE"

