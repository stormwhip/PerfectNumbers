"""Budgeted discovery only; accepted factors always require independent proof and replay."""
import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = '/mnt/e/PerfectNumbers/NightCache/ecm/pkg/usr'
BEIJING = timezone(timedelta(hours=8))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--strong', action='store_true')
    args = p.parse_args()
    e = 1162
    curves, b1 = (64,1000000) if args.strong else (128,250000)
    name = f'Root{e}ECM' + ('Strong' if args.strong else '')
    n = (3**(e+1)-1)//2
    cutoff = datetime(2026, 11, 25, 9, 15, tzinfo=BEIJING)
    start = datetime.now(BEIJING)
    secs = min(1200, int((cutoff-start).total_seconds()))
    if secs < 1:
        raise SystemExit('root-3 ECM deadline passed')
    cmd = ['wsl', '-d', 'Ubuntu', '--', 'timeout', f'{secs}s', 'env',
           f'LD_LIBRARY_PATH={ROOT}/lib/x86_64-linux-gnu', f'{ROOT}/bin/ecm',
           '-maxmem', '128', '-one', '-c', str(curves), str(b1)]
    log = HERE / (name+'.log')
    with log.open('wb') as out:
        proc = subprocess.run(cmd, input=f'{n}\n'.encode(), stdout=out, stderr=subprocess.STDOUT,
                              timeout=secs+20, cwd=HERE)
    units = log.read_bytes()
    # WSL startup can prepend a UTF-16 diagnostic to otherwise ASCII ECM output.
    text = units.decode('ascii', 'replace').replace('\x00', '')
    digest = hashlib.sha256(units).hexdigest()
    log.write_text('\n'.join(x for x in text.splitlines() if x.isascii())+'\n', encoding='ascii')
    proposed = {int(w) for w in re.findall(r'\b[0-9]{1,555}\b', text)}
    factors = sorted(w for w in proposed if 1<w<n and n%w==0)
    rows = dict(root=3, e=e, started=start.isoformat(), requested_curves=curves, b1=b1,
                seconds=secs, completed=text.count('Step 2 took'), status=proc.returncode,
                sigma_sha256=hashlib.sha256(str(n).encode()).hexdigest(),
                output_stream_sha256=digest, factors=list(map(str, factors)))
    (HERE / (name+'.json')).write_text(json.dumps(rows, indent=1)+'\n', encoding='utf8')
    print(rows, flush=True)
    if proc.returncode not in (0, 2, 6, 8, 10, 14, 124):
        raise SystemExit(proc.returncode)


if __name__ == '__main__':
    main()
