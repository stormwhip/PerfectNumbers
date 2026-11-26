#!/bin/sh
set -eu
base=/mnt/e/PerfectNumbers/Build/Night2400/LinuxTools/usr
export LD_LIBRARY_PATH="$base/lib/x86_64-linux-gnu"
case "$1" in
small) q=7553426653081; f=2;;
shared) q=32009891; f=12;;
wide) q=172827552198815888791; f=4;;
other) q=150257132274929209881291511765897647525733071572857469584719562313499835376588356199183839; f=2;;
*) exit 2;;
esac
n=$(python3 -c "q=$q;print((q**($f+1)-1)//(q-1))")
for sigma in $(seq 263001 263022); do
 code=0
 d=$(printf '%s\n' "$n" | timeout 18 "$base/bin/ecm" -q -param 0 -sigma "$sigma" 180000 20000000) || code=$?
 if [ "$code" -ne 0 ] && [ "$code" -ne 124 ]; then printf 'curve=%s status=%s\n%s\n' "$sigma" "$code" "$d"; break; fi
done
