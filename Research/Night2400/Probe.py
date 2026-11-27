"""Discovery-only: inspect root-pivot opportunities, not a certificate.

Requires python-flint and the GitHub data-v1 index. Each printed branch count
uses exact State filters but probable-prime factor labels are only suggestions.
"""
import argparse
import json
from math import prod
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent/'Session20261126')]
from Discover import Finder, Bank
from PivotCheck import C, B, floor10


def pivot_cases(s,q):
    v=C.valuation(s.D,q)
    scale=s.base//q**v
    while scale*q**v <= B:
        if s.possible(q,v,C.valuation(s.D,q)):
            part=C.State([*s.rows.items(),(q,v)])
            if not part.conflict and part.base<=B and prod(C.sigma(q,t) for q,t in part.rows.items())<=2*part.X:
                yield v,part
        v+=1


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--index',required=True,type=Path)
    p.add_argument('--key',action='append',nargs=2,type=int)
    p.add_argument('--smooth-bits',default=0,type=int)
    a=p.parse_args()
    finder=Finder(Bank(a.index),a.smooth_bits)
    source=json.loads((HERE.parent/'FinalSprint/Delta.json').read_bytes())
    counts={}
    for row in source['remaining_shards']:
        for e in row['remaining_actuals']:
            counts.setdefault((row['root'],e),[]).append((row['id'],len(row['remaining_actuals'])))
    keys=list(map(tuple,a.key)) if a.key else counts
    for p,e in keys:
        s=C.State([(p,e)])
        roots=[q for q in finder.factors(p,e) if s.D%q==0 and q not in s.bad]
        pivots=[]
        for q in sorted(roots,reverse=True)[:3]:
            cases=list(pivot_cases(s,q))
            pivots.append({'prime':str(q),'bits':q.bit_length(),'count':len(cases),'min_floor':min((floor10(s.base) for _,s in cases),default=None),'exps':[v for v,_ in cases] if len(cases)<=18 else None})
        print(json.dumps({'key':[p,e],'shards':counts.get((p,e),[]),'pivots':pivots},separators=(',',':')),flush=True)


if __name__=='__main__':
    main()
