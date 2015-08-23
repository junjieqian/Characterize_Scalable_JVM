#!/usr/bin/env python

import string
import sys
import os
import math
import numpy as np
#import brewer2mpl

try:
	import matplotlib.pyplot as plt
except:
	sys.exit("No plot library")

#colorlist = ['b', 'r', 'g', 'c', 'm', 'y', 'k', 'm', 'b', 'r', 'g', 'c', 'k', 'g', 'b']
#colorlist = plt.get_cmap('jet', 20)(np.linspace(0, 1.0, 20))
#colorlist = brewer2mpl.get_map('Set2', 'Qualitative', 8).mpl_colors
colorlist = [ '#bd2309', '#bbb12d', '#1480fa', '#14fa2f', '#000000', '#faf214', '#2edfea', '#ea2ec4', '#ea2e40', '#cdcdcd', '#577a4d', '#2e46c0', '#f59422', '#219774', '#8086d9']
#print colorlist
makerlist = ['o', '^', '*', 'D', '+', 's', 'p', '>', '<', '1', 'h', 'x', '2', '3', '4', 'd', '|']

makerlist1 = ['o-', '^-', '*-', 'D-', '+-', 's-', 'p-', '>-', '<-', '1-', 'h-', 'x-', '2-', '3-', '4-', 'd-', '|-']
makerlist2 = ['o.', '^.', '*.', 'D.', '+.', 's.', 'p.', '>.', '<.', '1.', 'h.', 'x.', '2.', '3.', '4.', 'd.', '|.']

def helper():
	print "usage: %prog log-dir \n\t\tlog file path needed\n"
	exit()

def logread(filename):
	fopen = open(filename, 'r')
	monitor_hold = {}
	monitor_wait = {}  # wait for lock, key should be monitorid+threadid
	total_contention_time = 0
	total_contention_list = []

	contend_time = []  # record the time dimension
	contend_freq = []  # record the frequency
	wait_time = []     # record time spent on waiting for monitors
	lock_time = []
	lock_freq = []

	run_contend_time = [0]
	run_contend_freq = [0]
	run_wait_time = [0]
	run_lock_time = [0]
	run_lock_freq = [0]
	for line in fopen:
		if line.find("monitor ") >= 0:
			word = line.split()
			threadid  = word[0].split(':')[0]
			monitorid = word[4]
			if word.count(':') > 1:
				timestamp_index = word.index(':', word.index(':')+1) + 1
			else:
				timestamp_index = word.index(':') + 1
			try:
				timestamp = float(word[timestamp_index])/1000000
			except:
				sys.exit(line)
			'''
			if line.find("Reference Handler") >=0 or line.find("Refresh Packages")== 0:
				timestamp = int(word[7])/1000000
			elif line.find("Unzip workspace Refresh Packages") == 0:
				timestamp = int(word[9])/1000000
			elif line.find("Framework Event Dispatcher") >= 0:
				timestamp = int(word[8])/1000000
			else:
				try:
					timestamp = int(word[6])/1000000
				except:
					sys.exit(line)
			'''

		if line.find("enter monitor") >= 0:
			keystr = monitorid+threadid
			if monitorid in monitor_hold: # contention happens here
				run_contend_time.append(timestamp)
				run_contend_freq.append(run_contend_freq[-1]+1)
			monitor_wait[keystr] = timestamp

		elif line.find("entered monitor") >= 0:
			keystr = monitorid+threadid
			if keystr in monitor_wait: # finish waiting, enter the monitor
				waittime = abs(timestamp - monitor_wait[keystr])
				total_contention_time += waittime
				if waittime > 1: # thread wait more than expected for this monitor
					# find the right space to insert this contention
					index = -1
					for element in run_contend_time:
						if element > monitor_wait[keystr]:
							index = run_contend_time.index(element)
							break
					if index > 0: 
					# insert this contention into middle of the time list, and update all following events
						run_contend_time.insert(index, monitor_wait[keystr])
						run_contend_freq.insert(index, run_contend_freq[index])
						for i in range(index+1, len(run_contend_freq)):
							run_contend_freq[i] += 1
					else:
						run_contend_time.append(monitor_wait[keystr])
						run_contend_freq.append(run_contend_freq[-1]+1)
				del monitor_wait[keystr]
			monitor_hold[monitorid] = threadid # hold the monitor
			run_lock_time.append(timestamp)
			run_lock_freq.append(run_lock_freq[-1]+1)

		elif line.find("exit monitor") >= 0:
			if monitorid in monitor_hold:
				del monitor_hold[monitorid]

		elif line.find("END of hotspot monitors tracing at") >= 0:
			word = line.split()
			endtime = float(word[6])/1000000
			steptime = endtime/1000 # divide the period into 1000 pieces
			j = 0
			k = 0
			contend_freq.append([])
			contend_time.append([])
			lock_time.append([])
			lock_freq.append([])
			for i in range(1, 1001):
				if len(contend_freq[-1]) == 0:
					contend_freq[-1].append(0)
				else:
					contend_freq[-1].append(contend_freq[-1][-1])
				contend_time[-1].append(i*steptime)
				if j < len(run_contend_freq):
					while run_contend_time[j] < i*steptime:
						contend_freq[-1][-1] = run_contend_freq[j]
						j += 1
						if j >= len(run_contend_freq):
							break
				if len(lock_freq[-1]) == 0:
					lock_freq[-1].append(0)
				else:
					lock_freq[-1].append(lock_freq[-1][-1])
				lock_time[-1].append(i*steptime)
				if k < len(run_lock_freq):
					while run_lock_time[k] < i*steptime:
						lock_freq[-1][-1] = run_lock_freq[k]
						k += 1
						if k >= len(run_lock_freq):
							break
			while len(contend_freq[-1]) < len(contend_time[-1]):
				contend_freq[-1].append(contend_freq[-1][-1])
			while len(lock_freq[-1]) < len(lock_time[-1]):
				lock_freq[-1].append(lock_freq[-1][-1])
			run_lock_time = [0]
			run_lock_freq = [0]
			run_contend_time = [0]
			run_contend_freq = [0]
			total_contention_list.append(total_contention_time)
			total_contention_time = 0

	fopen.close()
	contend_time1 = normiliaze(contend_time)
	contend_freq1 = normiliaze(contend_freq)
	lock_time1 = normiliaze(lock_time)
	lock_freq1 = normiliaze(lock_freq)
	return (contend_time1, contend_freq1, lock_time1, lock_freq1, total_contention_list)

