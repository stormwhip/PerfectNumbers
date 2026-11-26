#!/bin/sh
set -eu
base=/mnt/e/PerfectNumbers/Build/Night2400/LinuxTools/usr
export LD_LIBRARY_PATH="$base/lib/x86_64-linux-gnu"
case "$1" in
root) n=$(python3 -c 'print((13**509-1)//12//4073)'); start=508001; end=508012; b1=100000; b2=10000000;;
*) exit 2;;
esac
for sigma in $(seq "$start" "$end"); do
 code=0
 d=$(printf '%s\n' "$n" | timeout 25 "$base/bin/ecm" -q -param 0 -sigma "$sigma" "$b1" "$b2") || code=$?
 if [ "$code" -gt 1 ] && [ "$code" -ne 124 ]; then printf 'curve=%s status=%s\n%s\n' "$sigma" "$code" "$d"; break; fi
done
