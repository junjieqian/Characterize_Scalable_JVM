#!/usr/bin/env python
# logs PMU events process

import string
import sys
import os
import numpy as np
import write_to_file

def log_file_process(filename):
	''' log_file_process function, to collect PMU events
	@param time_mu/time_gc/time, the time spent of mutator/gc/total for each run
	@param major_gc/gc, the full heap gcs and total gcs for each run
	@param cycles_mu/cyles_gc, the CPU cycles spent for each run
	@param instructions_mu/instructions_gc, the instructions of mutator/gc for each run
	@param misses_mu/misses_gc, the cache misses of mutator/gc for each run

	one better way would be first identify the index of desired event, then fetch the number next line
	'''
	fp = open(filename, 'r')
	gc = []
	time_mu = []
	time_gc = []
	major_gc = []
	cycles_mu = []
	cycles_gc = []
	instructions_mu = []
	instructions_gc = []
	misses_mu = []
	misses_gc = []
	time = []
	for line in fp:
		if line.find("\t0.00\t") >= 0:
			word = line.split('\t')
			gc.append(word[0])
			time_mu.append(word[1])
			time_gc.append(word[2])
			major_gc.append(word[13])
			cycles_mu.append(word[33])
			cycles_gc.append(word[34])
			instructions_mu.append(word[35])
			instructions_gc.append(word[36])
			misses_mu.append(word[37])
			misses_gc.append(word[38])
		elif line.find("Total time:") >= 0:
			word = line.split(': ')
			time.append(word[1].split(' ')[0])
	return (gc, time_mu, time_gc, major_gc, cycles_mu, cycles_gc, \
		instructions_mu, instructions_gc, misses_mu, misses_gc, time)

def log_path_process(filepath):
	''' log_path_process function, to collect GC efficiency for one directories
	@param fnames, the log names with path
	@param size_list, the average size change for each GC
	@param time_list, the time used for each GC
	'''
	gc = []
	time_mu = []
	time_gc = []
	major_gc = []
	cycles_mu = []
	cycles_gc = []
	instructions_mu = []
	instructions_gc = []
	misses_mu = []
	misses_gc = []
	time = []
	for root, dirs, files in os.walk(filepath):
		fnames = [os.path.join(root, f) for f in files]
		for filename in fnames:
			(gc, time_mu, time_gc, major_gc, cycles_mu, cycles_gc, \
				instructions_mu, instructions_gc, misses_mu, misses_gc, time) \
			= log_file_process(filename)
			resultname = filename + "_result"
			gc = write_to_file.writetofile(gc, resultname)
			time_mu = write_to_file.writetofile(time_mu, resultname)
			time_gc = write_to_file.writetofile(time_gc, resultname)
			major_gc = write_to_file.writetofile(major_gc, resultname)
			cycles_mu = write_to_file.writetofile(cycles_mu, resultname)
			cycles_gc = write_to_file.writetofile(cycles_gc, resultname)
			instructions_mu = write_to_file.writetofile(instructions_mu, resultname)
			instructions_gc = write_to_file.writetofile(instructions_gc, resultname)
			misses_mu = write_to_file.writetofile(misses_mu, resultname)
			misses_gc = write_to_file.writetofile(misses_gc, resultname)
			time = write_to_file.writetofile(time, resultname)
