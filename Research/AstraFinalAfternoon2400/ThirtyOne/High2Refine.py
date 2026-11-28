"""Anonymous no-prime-label size masks for exact (31,2) high remaining firsts."""
from functools import cache
from itertools import product
from math import gcd,isqrt
from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from Replay import B, state, prime_small, sigma, valuation
from AnonymousEuler import possible_factor


@cache
def rough(p,l,Z):
    lim=10**8
    assert prime_small(l) and p%l!=1 and Z%(2*l)==1 and isqrt(Z)**2!=Z and pow(2,Z-1,Z)!=1
    assert all(Z%k for k in range(2*l+1,lim+1,2*l))
    return lim+1


def scan(e):
    assert e in (192,400)
    x,s,d,bs,ok=state(((31,2),(331,e)));assert ok
    a=bs[1];l=e+1;lim=rough(331,l,a)
    assert d==3*a and gcd(a,3)==1 and a%4 in (1,3) and valuation(s,331)==1 and valuation(s,31)==0
    cs={}
    # 3^2 is compulsory, regardless of all Euler positions. For an exterior
    # Euler q the nonsquare large block requires a further ordinary factor.
    for i,j in product(range(3),range(e)):
        m=31**i*331**j;q0=2*m-1;Q=max(q0,5)
        inner=possible_factor(a,l,q0,m) if not j else None
        # For positive j, reciprocal q (1 mod4) sees 331 (3 mod4) as a nonsquare,
        # whereas sigma(331^e) has odd primitive order at q.
        for alpha in (1,5):
            mask=0
            if inner is not None and 9*x*max(a,inner**alpha)<=B:mask|=1
            if 9*x*a*lim*Q**alpha<=B and 2*x*Q**(alpha+1)<=3*B:mask|=2
            cs[alpha,mask]=cs.get((alpha,mask),0)+1
    assert sum(cs.values())==6*e
    return [(a,m,v) for (a,m),v in sorted(cs.items())]

if __name__=='__main__':
    assert __debug__
    for e in (192,400):print(json.dumps({'first':e,'masks':scan(e)}),flush=True)
