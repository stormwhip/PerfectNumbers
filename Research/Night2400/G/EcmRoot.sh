#!/bin/sh
set -eu
TOOLS=/mnt/e/PerfectNumbers/Build/Night2400/LinuxTools/usr
export LD_LIBRARY_PATH="$TOOLS/lib/x86_64-linux-gnu"
python3 -c 'print((11**359-1)//10//2471107084783904470093)' | timeout 1800 "$TOOLS/bin/ecm" -q -c 450 250000
