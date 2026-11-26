#!/bin/sh
set -eu
TOOLS=/mnt/e/PerfectNumbers/Build/Night2400/LinuxTools/usr
export LD_LIBRARY_PATH="$TOOLS/lib/x86_64-linux-gnu"
python3 -c 'q=2471107084783904470093; print((q**11-1)//(q-1)//23)' | timeout 950 "$TOOLS/bin/ecm" -q -c 210 200000
