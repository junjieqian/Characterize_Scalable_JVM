#!/usr/bin/python

#Java-xalan:0.0458583536487,0.00267890684726,0.00358446919256,0.00358483086453,0.00358515740667,0.00268356182735,0.00358819955599,0.00358436894452,0.00269242845484,0.000897246787705,0.171662331709,0.183442171293,0.572157973468,

import string
import sys
import matplotlib.pyplot as plt

colorlist = [ '#bd2309', '#bbb12d', '#1480fa', '#14fa2f', '#000000', '#faf214', '#2edfea', '#ea2ec4', '#ea2e40', '#cdcdcd', '#577a4d', '#2e46c0', '#f59422', '#219774', '#8086d9']

def plot(*args):
	inlist = args[0]
	name   = args[1]
	list1  = []
	list2  = ['1', '2', '4', '8', '16', '32', '48']
	maxlength = 0
	for i in inlist:
		if len(i) > maxlength:
			maxlength = len(i)
	list3  = []
	for i in range(maxlength):
		list1.append([])
		list3.append([])
		for j in range(len(inlist)):
			if i < len(inlist[j]):
				list1[i].append(inlist[j][i])
			else:
				list1[i].append(0.0)
			if i == 0:  # the first one
				list3[i].append(0.0)
			else:
				list3[i].append(list3[i-1][j] + list1[i-1][j])
	plt.figure(0)
	i = 0
	for n in range(len(list1)):
		if i >= len(colorlist):
			i = 0
		plt.bar(range(len(list1[n])), list1[n], bottom=list3[n], color=colorlist[i])
		i += 1
	plt.xlabel("Thread number")
	plt.ylabel("Fractions of threads' execution time in total")
        plt.ylim(0, 1)
	plt.xticks(range(len(list2)), list2)
	plt.title(name)
	plt.savefig(name)

#color2list = ['#000000', '#a9a9a9', '#696969', '#808080', '#d3d3d3', '#f5f5f5']
color2list = ['#a9a9a9', '#f5f5f5']
hatchlist = ['\\', '/']
def plot2(*args):
	inlist0 = args[0]
	name    = args[1]
	inlist1 = args[2]
	list1   = []
	list2   = ['1', '2', '4', '8', '16', '32', '48']
	maxlength = 0
	timelist = []
	gctid = '0'
	timelistindex = -1
	for i in inlist0:
		timelist.append([])
		timelistindex += 1
		i[gctid] = 0
		for j in range(len(inlist1[timelistindex])):
			if inlist1[timelistindex][j] in i:
				i[gctid] += i[inlist1[timelistindex][j]]
				i.pop(inlist1[timelistindex][j], None)
		for element in i:
			if element != gctid:
				timelist[timelistindex].append(float(i[element]))
		timelist[timelistindex].append(float(i[gctid]))
		timelist[timelistindex].sort(reverse=True)
	for ii in timelist:
		if len(ii)>maxlength:
			maxlength = len(ii)
	list3 = []
	for i in range(maxlength):
		list1.append([])
		list3.append([])
		for j in range(len(timelist)):
			if i < len(timelist[j]):
				list1[i].append(timelist[j][i])
			else:
				list1[i].append(0.0)
			if i==0:
				list3[i].append(0.0)
			else:
				list3[i].append(list3[i-1][j] + list1[i-1][j])
	plt.figure(0)
	i = 0
	for n in range(len(list1)-1):
		if i>=len(color2list):
			i = 0
		plt.bar(range(len(list1[n])), list1[n], bottom=list3[n], color=color2list[i], hatch=hatchlist[i], edgecolor='black')
		i += 1
#	plt.bar(range(len(list1[-1])), list1[-1], bottom=list3[-1], color="#ffffff", hatch="/", edgecolor='black', label="GC")
	plt.xlabel("Processor core number change")
	plt.ylabel("Fractions of threads' execution time in total")
        plt.ylim(0,1)
	plt.xticks(range(len(list2)), list2)
#	plt.legend(loc="upper right")
	plt.title(name)
	plt.savefig(name+"_threadtime.pdf", format="pdf", dpi=900, bbox_inches='tight')

def main():
	if len(sys.argv) < 3:
		sys.exit("Usage: %prog results dumpfiles")
	
	fp = open(sys.argv[1], "r")
	fdump = open(sys.argv[2])
	result = {}
	for line in fp:
		word = line.split('==')
		name = word[0]
		if not name in result:
			result[name] = [{}, {}, {}, {}, {}, {}, {}]
		data = word[1].split(',')
		for i in range(7):
			if len(result[name][i]) == 0:
				for j in range(len(data)-1):
					result[name][i][data[j].split(':')[0]] = float(data[j].split(':')[1])
#				result[name][i] = sorted(result[name][i].items(), key=lambda x: x[1], reverse=True)
				break
	gctid = []
	for line in fdump:
		if line.find("2014-0") >=0:
			gctid.append([])
		if line.find("GC task thread")>=0:
			word = line.split()
			gctid[-1].append(str(int(word[-2].split('=')[1], 0))) #nid
	for name in result:
		plot2(result[name], name, gctid)

if __name__ == "__main__":
	main()
