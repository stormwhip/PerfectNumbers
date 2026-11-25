"""Discovery only: score large probable-prime cyclotomic root blocks, never accept a proof."""
import argparse
from functools import cache
import json
from math import gcd, isqrt, prod
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from Ledger import load_baseline, obligations
from SizeExperiment import trial_bank
from SizePilot import B,I

@cache
def divisors(n):
    return tuple(sorted({x for j in range(1,isqrt(n)+1) if n%j==0 for x in (j,n//j)}))

@cache
def phi(p,h):
    return (p**h-1)//prod(phi(p,d) for d in divisors(h) if d<h)


def main():
    from sympy import isprime
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--limit',type=int,default=12)
    parser.add_argument('--all',action='store_true')
    args=parser.parse_args()
    data=load_baseline(); cases=obligations(data['remaining_shards']);pool=trial_bank()
    pstore={}
    for p,e in sorted(cases,key=lambda item:-item[1]*item[0].bit_length()):
        if not args.all and pstore.get(p,0)>=args.limit:continue
        pstore[p]=pstore.get(p,0)+1
        A=I.sigma(p,e); hints=[q for q in pool if A%q==0]
        rough=A
        for q in hints:
            while rough%q==0:rough//=q
        blocks=[]
        for h in divisors(e+1)[1:]:
            n=gcd(rough,phi(p,h));
            if n>1:blocks.append((h,n,bool(isprime(n))))
        ks=[*hints,*(x for _,x,prp in blocks if prp)]
        if any(x**3>=3*B for x in ks):
            print(json.dumps(dict(p=p,e=e,status='cap_candidate',numbers=[x for x in ks if x**3>=3*B])),flush=True)
        else:
            print(json.dumps(dict(p=p,e=e,status='unverified',known=len(hints),blocks=[(h,len(str(x)),prp,x if prp else None) for h,x,prp in blocks])),flush=True)

if __name__=='__main__':main()
