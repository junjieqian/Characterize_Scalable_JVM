# !/usr/bin/env python

import string
import os

def log_file_process(log):
    # function process the log
    # _gc_list, store the average GC number for different thread number
    print "Results for ", log
    fp = open(log, 'r')
    minor_gc_list = []
    major_gc_list = []
    temp_minor = []
    temp_major = []
    minor = 0
    major = 0
    cnt = 0
    for line in fp:
        if line.find("[GC ")>=0:
            minor += 1
        elif line.find("[Full GC")>=0:
            major += 1
        elif line.find("%%%%%%\n")>=0:
            temp_minor.append(minor)
            temp_major.append(major)
            minor = 0
            major = 0
	    cnt += 1
        if cnt==15:
            minor_gc_list.append(float(sum(temp_minor))/15.0)
            major_gc_list.append(float(sum(temp_major))/15.0)
            del temp_minor[:]
            del temp_major[:]
	    cnt = 0
    print "Minor GC happen times: ", minor_gc_list
    print "Major GC happen times: ", major_gc_list, '\n'
    fp.close()

def log_path_process(logpath):
    for roots, dirs, files in os.walk(logpath):
        for f in [os.path.join(roots, fi) for fi in files]:
            log_file_process(f)
