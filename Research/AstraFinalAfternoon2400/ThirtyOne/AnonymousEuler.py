"""Complete finite allocation/special-position bounds for hard first fibers.

This scans only target supply allocations. A positive remaining mask is not a
claim that a matching prime q actually exists, nor that the fiber is closed.
"""
from functools import cache
from hashlib import sha256
from math import gcd,isqrt
from itertools import product
from pathlib import Path
import argparse,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from Replay import B, state, prime_small, atoms

LIM=10**8


@cache
def prove_block(z,h,Z):
    ell=h+1
    assert prime_small(ell) and z%ell!=1 and Z%(2*ell)==1
    assert isqrt(Z)**2!=Z and pow(2,Z-1,Z)!=1
    assert all(Z%q for q in range(2*ell+1,LIM+1,2*ell))


def lower_progression(r,m,L):
    return r+max(0,(L-r+m-1)//m)*m


def possible_factor(Z, ell, q0, m):
    # Real Euler divisor is 1 mod 4ell, so q≡1 mod ell in addition to q0 mod 4m.
    # m uses only 31 and 3229. The cofactor's unique compatible residue is checked too.
    mod=4*m;assert gcd(mod,ell)==1
    period=mod*ell
    r=q0+mod*((1-q0)*pow(mod,-1,ell)%ell)
    assert r%ell==1 and r%mod==q0 and gcd(r,period)==1
    Q=lower_progression(r,period,LIM+1)
    # Z is composite; if q is a prime divisor then cofactor k>1 and k>LIM.
    C0=Z*q0%mod
    C1=C0+mod*((Z-C0)*pow(mod,-1,ell)%ell)
    C=lower_progression(C1,period,LIM+1)
    if C*Q>Z or ((C+period)*Q>Z and Z%C):
        return None
    return Q


def necessary(e,f,price):
    row=((31,e),(3229,f));x,s,d,bs,ok=state(row)
    assert ok and e==268 and f in (102,156,210) and gcd(bs[0]//3229,bs[1])==1
    a,b=bs[0]//3229,bs[1]
    assert d==a*b
    for (z,h),Z in zip(row,(a,b)):
        prove_block(z,h,Z)
    assert e==268 and f<=210
    assert not (s%31==0 or s%3229**2==0)
    U=1;WN,WD=(9,5)
    if price:
        U,need,labels=atoms(row,(31,3229),WN,WD)
        assert need==[e,f]
    pp=[31**j for j in range(e+1)];tt=[3229**j for j in range(f+1)]
    shape={};survivors=[]
    if price:
        fine=B**WD*U
        side=3**WN*B**WN*U*max(a,b)**(WN-WD)
        dd=d**(WN-WD)
    for i,j in product(range(e+1),range(f+1)):
        m=pp[i]*tt[j]; q0=2*m-1
        Q=max(5,q0)
        # q^alpha, alpha=1 or alpha>=5: monotone in alpha. Keep the two
        # classes separate, in each case checking only its least possible alpha.
        q_a=possible_factor(a,e+1,q0,m) if not i else None
        q_b=possible_factor(b,f+1,q0,m)
        for alpha in (1,5):
            mask=0
            a_e=q_a**alpha if q_a is not None else 0
            b_e=q_b**alpha if q_b is not None else 0
            # q^alpha can overlap its own D block. Taking max avoids assuming
            # either the exponent or the unresolved block is square-free.
            if q_a is not None and x*b*(LIM+1)*max(a,a_e)<=B:
                mask|=1
            if q_b is not None and x*a*(LIM+1)*max(b,b_e)<=B:
                mask|=2
            if x*d*(LIM+1)**2*Q**alpha<=B and 2*x*Q**(alpha+1)<=3*B:
                mask|=4
            if price:
                mass=pp[e-i]*tt[f-j]
                if (x*Q)**WD*mass**WN>fine:
                    mask=0
                elif mask&4:
                    # Count r^h supplying q and part of mass as in Replay,
                    # with overlap capped by the larger coprime block of D.
                    if (2*x*Q*Q)**WN*dd*mass**WN>side:
                        mask-=4
            shape[str(alpha),mask]=shape.get((str(alpha),mask),0)+1
            if mask:survivors.append((i,j,alpha,mask))
    assert sum(shape.values())==2*(e+1)*(f+1)
    return dict(f=f,price=price,counts=[[k[0],k[1],v] for k,v in sorted(shape.items())],
                survivors_digest=sha256(json.dumps(survivors,separators=(',',':')).encode()).hexdigest())


if __name__=='__main__':
    assert __debug__;ap=argparse.ArgumentParser();ap.add_argument('--price',action='store_true');ap.add_argument('--first',nargs='+',type=int,default=(102,156,210));args=ap.parse_args()
    for f in args.first:print(json.dumps(necessary(268,f,args.price)),flush=True)
