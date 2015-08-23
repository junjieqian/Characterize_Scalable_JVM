#!/usr/bin/env Python

import string
import sys
from pkg import ObjectsLife
from pyro import Plot 

def helper():
  print "Usage: python main.py file-name option"
  print "file-name, Elephant track log file name or the file path"
  print "options: "
  print "  0, trace-file input format"
  print "  1, Object life time \n  objectlife, plot the objectlife information \n  objectallocation, plot the object allocated rate information"
  print "Benchmark name"
  print "Example: python ../../ET_logs/main.py objectallocation/ objectallocation scalac"

def main():
  try:
    script, filename, option, name = sys.argv
  except:
    helper()
    sys.exit()
  if option == '0':
    print "shared objects number: ", SharedObjects.SharedObjects(filename)
  elif option == '1':
    ObjectsLife.ObjectsLife(filename)
  elif option == "objectlife":
    Plot.plot(filename, "objectlife", name)
  elif option == "objectallocation":
    Plot.plot(filename, "objectallocation", name)


if __name__ == "__main__":
  main()
