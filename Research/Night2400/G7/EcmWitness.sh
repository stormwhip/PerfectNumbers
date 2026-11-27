#!/bin/sh
set -eu
base=/mnt/e/PerfectNumbers/Build/Night2400/LinuxTools/usr
export LD_LIBRARY_PATH="$base/lib/x86_64-linux-gnu"
case "$1" in
alpha) n=1794673131407804353825335957011653571279040806829400348676822341;;
beta) n=96397552582727261781206180968483312089996886023542184642389206005528441041;;
gamma) n=135843589400569110473037833291119808916292951837854693690753443912544336367582400808129748709926029708189127699;;
delta) n=2281486702512879669534227181923814808490872549;;
*) exit 2;;
esac
for sigma in $(seq 884001 884015); do
 code=0
 d=$(printf '%s\n' "$n" | timeout 20 "$base/bin/ecm" -q -param 0 -sigma "$sigma" 230000 27000000) || code=$?
 if [ "$code" -ne 0 ] && [ "$code" -ne 124 ]; then printf 'curve=%s status=%s\n%s\n' "$sigma" "$code" "$d"; break; fi
done
