#!/bin/sh
set -eu
TOOLS=/mnt/e/PerfectNumbers/Build/Night2400/LinuxTools/usr
export LD_LIBRARY_PATH="$TOOLS/lib/x86_64-linux-gnu"
q=11842464881317660217
n=$(python3 -c "q=$q; print((q**31-1)//(q-1)//1303//230374393)")
for sigma in $(seq 310001 310024); do
  code=0
  out=$(printf '%s\n' "$n" | timeout 20 "$TOOLS/bin/ecm" -q -param 0 -sigma "$sigma" 120000 15000000) || code=$?
  if [ "$code" -ne 0 ] && [ "$code" -ne 124 ]; then printf 'curve=%s status=%s\n%s\n' "$sigma" "$code" "$out"; break; fi
done
