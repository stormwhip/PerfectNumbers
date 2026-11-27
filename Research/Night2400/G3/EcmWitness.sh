#!/bin/sh
set -eu
base=/mnt/e/PerfectNumbers/Build/Night2400/LinuxTools/usr
export LD_LIBRARY_PATH="$base/lib/x86_64-linux-gnu"
case "$1" in
alpha) expr='((575791**19-1)//575790)' ;;
beta) expr='348891733212830115445717267859463577250432526971733820097668034027' ;;
gamma) expr='((1359610333**11-1)//1359610332)//355873541' ;;
delta) expr='23375230435605291983084445388654048956813047346619897393318035368479827540579508333' ;;
*) exit 2;;
esac
n=$(python3 -c "print($expr)")
for sigma in $(seq 439001 439035); do
  code=0
  d=$(printf '%s\n' "$n" | timeout 20 "$base/bin/ecm" -q -param 0 -sigma "$sigma" 300000 50000000) || code=$?
  if [ "$code" -ne 0 ] && [ "$code" -ne 124 ]; then printf 'curve=%s status=%s\n%s\n' "$sigma" "$code" "$d"; break; fi
done
