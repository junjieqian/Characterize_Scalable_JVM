#!/usr/bin/env python
# logs gc efficiecny process

import string
import sys
import os
import numpy as np
import write_to_file

def log_file_process(filename):
	''' log_file_process function, to collect GC efficiency
	@param size_list, the average size change for each GC
	@param time_list, the time used for each GC
	@param before, the memory size before GC happens
	@param after, the memory size after GC happens
	@param time, the time spent for the GC
	@param gc_size_list, the size change for GC during on run
	'''
	fp = open(filename, 'r')
	size_list = []
	time_list = []
	gc_size_list = []
	gc_time_list = []
#	print filename
	for line in fp:
		if line.find("[GC ") >= 0:
			word = line.split("->")
#			print (word[0].split('  '))
			before = int((word[0].split('  '))[1].split("KB")[0])
			after = int((word[1].split("KB"))[0])
			time = float(word[1].split(' ')[-2])
			gc_time_list.append(time)
			gc_size_list.append(before-after)
		elif line.find("%%%%%%%%%%%%") >= 0:
			size_list.append(np.mean(gc_size_list))
			time_list.append(np.mean(gc_time_list))
			del gc_time_list[:]
			del gc_size_list[:]
	return (size_list, time_list)

def log_path_process(filepath):
	''' log_path_process function, to collect GC efficiency for one directories
	@param fnames, the log names with path
	@param size_list, the average size change for each GC
	@param time_list, the time used for each GC
	'''
	time_list = []
	size_list = []
	for root, dirs, files in os.walk(filepath):
		fnames = [os.path.join(root, f) for f in files]
		for filename in fnames:
			(size_list, time_list) = log_file_process(filename)
			resultname = filename + "_result"
			size_list = write_to_file.writetofile(size_list, resultname)
			time_list = write_to_file.writetofile(time_list, resultname)
