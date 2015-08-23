# !/bin/env/python
# gc-trace.py

import string
import os
import sys
from sys import argv
from pyheatmap.heatmap import HeatMap
import matplotlib.pyplot as plt
import numpy as np

class g:
  biaslist = []
  maturelist = []

def getnames():
  try:
    script, tracename, resultname = argv
  except:
    sys.exit("Usage: python gc-trace.py trace-file-name result-file-name")

  return (tracename, resultname)

def readin(tracename):
  fp              = open(tracename, 'r')
  addrlist        = []  # used to store the addr list, indexed by different GC
  intersizelist   = []  # used to store the inter size of different addr
  tempsizelist    = []  # used to temp store inter size during each GC
  sizedict        = {}  # used to store last occur max size
  indexdict       = {}  # used to store the index in list
  templist        = []  # used to store addr list during each GC
  g.biglist       = []  # used to store the big inter arrival size occurence
  g.maturelist    = []  # used to store the mature objects # in each GC
  maxaddr         = 0
  idx             = 0
  mature          = 0
  big             = 0

  for line in fp:
    rw=1
    if line.find("GC")>0:  # this is one GC info, reset all elements
      addrlist.append(templist)
      intersizelist.append(tempsizelist)
      g.biglist.append(big)
      g.maturelist.append(mature)
      tempsizelist = []
      templist     = []
      sizedict     = {}
      indexdict    = {}
      maxaddr      = 0
      idx          = 0
      big          = 0
      mature       = 0

    else:
      try:
        word=line.split(" ")
        if word[2]=='R\n':
          rw=-1
        addr=int(word[0], 0)
        #addr *= rw
        templist.append(addr)
        if (abs(addr)>maxaddr) and (abs(addr)>=int(0xa4c00000,0)) and (abs(addr)<=int(0xafffffff, 0)):  # update the max addr in heap young generation
          maxaddr     = abs(addr)
        # if it happens once, record the passed memory size
        # update the sizedict
        if (abs(addr)>=int(0xa4c00000, 0)) and (abs(addr)<=int(0xafffffff, 0)):
          if addr in sizedict:
            lastmaxaddr      = sizedict[addr]
            sizedict[addr]   = maxaddr
            index            = indexdict[addr]
            tempsizelist[index].append(maxaddr-lastmaxaddr)
            if (maxaddr-lastmaxaddr)>=8388608:
              big     += 1
          else:
          #  print addr
            sizedict[addr]   = maxaddr
            idx       += 1;
            tempsizelist.append([0])
            indexdict[addr]  = idx
        elif (abs(addr)>int(0x6fffffff, 0)):
          mature += 1

      except:
        pass

  print "Trace file finished"
  fp.close()
  return (addrlist, intersizelist)

def heatplot(addrlist, resultname):
  hm = HeatMap(addrlist)
  hm.heatmap(save_as=resultname)

def plot(addrlist, resultname):
  i = 211

  plt.figure(1)
  plt.subplot(211)
  element = addrlist[0]
  t = np.arange(0, len(element), 1)
  plt.plot(t, element, '.')
  plt.subplot(212)
  element = addrlist[1]
  t = np.arange(0, len(element), 1)
  plt.plot(t, element, '.')
  plt.subplot(213)
  element = addrlist[2]
  t = np.arange(0, len(element), 1)
  plt.plot(t, element, '.')
  plt.savefig(resultname)

def main():
  (tracename,resultname)     = getnames()
  addrlist                   = []
  intersizelist              = []
  (addrlist, intersizelist)  = readin(tracename)
  heatplot(addrlist, resultname)
  print g.biglist, g.maturelist

if __name__ == '__main__':
  main()
