#!/usr/bin/python

import os
import sys
import string

if __name__ == "__main__":
	for root, dirs, fs in os.walk(sys.argv[1]):
		f = [os.path.join(root, f) for f in fs]
		for filename in f:
			fp = open(filename)
			print filename
			threadlist = []
			for line in fp:
				threadlist.append(line.count(':'))
			print threadlist
			fp.close()
