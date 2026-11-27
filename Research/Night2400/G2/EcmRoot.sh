#!/bin/sh
set -eu
TOOLS=/mnt/e/PerfectNumbers/Build/Night2400/LinuxTools/usr
export LD_LIBRARY_PATH="$TOOLS/lib/x86_64-linux-gnu"
python3 -c 'print((19**433-1)//18//11842464881317660217)' | timeout 300 "$TOOLS/bin/ecm" -q -c 40 100000
