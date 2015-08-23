#!/usr/bin/python

import sys
import os
import string

def helper(filename):
	fp = open(filename)
	minorgc = 0
	majorgc = 0
	minortime = 0.0
	majortime = 0.0
	minorlist = []
	majorlist = []
	minortimelist = []
	majortimelist = []
	for line in fp:
		if line.find("Full GC") >= 0:  # major GC
			majorgc += 1
			majortime += float(line.split()[-7])
		elif line.find("GC") >= 0: # minor GC
			minorgc += 1
			minortime += float(line.split()[-7])
		elif line.find("%%%%%%%%%%%") >= 0:  # new run
			minorlist.append(minorgc)
			minorgc = 0
			majorlist.append(majorgc)
			minortimelist.append(minortime)
			minortime = 0.0
			majortimelist.append(majortime)
			majortime = 0.0
	fp.close()
	return(float(sum(minorlist)/len(minorlist)), float(sum(majorlist)/len(majorlist)), float(sum(minortimelist)/len(minortimelist)), float(sum(majortimelist)/len(majortimelist)))

if __name__ == "__main__":
	if len(sys.argv) < 2:
		sys.exit("file path needed")
	minorgcdict = {}    #[0, 0, 0, 0, 0, 0, 0]
	majorgcdict = {}    #[0, 0, 0, 0, 0, 0, 0]
	minorgctimedict = {}
	majorgctimedict = {}
	thread = ['1', '2', '4', '8', '16', '32', '48']
	for root, dirs, files in os.walk(sys.argv[1]):
		f = [os.path.join(root, fs) for fs in files]
		for filename in f:
			(minorgc, majorgc, minortime, majortime) = helper(filename)
			name = (filename.split('_')[-2]).split('/')[-1]
			threadid = filename.split('_')[-1]
			index = thread.index(threadid)
			if not name in minorgcdict:
				minorgcdict[name] = [0, 0, 0, 0, 0, 0, 0]
				majorgcdict[name] = [0, 0, 0, 0, 0, 0, 0]
				minorgctimedict[name] = [0, 0, 0, 0, 0, 0, 0]
				majorgctimedict[name] = [0, 0, 0, 0, 0, 0, 0]
			minorgcdict[name][index] = minorgc
			majorgcdict[name][index] = majorgc
			minorgctimedict[name][index] = minortime
			majorgctimedict[name][index] = majortime
	for name in minorgcdict:
		print name
		print "\t Minor GC freq: " + str(minorgcdict[name])
		print "\t Major GC freq: " + str(majorgcdict[name])
		print "\t Minor GC time: " + str(minorgctimedict[name])
		print "\t Major GC time: " + str(majorgctimedict[name])
		print "-------------------------------------------------------------------------------------------------"
