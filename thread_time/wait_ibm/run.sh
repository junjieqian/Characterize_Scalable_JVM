#!/bin/bash

java -jar ../dacapo-9.12-rc1-bach.jar sunflow &

pid=0

while [ $pid -eq 0 ]
do
	pid="pidof java"
done

bash waitDataCollector.sh $pid
