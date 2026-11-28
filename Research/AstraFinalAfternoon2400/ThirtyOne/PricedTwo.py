"""Exact non-Euler and Euler-first windows for anonymous high (31,2) branches."""
from functools import cache
from itertools import product
from math import gcd,isqrt
from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from Replay import B, BANNED, SMALL, state, prime_small, roots, valuation
from High2Refine import rough
from AnonymousEuler import possible_factor


@cache
def deficits(row):
    x,s,d,bs,ok=state(row);assert ok and prime_small(331)
    c=row[-1][1]-1;t=331
    assert 331-1==2*3*5*11 and valuation(s,t)==1 and 3**330>=t*t
    # 331-LTE length budget t^k−1 fits independently of base-order budget.
    # Joint 31 omitted here, so no shared charge or divisibility premise.
    os=tuple(o for o in range(3,t,2) if (t-1)%o==0)
    loss={}
    excluded=(*BANNED,*dict(row))
    def maybe(y):return y>=3 and y%2 and y not in excluded and all(y==k or y%k for k in SMALL) and pow(2,y-1,y)==1
    for o in os:
        h=o-1
        if 3**h>=t**(2*c):continue
        for m,rr in roots(t,o,c)[1:]:
            goal=m*m
            for y in rr:
                if y<3 or not y%2 or (y.bit_length()-1)*h>=goal.bit_length():continue
                size=y**h
                if size>=goal or x*d*(size//gcd(d,size))>B:continue
                q=isqrt(y)
                if not (maybe(y) or q*q==y and q%4==1 and maybe(q)):continue
                pv=loss.get(y)
                if pv is None or goal*pv[1]>pv[0]*size:loss[y]=goal,size
    U=10**8
    for p,q in loss.values():U=-(-(U*p)//q)
    return -(-U//10**8),len(loss)


def check(e):
    row=((31,2),(331,e));x,s,d,bs,ok=state(row);assert ok
    a=bs[1];l=e+1;lim=rough(331,l,a)
    U,labels=deficits(row)
    assert e in (192,400) and d==3*a and valuation(s,31)==0
    count={};remain=[]
    for i,j in product(range(3),range(e)):
        m=31**i*331**j;q0=2*m-1;Q=max(5,q0);R=331**(2*(e-1-j))
        inside=possible_factor(a,l,q0,m) if not j else None
        for alpha in (1,5):
            mask=0
            if x*Q*R<=B*U:
                if inside is not None and 9*x*max(a,inside**alpha)<=B:mask|=1
                if 9*x*a*lim*Q**alpha<=B and 2*x*Q**(alpha+1)<=3*B:
                    # A known ordinary 3^h might be the emitter r. Its exact
                    # component cannot overlap the anonymous A; cap for gcd
                    # against D therefore at most max(3,A), no factor 9 included.
                    # True q outside D implies a source with r^h > 2QY/3.
                    if 4*x*x*d*Q**(alpha+3)*R<=9*B*B*U*max(3,a):mask|=2
            if mask:remain.append((i,j,alpha,mask))
            count[alpha,mask]=count.get((alpha,mask),0)+1
    return dict(first=e, loss_labels=labels, U_digits=len(str(U)),summary=[(a,m,n) for (a,m),n in sorted(count.items())],residual=remain)

if __name__=='__main__':
    import argparse
    assert __debug__
    a=argparse.ArgumentParser();a.add_argument('first',type=int,nargs='*',default=[192,400]);p=a.parse_args()
    for e in p.first:
        r=check(e);t=r.pop('residual');print(json.dumps(r),flush=True)
        from hashlib import sha256
        print('residual',len(t),sha256(json.dumps(t,separators=(',',':')).encode()).hexdigest(),flush=True)
