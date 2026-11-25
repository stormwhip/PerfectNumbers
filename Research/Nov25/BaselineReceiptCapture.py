"""Record positive cold-replay receipts for the historical baseline only."""
import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path

PIN = 'e89dffd5a74debad80f695d6177f3d785e6268e8'
HASH = 'b66c42bf222be1344d858d42a779a45c288187ae16ae08c1d2fcea48b80f9edb'
TOTAL = 285


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('receipts', type=Path)
    p.add_argument('out', type=Path)
    args = p.parse_args()
    if not args.receipts.is_dir():raise ValueError('expected cold-replay receipt directory')
    checked = {}
    for path in sorted(args.receipts.glob('*.json')):
        job = json.loads(path.read_bytes())
        if job['sha256'] != HASH or job['passed'] is not True or job['name'] in checked:
            raise ValueError('mismatched audit provenance or duplicate receipt')
        checked[job['name']] = job
    if len(checked)>=TOTAL:raise ValueError('reconcile as a full replay instead')
    result = {'historical_baseline_commit':PIN, 'replay_input_sha256':HASH,
              'recorded_at_beijing':datetime.now(timezone(timedelta(hours=8))).isoformat(timespec='seconds'),
              'expected_jobs':TOTAL, 'completed_successfully':len(checked), 'fully_verified':False,
              'scope':'Partial historical baseline run; not a Nov25 proof registration. None of the other jobs is credited.',
              'receipts':list(checked.values())}
    args.out.write_text(json.dumps(result,indent=1)+'\n',encoding='utf-8',newline='\n')
    print(f'{len(checked)}/{TOTAL} historical jobs have positive receipts; not a complete baseline replay')


if __name__=='__main__':main()
