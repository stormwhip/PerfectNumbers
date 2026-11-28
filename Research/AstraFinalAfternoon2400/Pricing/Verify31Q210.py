#!/usr/bin/env python3
"""Strict joint-price closure of first-pivot 3229^156 and 3229^210 at (31,268)."""
import argparse
from itertools import product
from math import gcd
from pathlib import Path
from hashlib import sha256
import runpy

HERE=Path(__file__).resolve().parent
Q=3229
P=31
B=10**2400


def need(ok,why):
    if not ok:raise ValueError(why)


def main():
    source=HERE.parent/'ThirtyOne'/'Replay.py'
    digest=sha256(source.read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    need(digest=='2d8040567afcc1775d83b15528047cc22adf29d4301c5d5374e2e34a5275f0ce','pricing kernel LF hash')
    V=runpy.run_path(str(source))
    need(__debug__ and V['B']==B and V['P']==P and V['BANNED']==(19,7,11),'same canonical prefix and bound')
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--pivot',type=int,choices=(156,210),default=210)
    f=ap.parse_args().pivot
    rows=((P,268),(Q,f))
    x,s,d,blocks,ok=V['state'](rows)
    need(ok and V['prime_small'](P) and V['prime_small'](Q) and V['valuation'](blocks[0],Q)==1 and s%P and s%(Q*Q),'verified fixed target domains')
    need(gcd(blocks[0]//Q,blocks[1])==1 and d==(blocks[0]//Q)*blocks[1],'mandatory product, exact support split')
    a,b=19,10
    need(f in (156,210) and all((q%4==3 or q%4==1) and h%2==0 for q,h in rows),'open Euler prefix')
    # Separate arithmetic fixes the order of the expensive tests and keeps
    # the mandatory-overlap test in ordinary rather than powered units.
    fast=runpy.run_path(str(HERE/'FastTwoPrice.py'))
    U,demands,entries=fast['priced_atoms'](V,rows,a,b)
    print('Certified complete priced atom support:',entries,flush=True)
    need(demands==[268,f-1] and U>=1,'price residual supply')
    # A holder q of the unique Euler exponent is not already fixed;
    # it either divides D, hence one block, or is an extra prime outside D.
    qcap=max(B//(x*d),blocks[0]//Q,blocks[1])
    nominal=x**b*(P**demands[0]*Q**demands[1])**a
    if f==210:
        need(nominal>B**b*U*qcap**(a-b),'strict uniform Euler cap inequality')
        need(nominal>B**b*U*qcap**(a-b)*10**(200*b),'uniform price reserve at least 200 digits')
    else:
        assert f==156
        A,C=blocks[0]//Q,blocks[1]
        K=max(A,C)
        lim=B**b*U
        one=nominal*(x*d)**(a-b)*2**a
        two=B**a*U*K**(a-b)*3**a
        # Since m≤q, a common q-threshold discharges the entire
        # exterior case before the finite inner residue comparisons.
        # Binary search is exact and only needs the powers q^(a−b),q^a.
        lo,hi=0, B//x+1
        while lo+1<hi:
            mid=(lo+hi)//2
            if nominal>lim*mid**(a-b):lo=mid
            else:hi=mid
        none_external=(lo>=B//(x*d) or one*(lo+1)**a>two)
        pp=[P**i for i in range(demands[0]+1)]
        qq=[Q**j for j in range(demands[1]+1)]
        left=[]; visited=0
        for i,j in product(range(len(pp)),range(len(qq))):
            m=pp[i]*qq[j];q0=max(5,2*m-1)
            if m<=lo:continue
            if nominal*q0**b>lim*m**a:continue
            if not none_external and x*d*q0<=B and one*q0**(2*a)<=two*m**a:
                left.append((i,j,'outside'));continue
            for s,C0 in enumerate((A,C)):
                if (i and s==0) or C0<q0:continue
                u=C0*pow(2*m-1,-1,4*m)%(4*m) or 4*m
                hi=C0//q0
                if u>hi:continue
                if (hi-u)//(4*m)<20 and all(C0%z for z in range(u,hi+1,4*m)):continue
                left.append((i,j,s));break
            visited+=1
        need(not left,('uncovered Euler cells',len(left),left[:10]))
        print('Exact internal residue checks:',visited,flush=True)
    print('EXCLUDED 31^268,3229^'+str(f)+' by exact joint Euler bound; loss components:',entries,flush=True)
    print('Dependency LF SHA256:',digest)


if __name__=='__main__':main()
