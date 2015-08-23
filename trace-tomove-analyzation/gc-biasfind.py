# using this file to find out when the first gc happens

import sys
import string
from sys import argv
import matplotlib.pyplot as plt
import numpy as np

class g:
    figname="object"
    i=0

def helpfinfo():
    sys.exit("Usage, python read.py source-file-name")

def printinfo(addrlist):
    plt.figure(1)
    n=len(addrlist)
    print 'length of the addrlist is: ', n
    p=np.arange(n)
    plt.plot(p, addrlist, 'k.')
    plt.axis([0, n, int('0x86650000', 0), int('0x88650000', 0)])
    plt.title("Distribution of BIAS object in Nursery")
    plt.xlabel("Object count")
    plt.ylabel("Object address in Nursery")

    plt.savefig((g.figname)+str(g.i))
    g.i+=1

def main():
    addrlist=[]
    addrdict={}   # save the previous access biggest addr info
  
    try:
        script, filename = argv
    except:
        helpfinfo()

    fp=open(filename, 'r')
    i=0
    gcflag=0
    exeflag=0
    for line in fp:
        if line.find('GC')>=0:
            print 'GC found at: ', i
            if len(addrlist)>0:
                printinfo(addrlist)
            addrlist=[]
            addrdict={}
            maxaddr=int('0x86650000', 0)
        if line.find('=')>=0 and exeflag==0:
            print "Benchmark starts from here, ", i
            addrlist = []
            addrdict = {}
            exeflag==1
#        if line.find('0x8ca5')>=0 or line.find('0x8d4')>=0:
#            print line
        try:
            word=line.split(":")
            addr=int(word[1], 0)

            if addr>=int(str(0x86650000), 0) and addr<=int(str(0x88650000)):
                if addr>maxaddr:
                    maxaddr=addr
                if addr in addrdict:
                    if abs(addrdict[addr]-maxaddr)>=262144:
                        print line
                        addrlist.append(addr)
                    addrdict[addr]=maxaddr
                else:
                    addrdict[addr]=addr
        except:
            pass
        i+=1
    fp.close()
    if len(addrlist)>0:
        printinfo(addrlist)

if __name__=='__main__':
    main()
