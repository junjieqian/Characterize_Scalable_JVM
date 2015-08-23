# gc-distribution.py
# using this to verify the access patern of objects arount each gc

import string
import sys
import math
import numpy as np
from sys import argv
import matplotlib.pyplot as plt

class g:
    figname='gc_plot_'
    bootname='boot_plot_'
    rationame='ratio_plot_'
    disname='dis_plot_'
    cnt=0
    figcnt=0

def printlist(list1, list2):
    plt.figure(g.figcnt)
    n=len(list1)
    if n>0:
        print 'length of the addrlist is: ', n
        p=np.arange(n)
        plt.plot(p, list1, 'bs')
        plt.plot(p, list2, 'g^')
#        plt.axis([0, p])
        plt.title("Access distribution during GC")
        plt.xlabel("GC range")
        plt.ylabel("Object address")

        plt.savefig((g.figname)+str(g.cnt))
        g.figcnt+=1

def printinfo(inlist):
    plt.figure(g.figcnt)
    n=len(inlist)
    if n>0:
        print 'length of the inlist is: ', n
        p=np.arange(n)
        plt.plot(p, inlist, 'k.')
        plt.title("Boot Gen accesses during GC")
        plt.xlabel("GC range")
        plt.ylabel("Object address")

        plt.savefig((g.bootname)+str(g.cnt))
        g.figcnt+=1

def printratio(inlist):
    plt.figure(g.figcnt)
    n=len(inlist)
    if n>0:
#        print 'length of the inlist is: ', n
        p=np.arange(n)
        plt.plot(p,inlist,'k.')
        plt.title("Ratio of Nursery:NoNursery accesses during GC")
        plt.xlabel("GC range")
        plt.ylabel("Ratio changes")
        plt.savefig((g.rationame)+str(g.cnt))
        g.figcnt+=1

def printdistribution(inlist):
    plt.figure(g.figcnt)
    n=len(inlist)
    nums1=[]
    nums2=[]
    nums3=[]
    l1cnt=0
    l2cnt=0
    l3cnt=0
    l4cnt=0
    if n>0:
        for i in range(1, 20):
            l1cnt=0
            l2cnt=0
            l3cnt=0
            l4cnt=0
            lcnt=0
            for j in range(0, n):
                try:
                    if int(inlist[j][i])<=32768:
                        l1cnt+=1
                    elif int(inlist[j][i])<=262144:
                        l2cnt+=1
                    elif int(inlist[j][i])<=8388608:
                        l3cnt+=1
                    elif int(inlist[j][i])>=8388608:
                        l4cnt+=1
                except:
                    pass
            lcnt=l1cnt+l2cnt+l3cnt+l4cnt
            if lcnt==0:
                break;
#            nums1.append(float(float(l1cnt)/float(lcnt)))
#            nums2.append(float(float(l1cnt+l2cnt)/float(lcnt)))
            nums3.append(float(float(l4cnt)/float(lcnt)))
            print l4cnt, ' and ', lcnt, ' and ', i
        ind=np.arange(len(nums3))
#        p1=plt.plot(ind, nums1, 'k^')
#        p2=plt.plot(ind, nums2, 'bs')
        p3=plt.plot(ind, nums3, 'r-')
        plt.title("Distribution of BIAS accesses in objects' lifetime in Nursery")
        plt.xlabel("Access indexes of individual object")
        plt.ylabel("Proportion of different Inter-size between accesses")
#        plt.legend((p1[0],p2[0],p3[0]), ('<32k', '32k-256k', '>256k'), loc='upper center')
#        plt.legend((p3[0]), ('<8m'), loc='upper center')
        plt.savefig((g.disname)+str(g.cnt))
        g.figcnt+=1
        fa=open("tempfileintersize", 'w')
        for item in inlist:
            print >>fa, item
        fa.close() 

def main():
    try:
        script, filename=argv
    except:
        sys.exit("USAGE: python gc-prefetch-verify.py trace-file-name")

    fp=open(filename, 'r')
    biaslist=[]         # save the BIAS accesses
    biasdict={}         # save the BIAS objects
    nurserylist=[]      # record the nursery access
    nonurserylist=[]
    ratiolist=[]
    bootlist=[]
    intersizelist=[]    # record the inter size list of each object
    objdict={}          # record the index of object in intersizelist to save finding time
    sizedict={}         # record the newest max size of object last accesses
    boot=0              # record the access # of the boot area objects
    nursery=0           # record the access # of the nursery objects
    nonursery=0         # record the access # of the non-nursery objects
    count=0
    maxaddr=0           # suppose the current highest address in nursery generation of heap
    for line in fp:
        if line.find('GC')>=0:
#            printlist(nurserylist, nonurserylist)
#            printinfo(bootlist)
            printratio(ratiolist)
            printdistribution(intersizelist)
            print "BIAS list access number is: ", len(list(set(biaslist)))
            print "BIAS list object number is: ", len(biasdict)
            print "Total object number is: ", len(objdict)
            print "Nursery accesses is: ", nursery
            print "Nonursery accesses is: ", nonursery
            nursery=0
            boot=0
            count=0
            nonursery=0
            del nurserylist[:]
            del bootlist[:]
            del nonurserylist[:]
            del ratiolist[:]
            del intersizelist[:]
            del biaslist[:]
            biasdict.clear()
            objdict.clear()
            sizedict.clear()
            g.cnt+=1
            maxaddr=0
            print 'GC happens @ ', line
            continue
        try:
            word=line.split(': ')
            rw=word[0]
            address=(word[1].split('\n'))[0]
            addr=int(address, 0)
            if addr<=2460286976 and addr>=2254766080:
                if addr<=2288320512:
                    nursery+=1
                    count+=1
                    if addr>maxaddr:
                        maxaddr=addr
                    if addr in objdict:
                        if abs(sizedict[addr]-maxaddr)>=8388608:
                            biaslist.append(addr)
                            if addr in biasdict:
                                biasdict[addr]+=1
                            else:
                                biasdict[addr]=0
                        index=objdict[addr]
                        intersizelist[index].append(abs(sizedict[addr]-maxaddr))
                        sizedict[addr]=maxaddr
                    else:
                        sizedict[addr]=addr
                        objdict[addr]=len(intersizelist)
                        intersizelist.append([0])
                else:
                    count+=1
                    nonursery+=1
                if count%1000000==0:    #### every 1000 accesses the ratio between two generations
                    ratiolist.append(float(float(nursery)/float(nonursery)))
                    nursery=0
                    nonursery=0
#            count+=1
#            nurserylist.append(nursery)
#            nonurserylist.append(nonursery)
#            if int(addr, 0)
        except:
            pass

#    printlist(nurserylist, nonurserylist)
    printratio(ratiolist)
    printdistribution(intersizelist)
    fp.close()
    print "nursery accesses is: ", nursery
    print "nonursery accesses is: ", nonursery

if __name__=='__main__':
    main()
