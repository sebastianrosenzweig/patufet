#!/bin/bash

last_pid=""

for f in /proc/[0-9]*/fd/*; do
    readlink "$f" 2>/dev/null | grep -q '/dev/snd/' || continue

    pid=${f#/proc/}
    pid=${pid%%/*}

    [ "$pid" = "$last_pid" ] && continue
    last_pid="$pid"

    echo "Killing PID $pid"
    kill -TERM "$pid"
done
