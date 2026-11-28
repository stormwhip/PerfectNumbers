#!/usr/bin/env python3
"""Exact replay: the compulsory cofactor r in BASE must have exponent 2."""
from fractions import Fraction
from functools import cache
from math import gcd, prod
from pathlib import Path
from hashlib import sha256
import runpy

here = Path(__file__).resolve().parent
rare = runpy.run_path(str(here/'RareTarget13.py'))
BASE, B, R, X0 = (rare[k] for k in ('BASE','B','R','X0'))
sigma, vp, need, prime_trial = (rare[k] for k in ('sigma','vp','need','prime_trial'))


def main():
    need(__debug__, 'dependent net-price verifier requires assertions enabled')
    src=here.parent/'Nineteen'/'Net13.py'
    need(sha256(src.read_bytes().replace(b'\r\n',b'\n')).hexdigest()=='765a641acce03dd08eb52a46e98cf99f18c4c061f16562af359044194eec735d', 'audited 19/13 net-price dependency')
    V=runpy.run_path(str(src))
    need(tuple(V['PREFIX'])==BASE and V['B']==B and V['X']==X0, 'matching baseline')
    need(rare['uniform_rare'](), 'uniform rare price at 77/20')
    Y=V['S']; D=Y//gcd(X0,Y)
    Q=(67,967,8311,11621,50627,392233)
    need(vp(Y,R)==1 and D%R==0,'r forced with fixed incoming valuation exactly one')
    need(all(prime_trial(q) and q not in dict(BASE) and D%q==0 for q in Q), 'compulsory prime primality and divisor')
    for q in Q:
        # If q had supplied 5-order, the 19/13-only gain cannot be used
        # without subtracting its exact rare supply. Here all are inactive.
        need(q%R!=1 and pow(q,5,R)!=1,('compulsory prime not rare-inactive',q))
    V0=V['baseprice']()*prod(V['gain'](q,vp(Y,q))[0] for q in Q)
    C,H=V['C'],V['D13']
    h=next(h for h in range(2,5031,2) if X0*R**h>B)
    passed=0
    for a in range(4,h,2):
        sig=sigma(R,a)
        if vp(sig,19)>C or vp(sig,13)>H:
            continue
        price=V0*V['atom'](R,a)
        # price is a lower bound on N^10 before charging r. After reserve
        # from the exterior components, square it and charge r^(77*(a-1)).
        # Distinct compulsory bases cannot provide r; r itself provides zero.
        need(price.numerator**2 * rare['rare_cost20'](a-1) > B**20 * price.denominator**2, ('open r exponent',a))
        passed+=1
    need(passed==len(range(4,h,2)), 'unaccounted compatible parity window')
    print('EXCLUDED r even exponents 4..'+str(h-2)+' by exact three-target net price; r >= '+str(h)+' by strict raw X0 tail; only r^2 remains')


if __name__=='__main__':
    main()
