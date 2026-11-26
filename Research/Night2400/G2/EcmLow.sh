#!/bin/sh
set -eu
TOOLS=/mnt/e/PerfectNumbers/Build/Night2400/LinuxTools/usr
export LD_LIBRARY_PATH="$TOOLS/lib/x86_64-linux-gnu"
case "$1" in
8) expr='(q**6+q**3+1)//19' ;;
9) expr='(q**4-q**3+q**2-q+1)//41' ;;
10) expr='((q**11-1)//(q-1))//(11*67*727541*3433783*32255653*1849984860439*2631061346321)' ;;
13) expr='((q**7+1)//(q+1))//205157' ;;
*) exit 2 ;;
esac
python3 -c "q=11842464881317660217; print($expr)" | timeout 300 "$TOOLS/bin/ecm" -q -c 48 125000
