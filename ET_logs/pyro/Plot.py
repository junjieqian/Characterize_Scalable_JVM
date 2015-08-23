#!/usr/bin/env Python

import string
import sys
import matplotlib.pyplot as plt
import os

#def plot(list1, list2):

def helper(value):
  cnt = 0
  while value/2 > 0:
    cnt += 1
    value = value/2
  return cnt

#labels = ['1', '2', '4', '8', '16', '32', '64', '128', '256', '512', '1k', '2k', '4k', '8k', '16k', '32k', '64k', '128k', '256k', '512k', '1m', '2m', '4m', '8m', '16m', '32m', '64m', '128m', '256m', '512m', '1G', '2G', '4G', '8G', '16G', '32G', '64G']
labels = ['1', '', '', '', '', '32', '', '', '', '', '1k', '', '', '', '', '32k', '', '', '', '', '1m', '', '', '', '', '32m', '', '', '', '', '1G', '', '4G', '8G', '16G', '32G', '64G']

def plot(filepath, option, name):
  ''' plot function
    @param list1, the xlabel list
    @param list2, the ylabel list
    @param option, the figure type to plot, including objectlife, objectlive
  '''
  title = ""
  x = ""
  y = ""
  resultfile = ""
  if option == "objectlife" :
#    title = "Change of alive object number with heap allocation"
    x = "Interarrival heap allocation during object's life"
#    y = "Fraction of objects number"
    y = "Cumulative objects number distribution"
    resultfile = name + "_object_life.pdf"
  elif option == "objectallocation" :
#    title = "Change of allocated object number with heap allocation"
    x = "Heap allocation size"
    y = "Allocated objects number"
    resultfile = name + "_object_allocation.pdf"
  if not os.path.isfile(filepath):
    for root, dirs, files in os.walk(filepath):
      fnames = [os.path.join(root, f) for f in files]
      files_sorted = sorted(fnames, key=lambda x: int((x.split('-')[-2]).split('_')[-1]))
      j = 0
      colorlist  = ['bo-', 'r^-', 'g*-', 'cD-', 'm+-', 'ys-', 'kp-']
      alloclist  = ['b', 'r', 'g', 'c', 'm', 'y', 'k']
      alloclist2 = ['bo', 'r^', 'g*', 'cD', 'm+', 'ys', 'kp']
      for filename in files_sorted:
        ''' plot the data for the file
          @param list1 list2, the list to plot the figure
          @param objectlife, the list to store the number of different object life range
        '''
        list1 = []
        list2 = []
        i = 0
        list11 = []  # used for objectallocation label
        list22 = []  # used for objectallocation label
        list3count = 1
        objectlife = []
        for countlist in range(0, 1000000):
          objectlife.append(0)
        maxlength = 0
        fp = open(filename, 'r')
        for line in fp:
          if i > 0:
            word = line.split(',')
            if option == "objectlife":
              # word[0] object_id, word[1] object_life
              length = helper(int(word[1]))
              objectlife[length] += 1
              if length > maxlength:
                maxlength = length
            else:
              list1.append(int(word[0]))
              list2.append(int(word[1]))
              if int(word[0]) > list3count*100000000:
                list3count += 1
                list11.append(int(word[0]))
                list22.append(int(word[1]))
          i += 1
        fp.close()
        if option == "objectlife":
          total = 0
          cumulative = 0
          for element in objectlife:
            total += element
          for item in range(0, (maxlength+1)):
            cumulative += objectlife[item]
            list1.append(item)
            list2.append(float(float(cumulative)/float(total)))
        plt.figure(1)
        print filename
        if option == "objectlife":
          plt.plot(list1, list2, colorlist[j], label=(filename.split('_')[-1]))
        else:
          plt.plot(list1, list2, alloclist[j])
          plt.plot(list11, list22, alloclist2[j], label=(filename.split('_')[-1]))
        j += 1
        plt.savefig(resultfile, format='pdf', dpi=900)
  plt.figure(1)
  if option == "objectlife":
    ax = plt.gca()
    ax.grid(True)
    plt.xticks(list1, labels)
  plt.title(title)
#  plt.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
  plt.xlabel(x)
  plt.ylabel(y)
  plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
  plt.legend(loc = "lower right", shadow = True)
  plt.title(name)
  plt.savefig(resultfile, format='pdf', dpi=900, bbox_inches='tight')

def main():
  try:
    script, filepath = sys.argv
  except:
    sys.exit(1)
  plot(filepath, "objectlive") 
  '''
  if not os.path.isfile(filepath):
    for root, dirs, files in os.walk(filepath):
      fnames = [os.path.join(root, f) for f in files]
      j = 0
      colorlist = ['b', 'r', 'g', 'c', 'm', 'y', 'k']
      for filename in fnames:
        list1 = []
        list2 = []
        i = 0
        fp = open(filename, 'r')
        for line in fp:
          if i > 0:
            word = line.split(',')
            list1.append(int(word[0]))
            list2.append(int(word[1]))
          i += 1
        fp.close()
        plt.figure(1)
        plt.plot(list1, list2, colorlist[j], label=(filename.split('_')[-1]))
#        plt.legend((p1[0]), (filename.split('_')[-1]))
        j += 1
        plt.savefig("object_alive.pdf", format='pdf', dpi=900)
  plt.figure(1)
  plt.title("Change of alive object number with heap allocation")
  plt.xlabel("Heap allocation size")
  plt.ylabel("Alive object number")
  plt.legend(loc='lower right', shadow = True)
  plt.savefig("object_alive.pdf", format='pdf', dpi=900)
#  frame = legend.get_frame()
'''

#if __name__ == '__main__':
#  main()
