#!/bin/sh
set -eu
TOOLS=/mnt/e/PerfectNumbers/Build/Night2400/LinuxTools/usr
export LD_LIBRARY_PATH="$TOOLS/lib/x86_64-linux-gnu"
python3 -c 'q=2471107084783904470093; print((q**6+q**3+1)//(3*163))' | timeout 1500 "$TOOLS/bin/ecm" -q -c 300 250000
