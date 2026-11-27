#!/bin/sh
set -eu
base=/mnt/e/PerfectNumbers/Build/Night2400/LinuxTools/usr
export LD_LIBRARY_PATH="$base/lib/x86_64-linux-gnu"
n=$(python3 -c 'print((7**883-1)//6//21193)')
for sigma in $(seq 882001 882020); do
 code=0
 d=$(printf '%s\n' "$n" | timeout 25 "$base/bin/ecm" -q -param 0 -sigma "$sigma" 160000 18000000) || code=$?
 if [ "$code" -ne 0 ] && [ "$code" -ne 124 ]; then printf 'curve=%s status=%s\n%s\n' "$sigma" "$code" "$d"; break; fi
done