def normiliaze(inlist):
	''' transform the list of results to average run results
	'''
	outlist = []
	for i in range(len(inlist[0])):
		element = 0.0
		for item in inlist:
			element += item[i]
		element = math.ceil(float(element)/float(len(inlist)))
		outlist.append(element)
	return outlist

def compare(dict1):
	for i in dict1:
		if dict1[i][0] != 0:
			val = dict1[i][0]
			for j in range(len(dict1[i])):
				dict1[i][j] = float(float(dict1[i][j])/float(val))
	return dict1

def logbase(list1):
	outlist = []
	for element in list1:
		if element > 0:
			outlist.append(math.log10(element))
		else:
			outlist.append(0.0)
#			sys.exit("Error"+ str(element))
	return outlist

def thread_plot(*args):
	''' one certain thread, put all benchmarks together
	thread_plot(lockdict, locktimedict. lock)
	'''
	dict1 = args[0]
	dict2 = args[1]
	plotname = args[2]
	base = int(args[3])
	i = 0  # list index for values in dict
	threadlist = [2, 4, 8, 16, 32, 48]
	for i in range(6):
		xlist1 = []
		ylist1 = []
		namelist = []
		j = -1
		for name in dict1:
			j += 1
			namelist.append(name)
			ylist1 = logbase(dict1[name][i])
			xlist1 = dict2[name][i]
			plt.figure(i+base)
#			plt.plot(xlist1, ylist1, colorlist[j], label=name)
			plt.plot(range(1000), ylist1, color=colorlist[j])
			markers_on = range(0, 1000, 100)
			plt.plot([range(1000)[tempi] for tempi in markers_on], [ylist1[tempj] for tempj in markers_on], color=colorlist[j], linestyle='None', marker=makerlist[j], label=name)
			plt.savefig(plotname+str(threadlist[i]), format='pdf', dpi=900, bbox_inches='tight')
#			plt.savefig(plotname+str(threadlist[i]))
		plt.figure(i+base)
		plt.title(plotname+str(threadlist[i]))
		plt.xlabel("Execution time")
#		plt.ylabel()
#		plt.legend(bbox_to_anchor=(0., 1.02, 1., .14),loc=10, ncol=6, prop={'size':7}, mode="expand", borderaxespad=0.)
		plt.legend(loc="lower right", prop={'size': 7}, ncol=2)
		plt.savefig(plotname+str(threadlist[i]), format='pdf', dpi=900, bbox_inches='tight')
#		plt.savefig(plotname+str(threadlist[i]))
		plt.cla()

def name_plot(*args):
	''' plot for same benchmarks with different thread number
	'''
	dict1 = args[0]
	dict2 = args[1]
	plotname = args[2]
	base = int(args[3])
	j = -1
	threadlist = [2, 4, 8, 16, 32, 48]
	for name in dict1:
		j += 1 # plt.plot
		xlist1 = []
		ylist2 = []
		for i in range(6):
			ylist1 = dict1[name][i]
			xlist1 = dict2[name][i]
			plt.figure(j+base)
			plt.plot(xlist1, ylist1, color=colorlist[i])
			markers_on = range(0, len(xlist1), 100)
			plt.plot([xlist1[tempi] for tempi in markers_on], [ylist1[tempj] for tempj in markers_on], color=colorlist[i], linestyle='None', marker=makerlist[i],label=(str(threadlist[i])+"-thread"))
			plt.savefig(plotname + name +".pdf", format="pdf", bbox_inches='tight')
		plt.figure(j+base)
		plt.title(plotname+name)
		plt.xlabel("Execution time divided into 1000 pieces")
		plt.ylabel("log10(total number)")
		plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1.05), ncol=7, prop={'size':7})
