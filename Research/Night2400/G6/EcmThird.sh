#!/bin/sh
set -eu
base=/mnt/e/PerfectNumbers/Build/Night2400/LinuxTools/usr
export LD_LIBRARY_PATH="$base/lib/x86_64-linux-gnu"
case "$1" in
alpha) n=139362892199298432228951499836997234668128840041064913071655990839789;;
beta) n=290259656088840089392886034145410779171161515751057780823533523326107098337041;;
gamma) n=2762673044485717326294288145065029547520388060581022660222735141108190262803161;;
*) exit 2;;
esac
for sigma in $(seq 265001 265018); do
 code=0
 d=$(printf '%s\n' "$n" | timeout 20 "$base/bin/ecm" -q -param 0 -sigma "$sigma" 260000 30000000) || code=$?
 if [ "$code" -ne 0 ] && [ "$code" -ne 124 ]; then printf 'curve=%s status=%s\n%s\n' "$sigma" "$code" "$d"; break; fi
done
