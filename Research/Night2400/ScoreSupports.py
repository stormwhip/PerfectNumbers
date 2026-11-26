"""Discovery triage only: estimate whether support masks reduce exact-root cost.

Uses exact immediate and forest checks, but probable prime labels and unproved
forests are not certificates. The score is for prioritization, not exclusion.
"""
import argparse
from fractions import Fraction
from math import prod
from pathlib import Path
from Probe import C, B, Bank, Finder, floor10


def abundance(s,known):
    levels={z:max(1,C.valuation(s.D,z)) for z in known}
    P=Fraction(prod(C.sigma(z,f) for z,f in s.rows.items()),s.X)
    save=Fraction(1)
    for z,h in levels.items():
        clear=lambda j:C.permitted(z,j,s.bad)
        f=h+h%2
        while not clear(f):f+=2
        m=Fraction(C.sigma(z,f),z**f);P*=m
        if not s.fixed_euler and C.euler(z,s.bad):
            f=h+((1-h)%4)
            while not clear(f):f+=4
            save=min(save,Fraction(C.sigma(z,f),z**f)/m)
    return P*save


def quick(finder,p,e,head):
    t=C.State([(p,e)]); primes=finder.factors(p,e)
    roots=[z for z in primes if t.D%z==0 and z not in t.bad and z!=p]
    direct=done=0;weak=[]; n=len(C.ORDER); k=C.ORDER.index(p)
    for m in range(2**k,2**n,2**(k+1)):
        present=tuple(z for i,z in enumerate(C.ORDER) if i>k and m>>i&1)
        absent=tuple(z for i,z in enumerate(C.ORDER) if i>k and not (m>>i&1))
        s=C.State([(p,e)],present,absent)
        K=sorted(set(present)|set(roots)-set(absent))
        if s.conflict or abundance(s,K)>2:direct+=1;continue
        lb=C.Forest(s,K,[],head).lower()[0]
        if lb>B:done+=1
        else:weak.append((floor10(lb),m))
    assert direct+done+len(weak)==2**(n-k-1)
    return direct,done,sorted(weak),[z.bit_length() for z in roots]


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--index',required=True,type=Path)
    p.add_argument('--key',action='append',nargs=2,type=int,required=True);p.add_argument('--head',default=96,type=int)
    a=p.parse_args(); finder=Finder(Bank(a.index),0)
    for p,e in a.key:
        direct,done,weak,bits=quick(finder,p,e,a.head)
        print(p,e,'direct',direct,'basic forest',done,'remaining',len(weak),'weakest',weak[:6],'strongest',weak[-4:],'forced bits',bits,flush=True)


if __name__=='__main__':main()