#		plt.legend(bbox_to_anchor=(0.,1/02, 1., .14), loc=10, ncol=6, prop={'size':7}, mode="expand", borderaxespad=0.)
		plt.savefig(plotname + name + ".pdf", format="pdf", bbox_inches='tight')
		plt.cla()

def contentionplot(dict1, plotname):
	list1 = []
	list2 = ['2', '4', '8', '16', '32', '48']
	namelist = []
	i = -1
	for name in dict1:
		i += 1
		list1 = logbase(dict1[name])
		plt.figure(0)
		plt.plot(list1, color=colorlist[i], marker=makerlist[i],label=name)
		plt.xticks(range(len(list2)), list2)
#		plt.ylim([1.5, 5.5])
		plt.savefig(plotname+".pdf", format="pdf", dpi=600, bbox_inches='tight')
	plt.figure(0)
#	plt.title("Time on contentions")
	plt.xlabel("Thread number")
	plt.ylabel("log10(total time)")
#	plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1.05), ncol=7, prop={'size':10})
	plt.legend(loc="upper center", ncol=6)
	plt.savefig(plotname+".pdf", format="pdf", dpi=600, bbox_inches='tight')
	plt.cla()

def lockplot(*args):
	indict = args[0]
	argument = args[1]
	list1 = []
	list2 = ['2', '4', '8', '16', '32', '48']
	namelist = []
	i = -1
	for name in indict:
		i += 1
		list1 = []
		for item in indict[name]:
			list1.append(item[-1])
		base = list1[0]
#		for j in range(len(list1)):
#			list1[j] = float(list1[j]/base)
		plt.figure(0)
		plt.plot(list1, color=colorlist[i], marker=makerlist[i], label=name)
#		plt.ylim([2.0, 5.5])
		plt.xticks(range(len(list2)), list2)
		plt.savefig(argument+".pdf", format="pdf", dpi=600, bbox_inches='tight')
	plt.figure(0)
	plt.xlabel("Thread number")
	if argument == "Contention_Lock_fraction":
		plt.xlabel("Fraction of contentions in locks")
	else:
		plt.xlabel("Number of locks")
#	plt.ylabel("log10(number)")
#	plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1.05), ncol=7, prop={'size':10})
	plt.legend(loc="upper center", ncol=6, prop={'size':10})
	plt.savefig(argument+".pdf", format="pdf", dpi=600, bbox_inches='tight')
	plt.cla()

def dividelist(list1, list2):
	list3 = []
	for i in range(len(list1)):
		if list2[i] == 0:
			list3.append(0)
			continue
		list3.append(float(list1[i]/list2[i]))
	return list3

if __name__ == '__main__':
	try:
		script, filepath = sys.argv
	except:
		helper()

	lockdict = {}
	locktimedict = {}
	contenddict = {}
	contendtimedict = {}
	contentiondict= {}
	threadlist = [2, 4, 8, 16, 32, 48]
	if not os.path.isfile(filepath):
		for root,dirs,files in os.walk(filepath):
			flist = [os.path.join(root, fs) for fs in files]
			flist.sort(key=lambda x: x.split('_')[0])
			for fp in flist:
				(contend_time, contend_freq, lock_time, lock_freq, total_contention_list) = logread(fp)
				filename  = fp.split('_')[0]
				try:
					filename = filename.split('/')[-1]
				except:
					pass
				print filename
				threadnum = int(fp.split('_')[1])
				index = threadlist.index(threadnum)
				if not filename in lockdict:
					lockdict[filename] = [[], [], [], [], [], []]
					locktimedict[filename] = [[], [], [], [], [], []]
					contenddict[filename] = [[], [], [], [], [], []]
					contendtimedict[filename] = [[], [], [], [], [], []]
					contentiondict[filename] = [0,0,0,0,0,0]
				lockdict[filename][index] = lock_freq
				locktimedict[filename][index] = lock_time
				contenddict[filename][index] = dividelist(contend_freq, lock_freq)
#				contenddict[filename][index] = contend_freq
				contendtimedict[filename][index] = contend_time
				contentiondict[filename][index] = float(float(sum(total_contention_list))/float(len(total_contention_list)))
#	contentionplot(contentiondict, "Total_contention_time")
#	thread_plot(lockdict, locktimedict, "Lock_number_ThreadCount_", 0)
#	thread_plot(contenddict, contendtimedict, "Contention_number_ThreadCount_", 10)
#	name_plot(lockdict, locktimedict, "Lock_number_Benchmark_", 20)
#	name_plot(contenddict, contendtimedict, "Contention_number_Benchmark_", 30)
	lockplot(lockdict, "Lock_number")
	lockplot(contenddict, "Contention_Lock_fraction")
#	lockplot(contenddict, "Contention_number")

