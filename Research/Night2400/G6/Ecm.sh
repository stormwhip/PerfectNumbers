#!/bin/sh
# Deterministic short queues on exact unresolved source sums.
set -eu
base=/mnt/e/PerfectNumbers/Build/Night2400/LinuxTools/usr
export LD_LIBRARY_PATH="$base/lib/x86_64-linux-gnu"
case "$1" in
alpha) q=3158844086932134865267303; f=10; product=864484445649417880981;;
beta) q=1308945966566467; f=6; product=29;;
gamma) q=993862819; f=28; product=1;;
delta) q=993862819; f=30; product=1;;
epsilon) q=231050784610489; f=60; product=1;;
zeta) q=284584844867762741744246325802733641345390981; f=4; product=620091679650662155;;
eta) q=1022243; f=30; product=1;;
theta) q=194220667891; f=18; product=950843221;;
iota) q=3158844086932134865267303; f=16; product=140568437238106181;;
kappa) q=3158844086932134865267303; f=30; product=1;;
*) exit 2;;
esac
n=$(python3 -c "q=$q; n=(q**($f+1)-1)//(q-1); assert n%$product==0;print(n//$product)")
for sigma in $(seq 262001 262028); do
 code=0
 d=$(printf '%s\n' "$n" | timeout 22 "$base/bin/ecm" -q -param 0 -sigma "$sigma" 230000 28000000) || code=$?
 if [ "$code" -ne 0 ] && [ "$code" -ne 124 ]; then printf 'curve=%s status=%s\n%s\n' "$sigma" "$code" "$d"; break; fi
done
