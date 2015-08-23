#!/usr/bin/bash

#python proc.py stdin stdout java-pmd java -jar ../dacapo-9.12-rc1-bach.jar pmd

Dacapo=/home/jqian/projects/jvm_cache_management/work-folder/dacapo-9.12-rc1-bach.jar
Scala=/home/jqian/projects/jvm_cache_management/benchmarks/scala-benchmark-suite-0.1.0-20120216.103539-3.jar

declare -A dacapobenchmark
dacapobenchmark=(["lusearch"]="96m" ["sunflow"]="72m" ["xalan"]="180m" ["h2"]="600m" ["pmd"]="102m" ["jython"]="66m" ["eclipse"]="249m")

declare -A scalabenchmark
scalabenchmark=(["scalac"]="60m" ["scaladoc"]="60m" ["scalatest"]="60m")

for thread in 1 2 4 8 16 32 48; do
	if [ $thread -eq 1 ]; then
		python set_cpus.py 0
	elif [ $thread -eq 2 ]; then
		python set_cpus.py 0-1
	elif [ $thread -eq 4 ]; then
		python set_cpus.py 0-3
	elif [ $thread -eq 8 ]; then
		python set_cpus.py 0-7
	elif [ $thread -eq 16 ]; then
		python set_cpus.py 0-15
	elif [ $thread -eq 32 ]; then
		python set_cpus.py 0-31
	elif [ $thread -eq 48 ]; then
		python set_cpus.py 0-47
	fi
	for name in "${!dacapobenchmark[@]}"; do
		python proc2.py stdin stdout $name java -Xmx${dacapobenchmark["$name"]} -Xms${dacapobenchmark["$name"]} -XX:+UseParallelGC -jar $Dacapo $name 
	done

	for sname in ${!scalabenchmark[@]}; do
		python proc2.py stdin stdout $sname java -Xmx${scalabenchmark["$sname"]} -Xms${scalabenchmark["$sname"]} -XX:+UseParallelGC -jar $Scala $sname
	done
done

