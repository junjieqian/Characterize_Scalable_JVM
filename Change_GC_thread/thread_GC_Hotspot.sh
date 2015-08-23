#!/bin/bash
#
# thread_same_gc.sh
# script to run the benchmark with different thread numbers, but same GC numbers with changable heap size

# define the Logfile
#LOGFILE=/home/jqian/projects/jvm_cache_management/work-folder/thread_and_GC/log_
LOGFILE=./results/

# define JikesRVM/benchmark path
Jikes=/home/jqian/projects/tools/JikesRVM/jikesrvm-3.1.3/dist/working/production_x86_64-linux/rvm
Jikes_PMU=/home/jqian/projects/jvm_cache_management/work-folder/jikesrvm-3.1.3-production-perfevent/dist/working/production_x86_64-linux/rvm

Dacapo=/home/jqian/projects/jvm_cache_management/work-folder/dacapo-9.12-rc1-bach.jar
SPECJVM=/home/jqian/projects/jvm_cache_management/benchmarks/specjvm2008/SPECjvm2008.jar
Scala=./scala.jar

# declare the associated array, benchmark-heap_size
# this is bash-4, supports associate array
declare -A dacapobenchmark
#dacapobenchmark=(["eclipse"]="480m" ["jython"]="180m" ["lusearch"]="96m" ["pmd"]="159m" ["sunflow"]="72m" ["avrora"]="96m" ["xalan"]="180m" ["h2"]="600m")
dacapobenchmark=(["eclipse"]="480m" ["jython"]="180m" ["pmd"]="159m" ["sunflow"]="72m" ["xalan"]="180m" ["h2"]="600m")
declare -A scalabenchmark
scalabenchmark=(["scalac"]="84m" ["scaladoc"]="105m" ["scalatest"]="33m")

function exe {
    set -x
    $Jikes -Xmx$1 -Xms$1 -verbose:gc -jar $Dacapo $name -t $thread >> $LOGFILE
    set +x
    echo "==============================" >> $LOGFILE
}

for thread in 1 2 4 8 16 32 48
do
	for gcthread in 1 2 4 8
	do
		for i in {1..15}
		do
		    for name in "${!dacapobenchmark[@]}"
			do
		        echo "$name-${dacapobenchmark["$name"]}"
			    set -x
				java -Xms${dacapobenchmark["$name"]} -Xmx${dacapobenchmark["$name"]} -verbose:gc -XX:+PrintGCApplicationConcurrentTime -XX:+PrintGCApplicationStoppedTime -XX:+UseParallelGC -XX:ParallelGCThreads=$gcthread -jar $Dacapo $name -t $thread >> $LOGFILE"$name"_"$thread"_$gcthread
	            sleep 20
		        echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" >> $LOGFILE"$name"_"$thread"_$gcthread
			done

			for sname in "${!scalabenchmark[@]}"
			do
				echo "$sname-${scalabenchmark["$sname"]}"
				set -x
				java -Xms${scalabenchmark["$sname"]} -Xmx${scalabenchmark["$sname"]} -verbose:gc -XX:+PrintGCApplicationConcurrentTime -XX:+PrintGCApplicationStoppedTime -XX:+UseParallelGC -XX:ParallelGCThreads=$gcthread -jar $Scala $sname -t $thread >> $LOGFILE"$sname"_"$thread"_$gcthread
				sleep 20
				echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" >> $LOGFILE"$sname"_"$thread"_$gcthread
			done
		done
	done
done

for thread in 1 2 4 8 16 32 48; do
	for gcthread in 1 2 4 8; do
		for i in {1..15}; do
			java -Xms96m -Xmx96m -verbose:gc -XX:+PrintGCApplicationConcurrentTime -XX:+PrintGCApplicationStoppedTime -XX:+UseParallelGC -XX:ParallelGCThreads=$gcthread -jar $Dacapo lusearch -t $thread >> $LOGFILE"lusearch"_"$thread"_$gcthread
			sleep 20
			echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" >> $LOGFILE"lusearch"_"$thread"_$gcthread
		done
	done
done
