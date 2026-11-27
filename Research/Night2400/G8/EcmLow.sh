#!/bin/sh
set -eu
base=/mnt/e/PerfectNumbers/Build/Night2400/LinuxTools/usr
export LD_LIBRARY_PATH="$base/lib/x86_64-linux-gnu"
case "$1" in
alpha) n=84555698756568194985402955772715138750519747432920344882303021;;
beta) n=140324121901326974955002918638986644602100619438994261423138153109049160183383632493343;;
gamma) n=1362241532466529096697137693434963385484932932556468372932967747;;
delta) n=1835073256170734214092822143872850465225519;;
epsilon) n=$(python3 -c 'print((4073**109-1)//4072)');;
*) exit 2;;
esac
for sigma in $(seq 510001 510027); do
 code=0
 d=$(printf '%s\n' "$n" | timeout 22 "$base/bin/ecm" -q -param 0 -sigma "$sigma" 240000 29000000) || code=$?
 if [ "$code" -gt 1 ] && [ "$code" -ne 124 ]; then printf 'curve=%s status=%s\n%s\n' "$sigma" "$code" "$d"; break; fi
done
