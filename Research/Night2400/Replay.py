"""Replay the independently accepted complete nightly keys, then verify projection.

Conditional packets are intentionally not credited or run here. This is not a
full-history proof replay. No discovery package or factor cache is required.
"""
import argparse
from ast import literal_eval
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from time import perf_counter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

# A newly accepted key requires an explicit candidate-specific status check.
MECHANISMS = {
    (7, 28): ('D2/Verify.py', (), 'VERIFIED (7, 28)'),
    (7, 130): ('E/Verify130.py', ('E/Tree7x130.json.gz',), 'tree'),
    (7, 420): ('VerifyFibers.py', ('E4/Fibers7x420Complete.json.gz',), 'fibers'),
    (7, 490): ('VerifyFibers.py', ('E3/Fibers7x490Complete.json.gz',), 'fibers'),
    (7, 586): ('VerifyFibers.py', ('E5/Fibers7x586Complete.json.gz',), 'fibers'),
    (7, 682): ('VerifyFibers.py', ('E6/Fibers7x682Complete.json.gz',), 'fibers'),
    (7, 732): ('VerifyFibers.py', ('E7/Fibers7x732Complete.json.gz',), 'fibers'),
    (13, 372): ('Verify13x372.py', (), 'merged'),
    (19, 162): ('VerifyFibers.py', ('E2/Fibers19x162Complete.json.gz',), 'fibers'),
    (19, 238): ('../FinalSprint/JointTree.py', ('F2/JointTree19x238.json.gz',), 'joint_tree'),
    (19, 270): ('../FinalSprint/JointTree.py', ('F3/JointTree19x270.json.gz',), 'joint_tree'),
    (19, 316): ('D/Verify.py', (), 'VERIFIED (19, 316)'),
    (19, 502): ('../Session20261126/TreeCheck.py', ('F/Tree19x502.json.gz',), 'stock_tree'),
}


def run(script, args=()):
    cmd = [sys.executable, '-I', '-S', '-B', '-X', 'int_max_str_digits=0', str(HERE/script), *map(str,args)]
    t=perf_counter()
    r=subprocess.run(cmd,cwd=ROOT,check=True,stdout=subprocess.PIPE,text=True,encoding='utf-8')
    return r.stdout,perf_counter()-t


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--projection-only',action='store_true',help='check bookkeeping, not arithmetic')
    args=ap.parse_args()
    if not __debug__:raise RuntimeError('assertions required')
    keys=list(map(tuple,json.loads((HERE/'VerifiedKeys.json').read_bytes())))
    assert len(keys)==len(set(keys)) and set(keys)==set(MECHANISMS)
    if not args.projection_only:
        for key in keys:
            script,data,expected=MECHANISMS[key]
            log,sec=run(script,[HERE/p for p in data]); final=log.rstrip().splitlines()[-1]
            if expected=='tree':
                status=json.loads(final)
                assert status['scope']=='EXACT_COMPLETE' and not status['open_paths'] and not status['partial_fibers']
            elif expected=='fibers':
                status=json.loads(final)
                assert tuple(status['key'])==key and not status['open'] and status['covered']==status['domain']
            elif expected=='merged':
                status=json.loads(final)
                assert tuple(status['key'])==key and status['scope']=='EXACT_COMPLETE' and not status['open']
            elif expected=='joint_tree':
                p,e,stats,prices=literal_eval(final)
                assert (p,e)==key and len(stats)==4 and stats[1]>=1 and len(prices)==stats[3]
            elif expected=='stock_tree':
                p,e,stats=literal_eval(final)
                assert (p,e)==key and len(stats)==3 and stats[1]>=1
            else:
                assert final.startswith(expected),final
            print('PASS complete',key,f'{sec:.3f} s',flush=True)
    current=list(map(tuple,json.loads((HERE/'VerifiedKeys.json').read_bytes())))
    if current != keys:
        raise RuntimeError('accepted key list changed during replay; run from a fixed checkout')
    with TemporaryDirectory(prefix='opn-night-projection-') as d:
        work=Path(d)
        run('Project.py',(ROOT/'Research/FinalSprint/Delta.json','--verified',HERE/'VerifiedKeys.json','--out',work))
        for name in ('Delta.json','KeyToShards.json','ShardToKeys.json'):
            assert json.loads((HERE/name).read_bytes())==json.loads((work/name).read_bytes()),name
    ledger=json.loads((HERE/'Delta.json').read_bytes())
    print('PASS projection',ledger['closed'],ledger['open'],ledger['distinct_keys'],
          'projection-only' if args.projection_only else 'with accepted-key arithmetic',flush=True)


if __name__=='__main__':main()
