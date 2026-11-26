#!/bin/sh
set -eu
base=/mnt/e/PerfectNumbers/Build/Night2400/LinuxTools/usr
export LD_LIBRARY_PATH="$base/lib/x86_64-linux-gnu"
case "$1" in
four) n=112031703428137653085910237427172260895957252604623290425614628653256388372235931 ;;
six) n=136983922146778098563474365501669924336488587342256165855994670772029535103380525352161949219449591346338291754331526119563771965181758866576605524420815851 ;;
*) exit 2;;
esac
for sigma in $(seq 372001 372045); do
  code=0
  d=$(printf '%s\n' "$n" | timeout 25 "$base/bin/ecm" -q -param 0 -sigma "$sigma" 250000 30000000) || code=$?
  if [ "$code" -ne 0 ] && [ "$code" -ne 124 ]; then printf 'curve=%s status=%s\n%s\n' "$sigma" "$code" "$d"; break; fi
done
