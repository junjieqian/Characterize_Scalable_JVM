#!/usr/bin/python

# to count how many locks involves with gc, the heap reference thread can be count as gc/jvm thread

import sys
import string
import matplotlib.pyplot as plt
import os

def helper(filename):
	fp = open(filename)
	monitor = {}
	enter = 0
	entered = 0
	exit = 0
	for line in fp:
		if line.find("Reference Handler") >= 0:
			if line.find("enter monitor") >= 0:
				enter += 1
			elif line.find("entered monitor") >= 0:
				entered += 1
			elif line.find("exit monitor") >= 0:
				exit += 1
	fp.close()
	return max(enter, entered, exit)

markerlist = ['o', '^', '*', 'D', '+', 's', 'p', '>', '<', '1', 'h', 'x', '2', '3', '4', 'd', '|']

def plot(indict):
	i = -1
	list2 = ['2', '4', '8', '16', '32', '48']
	for name in indict:
		i += 1
		ylist = []
		ylist = indict[name]
		plt.figure(0)
		plt.plot(range(len(ylist)), ylist, color= "#000000", marker=markerlist[i], label=name)
		plt.savefig("Lock_inGC.pdf", format="pdf", bbox_inches="tight")
	plt.figure(0)
	plt.xticks(range(len(list2)), list2)
	plt.xlabel("Thread number")
	plt.legend(loc="upper center", ncol=5, prop={'size':10})
	plt.savefig("Lock_inGC.pdf", format="pdf", bbox_inches="tight")
	plt.cla()

if __name__ == "__main__":
	if len(sys.argv) < 2:
		sys.exit("%prog +  filename")
	threadlist = ['2', '4', '8', '16', '32', '48']
	gcdict = {}
	for root, dirs, files in os.walk(sys.argv[1]):
		f = [os.path.join(root, fs) for fs in files]
		for filename in f:
			gclock = helper(filename)
			name = filename.split('_')[0]
			try:
				name = name.split('/')[-1]
			except:
				pass
			print name
			threadnum = filename.split('_')[1]
			index = threadlist.index(threadnum)
			if not name in gcdict:
				gcdict[name] = [0,0,0,0,0,0]
			gcdict[name][index] = gclock
	plot(gcdict)
