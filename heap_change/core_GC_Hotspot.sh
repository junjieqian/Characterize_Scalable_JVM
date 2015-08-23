#!/bin/bash
#
# thread_same_gc.sh
# script to run the benchmark with different thread numbers, but same GC numbers with changable heap size

# define the Logfile
#LOGFILE=/home/jqian/projects/jvm_cache_management/work-folder/thread_and_GC/log_
LOGFILE=./results/

# define JikesRVM/benchmark path
Dacapo=./dacapo-9.12-rc1-bach.jar

# declare the associated array, benchmark-heap_size
# this is bash-4, supports associate array

name="lusearch"
size="96m"
gc="2"

for thread in 1 2 4
do
   if [ $thread -eq 1 ]; then
      python set_cpus.py 0
	size="600m"
   elif [ $thread -eq 2 ]; then
      python set_cpus.py 0-1
	size="400m"
   elif [ $thread -eq 4 ]; then
      python set_cpus.py 0-3
	size="100m"
   elif [ $thread -eq 8 ]; then
      python set_cpus.py 0-7
	size="110m"
   elif [ $thread -eq 16 ]; then
      python set_cpus.py 0-15
	size="120m"
   elif [ $thread -eq 32 ]; then
      python set_cpus.py 0-31
	size="180m"
   elif [ $thread -eq 48 ]; then
      python set_cpus.py 0-47
	size="200m"
   fi
   for i in {1..4}; do
	   java -Xms"$size" -Xmx"$size" -verbose:gc -XX:+PrintGCApplicationConcurrentTime -XX:+PrintGCApplicationStoppedTime -XX:+UseParallelGC -XX:ParallelGCThreads=$gc  -jar $Dacapo $name >> $LOGFILE"$name"_"$thread"
	   echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" >> $LOGFILE"$name"_"$thread"
done
done

