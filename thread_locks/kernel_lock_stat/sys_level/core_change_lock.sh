#!/bin/bash

# algorithm, run with jikesrvm different times with different thread counts and possible different cores

#Jikesrvm=/home/jqian/projects/jvm_cache_management/work-folder/jikesrvm-3.1.3-10723-node3/dist/working/production_x86_64-linux/rvm

#python ../set_cpus.py 0

Dacapo=/home/jqian/projects/jvm_cache_management/work-folder/dacapo-9.12-rc1-bach.jar
Scala=/home/jqian/tmp/temp/core_change/scala.jar

declare -A dacapobenchmark
#dacapobenchmark=(["lusearch"]="21m" ["xalan"]="21m" ["sunflow"]="21m" ["h2"]="795m" ["avrora"]="33m" ["eclipse"]="249m" ["jython"]="66m" ["pmd"]="102m")
dacapobenchmark=(["xalan"]="21m" ["sunflow"]="21m" ["h2"]="795m" ["avrora"]="33m" ["eclipse"]="249m" ["jython"]="66m" ["pmd"]="102m" ["lusearch"]="63m")
declare -A scalabenchmark
scalabenchmark=(["scalatest"]="33m" ["apparat"]="51m" ["scalac"]="84m" ["scaladoc"]="105m")

#for core in 0 1 3 7
#do
#  if [ $core -gt 0 ]
#  then
#  python ../set_cpus.py 0-$core
#  fi
core=8
  for thread in 1 2 4 8 16 32 48
  do
    for name in "${!dacapobenchmark[@]}"
    do
      for i in {1..10}
      do
        set -x
        echo "StartTime::: "$(($(date +%s%N)/1000000)) >> $name-$core-$thread
        echo 0 > /proc/lock_stat
        java -Xmx${dacapobenchmark["$name"]} -Xms${dacapobenchmark["$name"]} -jar $Dacapo $name -t $thread 
        cat /proc/lock_stat >> $name-$core-$thread
        echo "EndTime::: "$(($(date +%s%N)/1000000)) >> $name-$core-$thread
        sleep 20
        set +x
        echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" >> $name-$core-$thread
      done
    done
    for nameS in "${!scalabenchmark[@]}"
    do
      for i in {1..10}
      do
        set -x
        echo "StartTime::: "$(($(date +%s%N)/1000000)) >> $nameS-$core-$thread 
        echo 0 > /proc/lock_stat
        java -Xmx${scalabenchmark["$nameS"]} -Xms${scalabenchmark["$nameS"]} -jar $Scala $nameS -t $thread
        cat /proc/lock_stat >> $nameS-$core-$thread
        echo "EndTime::: "$(($(date +%s%N)/1000000)) >> $nameS-$core-$thread
        sleep 20
        set +x
        echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%" >> $nameS-$core-$thread
      done
    done
  done
#done

