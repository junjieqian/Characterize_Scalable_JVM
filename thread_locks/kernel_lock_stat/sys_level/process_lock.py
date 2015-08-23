#!/usr/bin/env Python

import string
import sys
import os
import matplotlib.pyplot as plt
import numpy as np

#threadlist = [1, 2, 4, 8, 16, 32, 48, 64]
threadlist = [1, 2, 4, 8, 16, 32, 48]
corelist   = ['1', '2', '4', '8']
colorlist  = ['bo-', 'r^-', 'g*-', 'cD-', 'm+-', 'ys-', 'kp-', 'm*-', 'b>-', 'r1-', 'gh-', 'cH-', 'mx-', 'y2-', 'k3-', 'm4-', 'bd-', 'r|-', 'g_-', 'cv-']

def helper(filename):
  fp = open(filename, 'r')
  res = 0
  cnt = 1
  for line in fp:
    if line.find("FatLocks: ")>=0 and line.find("of all lock operations"):
      word = (line.split(": ")[1]).split(' ')
      res += int(word[0], 0)
      cnt += 1
  res = res/cnt
  return res

def jproflock(filename):
  fp = open(filename, 'r')
  locks = 0
  cnt = 0 
  for line in fp:
	if line.find("MONITOR") >= 0:
	  locks += 1
	elif line.find("%%%%") >= 0:
	  cnt += 1
  locks = float(float(locks - 5*cnt)/float(cnt))
  return locks

def lockstat(filename):
  fp = open(filename, 'r')
  res = 0.00
  result = 0.0000000000
  cnt = 0 
  locks = 0
  executiontime = 0
  locktime = 0.00
  for line in fp:
    if line.find("%%%%%%%") >= 0:
      executiontime = end - start
      locktime = res*0.001
      result += float(float(locktime)/float(executiontime))
#      result += locktime
      start = 0
      end =0
      res = 0.00
      cnt += 1
    elif line.find("StartTime:::") >= 0:
      start = int(line.split(' ')[1])
    elif line.find("EndTime:::") >= 0:
      end = int(line.split(' ')[1])
    elif line.find(':') >= 0:
      try:
        word = line.split()
        res += float(word[5])
        locks += int(word[2])
      except:
        pass
  result = float(result/float(cnt))
  return result

def plot(*args):
  locklist   = args[0]
  namelist   = args[1]
  coreindex  = args[2]
  core = corelist[coreindex]
  resultfile = "lockchange" + str(core) + ".pdf"
  for i in range(len(namelist)):
    list1 = locklist[i]
    plt.figure(coreindex)
#    plt.plot(threadlist, locklist[i], colorlist[i], label=namelist[i])
    plt.plot(corelist, locklist[i], colorlist[i], label=namelist[i])
    plt.savefig(resultfile, format='pdf', dpi=900)
  plt.figure(coreindex)
#  plt.title("Fatlock change with threads when core number is %s"%str(core))
#  plt.title("System total lock waiting time with cores")
  plt.title("Lock contentions in Java VM")
#threads, core number is %s"%str(core))
  plt.ylabel("Normilized to single core")
  plt.xlabel("Core number")
#  plt.legend(loc="upper left", ncol=3, shadow=True)
  plt.legend(bbox_to_anchor=(0., 1.02, 1., .14),loc=10, ncol=6, prop={'size':7}, mode="expand", borderaxespad=0.)
  plt.savefig(resultfile, format="pdf", dpi=900)

def compare(dict1):
  for i in dict1:
    if not dict1[i][0] == 0:
      val = dict1[i][0]
      for j in range(len(dict1[i])):
        dict1[i][j] = float(float(dict1[i][j])/float(val)) 
  return dict1


def main():
  try:
    script, filepath = sys.argv
  except:
    sys.exit("USAGE: python process_lock.py LOCK_PROFILE_DIR")
  res = {}  #the dict to contain the results
  if os.path.isfile(filepath):
    print filepath, lockstat(filepath)
  else:
    threads = [1, 2, 4, 8, 16, 32, 48]
    for root, dirs, files in os.walk(filepath):
      fnames = [os.path.join(root, f) for f in files]
      for f in fnames:
        info = f.split('-')
#        thread, core, name = info[-1], info[-2], info[-3].split('/')[-1]
        thread, name = info[-1], info[-3]
#        coreindex = cores.index(int(core))
        threadindex = threads.index(int(thread))
        if not name in res:
#          res[name] = [[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]]
          res[name] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
#        res[name][coreindex][threadindex] = helper(f)
#        res[name][coreindex][threadindex] = lockstat(f)
        res[name][threadindex] = lockstat(f)
  res = compare(res)
  for i in res:
    print i, ": "
    print "\t", res[i]
    print "====================================="
  print "DONE"
  """
  for i in range(4):
    namelist = []
    locklist = []
    for name in res:
      namelist.append(name)
      first = res[name][i][0]
      if first > 0.0000000:
        for j in range(len(res[name][i])):
          res[name][i][j] = float(res[name][i][j]/first)
      locklist.append(res[name][i])
#    plot(locklist, namelist, i)
  namelist = []
  locklist = []
  namelist = []
  locklist = []
  for name in res:
    namelist.append(name)
    templist = []
    first = res[name][0]
    for i in range(len(res[name])):
      templist.append(float(float(res[name][i])/float(first)))
#    for i in range(4):
#      first = res[name][i][0]
#      if first> 0.0000:
#        templist.append(float(res[name][i][i]/first))
    locklist.append(templist)
  plot(locklist, namelist, 0)
"""

if __name__ == "__main__":
  main()
