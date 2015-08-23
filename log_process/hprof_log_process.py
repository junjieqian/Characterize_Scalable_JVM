# !/usr/bin/env python

import string
import os
import sys
import re

def file_result_collection(filename):
    fp = open(filename, 'r')
    i = 0
    alive = 0
    allocate = 0
    for line in fp:
        if line.find('SITES END')>=0:
            break
        if i == 1:
            first = re.sub("\s\s+", ' ', line)
            second = first.split('% ')
#	    print second
            third = second[2].split(' ')
            alive += int(third[1])
            allocate += int(third[3])
        if line.find("rank")>=0 and line.find("self")>=0 and line.find("accum")>=0:
            i += 1
    fp.close()
    return (str(alive), str(allocate))

def filename_assign(filepath):
    for roots, dirs, files in os.walk(filepath):
        for filename in files:
            if len(filename.split('-')) < 2:
                continue
            resultfile = filename.split('-')[0]
            count = filename.split('-')[1]
            resultfile += "_result"
            fp = open(resultfile, 'a')
            (alive, allocate) = file_result_collection(filename)
            to_write = str(count) + "-thread: " + alive + " & " + allocate + "\n"
            fp.write(to_write)
#            fp.write(count, "-thread: ", alive, " & ", allocate)
            fp.close()
    print 'done'

def main():
    try:
        script, filepath = sys.argv
    except:
        sys.exit("Error")
    filename_assign(filepath)

if __name__ == '__main__':
    main()
