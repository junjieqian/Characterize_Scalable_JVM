#!/bin/bash

#java -server -XX:+TieredCompilation -XX:+AggressiveOpts \
#  -XX:+PrintGCDetails -XX:+PrintGCTimeStamps -Xloggc:$*_GC \
java  -Xmx4g -Xbootclasspath/a:$ELEPHANT_TRACKS_HOME \
  -agentlib:ElephantTracks=javaPath=/usr/bin/java:classPath=$ELEPHANT_TRACKS_HOME/asm-3.3.1.jar:verbose=f:traceFile="./$*_tracefile":outputFile=java-$*:classReWriter=$ELEPHANT_TRACKS_HOME/elephantTracksRewriter.jar \
  -jar /home/jqian/projects/jvm_cache_management/profile-tools/elephant_tracks/elephant-results/dacapo-9.12.jar $*
