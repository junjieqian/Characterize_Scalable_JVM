#!/bin/bash

# algorithm, run with jikesrvm different times with different thread counts and possible different cores

#Jikesrvm=/home/jqian/projects/jvm_cache_management/work-folder/jikesrvm-3.1.3-10723-node3/dist/working/production_x86_64-linux/rvm

python ../set_cpus.py 0

Dacapo=/home/jqian/projects/jvm_cache_management/work-folder/dacapo-9.12-rc1-bach.jar
Scala=/home/jqian/tmp/temp/core_change/scala.jar

declare -A dacapobenchmark
#dacapobenchmark=(["lusearch"]="21m" ["xalan"]="21m" ["sunflow"]="21m" ["h2"]="795m" ["avrora"]="33m" ["eclipse"]="249m" ["jython"]="66m" ["pmd"]="102m")
dacapobenchmark=(["xalan"]="21m" ["sunflow"]="21m" ["h2"]="795m" ["avrora"]="33m" ["eclipse"]="249m" ["jython"]="66m" ["pmd"]="102m")
declare -A scalabenchmark
 scalabenchmark=(["scalatest"]="33m" ["apparat"]="51m" ["scalac"]="84m" ["scaladoc"]="105m" ["tmt"]="96m")

#for core in 0 1 3 7
for core in 7
do
  if [ $core -gt 0 ]
  then
  python ../set_cpus.py 0-$core
  fi
    for name in "${!dacapobenchmark[@]}"
    do
      for i in {1..15}
      do
        set -x
#        java -Xmx${dacapobenchmark["$name"]} -Xms${dacapobenchmark["$name"]} -jar $Dacapo $name -t $thread 
#        cat /proc/lock_stat >> $name-$core-$thread
        java -Xrunhprof:monitor=y,thread=y,interval=1,verbose=y -jar $Dacapo $name
		cat java.hprof.txt >> $name-$core
        sleep 20
        set +x
        echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" >> $name-$core
      done
    done
    for nameS in "${!scalabenchmark[@]}"
    do
      for i in {1..15}
      do
        set -x
#        java -Xmx${scalabenchmark["$nameS"]} -Xms${scalabenchmark["$nameS"]} -jar $Scala $nameS -t $thread
#        cat /proc/lock_stat >> $nameS-$core-$thread
        java -Xrunhprof:monitor=y,thread=y,interval=1,verbose=y -jar $Scala $nameS
		cat java.hprof.txt >> $nameS-$core
        sleep 20
        set +x
        echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%" >> $nameS-$core
      done
    done
done

