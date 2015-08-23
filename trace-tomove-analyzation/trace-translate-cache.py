# !/bin/env/python
# trace-translate-cache.py

import sys
import string
from sys import argv

def main():
    try:
        script, filename, retname=argv
    except:
        sys.exit("USAGE: python trace-translate-cache.py source-trace-file-name result-cache-input-file-name\n")

    fp=open(filename, 'r')
    fw=open(retname, 'w')
    i=0
    for line in fp:
        word=line.split(" ")
        try:
            rwint=int(word[0])
            rw=str(rwint)
            addr1=int(word[1], 0)
            addr2=hex(addr1)
            addr=str(addr2)
            fw.write(rw)
            fw.write(' ')
            fw.write(addr)
            fw.write('\n')
        except:
            i+=1
    fp.close()
    fw.close()
    print i

if __name__=='__main__':
    main()
