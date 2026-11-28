"""Run acceptance commands for committed Astra packets, with explicit scope and arguments."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
from time import monotonic

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
RESEARCH = HERE.relative_to(REPO)


def run(name, params):
    t = monotonic()
    module, *args = params
    resolved = [str(RESEARCH / a.removeprefix('@')) if a.startswith('@') else a for a in args]
    cmd = [sys.executable, '-I', '-S', '-B', '-X', 'int_max_str_digits=0', str(RESEARCH / module), *resolved]
    print(f'BEGIN {name}:', ' '.join(cmd), flush=True)
    result = subprocess.run(cmd, cwd=REPO)
    print(f'END {name}: exit={result.returncode}, wall_seconds={monotonic()-t:.3f}', flush=True)
    return result.returncode


def main():
    assert __debug__, 'do not verify under -O'
    manifest = json.loads((HERE/'ReplayManifest.json').read_bytes())
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('names', nargs='*', help='no arguments runs all listed commands')
    ap.add_argument('--list', action='store_true')
    args = ap.parse_args()
    if args.list:
        print('\n'.join(manifest))
        return 0
    names = args.names or list(manifest)
    unknown = sorted(set(names)-manifest.keys())
    if unknown:
        ap.error('unknown replays: '+', '.join(unknown))
    for name in names:
        if run(name, manifest[name]):
            return 1
    print(f'PASS {len(names)} selected commands (Astra packet scope only; not historical end-to-end replay).')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
