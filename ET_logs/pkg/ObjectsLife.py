#!/usr/bin/env Python

import sys
import string
#import matplotlib.pyplot as plt

def ObjectsLife(filename):
  """ function, calculate the objects' lifetime
    get how many objects have been allocated during one objects' life, 1. size. 2. GC
    @param liveobjects, dict to store current alive objects with the heap size when first allocated
    @param deadobjects, dict to store the objects with the heap size allocated during its life time
    @param objectnumber, list to store the number of objects alive when allocated certain number of heap sizes
    @param currentsize, the total heap size has been allocated
    @param objectid, the object-id
    @param objectsize, the object-size in bytes
  """
  fp = open(filename, 'r')
  numbername = "object_number_heap_allocation.csv"
  fw1 = open(numbername, 'w')
  fw1.write("heap size, live objects number \n")
  objectlifename = "object_life.csv"
  fw2 = open(objectlifename, 'w')
  fw2.write("object id, object life time \n")
  liveobjects  = {}
  objectnumber = []
  currentsize  = 0
  heapsizelist = []
  prevsize     = 0
  totalobjects = 0
  for line in fp:
    if line.startswith('A '):       # this is start of one objects' life
      word = line.split(' ')
      objectid = str(word[1])
      objectsize = int(word[2], 16)
      liveobjects[objectid] = currentsize
      currentsize += objectsize
      totalobjects += 1
    elif line.startswith('R '):     # Not sure which this is, but it needs to be included
      word = line.split(' ')
      objectid = word[1]
      if not (objectid in liveobjects):
        liveobjects[objectid] = currentsize
    elif line.startswith('D '):     # this is end of one objects' life
      word = line.split(' ')
      objectid = word[1].split('\n')[0]
      if objectid in liveobjects:
        ll = "0x" + str(objectid) + ", " + str(currentsize - liveobjects[objectid]) + '\n'
        fw2.write(ll)
        del liveobjects[objectid]
      else:
        print objectid, "is dead without allocated"
    if currentsize - prevsize >= 1000:
#      objectnumber.append(len(liveobjects))
#      heapsizelist.append(currentsize)
      l = str(currentsize) + ", " + str(len(liveobjects)) + '\n'
      fw1.write(l)
      prevsize = currentsize
  fp.close()
  fw1.close()
  if len(liveobjects) > 0:
    for key in liveobjects:
      ll = "0x" + str(objectid) + ", " + str(currentsize - liveobjects[objectid]) + '\n'
      fw2.write(ll)
  fw2.close()
