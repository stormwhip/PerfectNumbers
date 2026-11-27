#!/usr/bin/env bash
# Optional deterministic discovery replay. Not used to validate any proof.
set -eu
[[ $# == 6 ]] || { echo 'usage: ReplaySearch.sh BASE INDEX B1 B2 FIRST_SIGMA LAST_SIGMA' >&2; exit 2; }
: "${ECM:=ecm}"
base=$1; index=$2; b1=$3; b2=$4; first=$5; last=$6
n=$(python3 -I -S -B -c 'import sys; b,d=map(int,sys.argv[1:]); print((b**d-1)//(b-1))' "$base" "$index")
for ((s=first;s<=last;s++)); do
    status=0
    printf '%s\n' "$n" | "$ECM" -param 1 -sigma "$s" "$b1" "$b2" || status=$?
    if (( status > 1 )); then exit "$status"; fi
    if (( status == 1 )); then exit 1; fi
done
