#!/usr/bin/env python
# write_to_file

import string

def writetofile(inlist, filename):
	fp = open(filename, 'a')
	for element in inlist:
		fp.write("%s, "%str(element))
	fp.write("\n")
	del inlist[:]
	fp.close()
	return inlist
