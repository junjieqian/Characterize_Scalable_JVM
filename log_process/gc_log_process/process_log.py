#!/usr/bin/env python
# log_processing.py

import sys
import string
import os
from logs import logs_gc_process
from logs import logs_pmu_process
from logs import logs_gc_frequency

def helper():
	print "###################################################################################"
	print "# USAGE: ./log_processing.py log-file-path/file process-option"
	print "#   JVM Log file process options, "
	print "#      0. for logs with gc-verbose get the GC efficiency"
	print "#      1. for logs with PMU info, needs to be in pretty order to fetech the events"
	print "#      2. for logs with gc-verbose, get the Major/Minor GC frequency"
	print "###################################################################################"

def main():
	try:
		script, filename, option = sys.argv
	except:
		helper()
		sys.exit()

	if option == '0':
		if os.path.isfile(filename):
			logs_gc_process.log_file_process(filename)
		else:
			logs_gc_process.log_path_process(filename)
	elif option == '1':
		if os.path.isfile(filename):
			logs_pmu_process.log_file_process(filename)
		else:
			logs_pmu_process.log_path_process(filename)
	elif option == '2':
		if os.path.isfile(filename):
			logs_gc_frequency.log_file_process(filename)
		else:
			logs_gc_frequency.log_path_process(filename)

if __name__ == "__main__":
	main()
