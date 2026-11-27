#!/bin/sh
# A bounded, deterministic follow-up for the low eighth branch remainder.
set -eu
TOOLS=/mnt/e/PerfectNumbers/Build/Night2400/LinuxTools/usr
export LD_LIBRARY_PATH="$TOOLS/lib/x86_64-linux-gnu"
n=110688337163891941111745062522003633670990951824616559702137636442030920991799895565406338396271
s=200001
while [ "$s" -le 200048 ]; do
  code=0
  echo "$n" | timeout 30 "$TOOLS/bin/ecm" -q -param 0 -sigma "$s" 160000 16000000 || code=$?
  if [ "$code" -ne 0 ] && [ "$code" -ne 124 ]; then printf 'curve=%s status=%s\n' "$s" "$code"; break; fi
  s=$((s+1))
done
