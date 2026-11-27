#!/bin/sh
set -eu
base=/mnt/e/PerfectNumbers/Build/Night2400/LinuxTools/usr
export LD_LIBRARY_PATH="$base/lib/x86_64-linux-gnu"
case "$1" in
alpha) n=201496215230984054640175876387971392697121;;
beta) n=160488872727544445222464620991213620971322415595901816921154141;;
gamma) n=3305073412018158677666642480587699684762394085901254116632037321599;;
delta) n=17205224259951709769833114728652235060560868076363960361;;
epsilon) n=581982884110999740353000236460988226449083520650728713439301602861481969;;
*) exit 2;;
esac
for sigma in $(seq 511001 511016); do
 code=0
 d=$(printf '%s\n' "$n" | timeout 18 "$base/bin/ecm" -q -param 0 -sigma "$sigma" 200000 22000000) || code=$?
 if [ "$code" -gt 1 ] && [ "$code" -ne 124 ]; then printf 'curve=%s status=%s\n%s\n' "$sigma" "$code" "$d"; break; fi
done
