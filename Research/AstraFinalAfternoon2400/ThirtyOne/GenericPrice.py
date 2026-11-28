"""Exact one-target pricing (requires already certified prime labels)."""
from fractions import Fraction
from functools import cache
from itertools import product
from math import gcd,isqrt,prod,lcm
from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from Replay import B, BANNED, SMALL, state, external, valuation, exclusive_components, odd_lifts, max_positive_base

T=917087137
Q=20668766888345125939752429067
W=1382896061
Z=142399308228250619911869629856705143726156604422206306519
FACTORS={T:[2]*5+[3,7,7,19,31,331], Q:[2,3,7,7,11,13,61,73,1097,4597,2805637,7803077],
         W:[2,2,5,7,13,759833], Z:[2,3,7,7,11,13,23,61,73,1097,4597,18749,2805637,126703781,7803077,126094978615129],
         108744349334141:[2,2,5,13,17,19,3229,401017],
         334965754217463378346093:[2,2,3,7,19,41,5118982734541588397],
         2018177869:[2,2,3,7,83,289469]}


@cache
def domain(t):
    # Certifier verifies every fixed prime independently; these assertions then
    # ensure the odd divisors below are all possible orders of interest.
    from ForestVerify import C
    fs=FACTORS[t]
    assert t-1==prod(fs) and all(C.pc.prime64(q) for q in fs)
    assert t>8000 and 3**8000>B
    if t<2**64:assert C.pc.prime64(t)
    divisors={1}
    for p in fs:
        if p%2:divisors|={x*p for x in divisors if x*p<=8000}
    return tuple(sorted(divisors-{1}))


@cache
def roots(t,o,c):
    g0=next(g for g in range(2,t) if all(pow(g,(t-1)//q,t)!=1 for q in set(FACTORS[t])))
    g=pow(g0,(t-1)//o,t);m=t
    for q in set(FACTORS[t]):
        if o%q==0:assert pow(g,o//q,t)!=1
    assert pow(g,o,t)==1
    out=[]
    indices=[j for j in range(1,o) if gcd(j,o)==1]
    for i in range(c):
        assert pow(g,o,m)==1
        rr=[];r=1
        for j in range(1,o):
            r=r*g%m
            if gcd(j,o)==1:rr.append(r)
        assert len(rr)==len(set(rr))==len(indices)
        out.append((m,tuple(rr)))
        m*=t;g=pow(g,t,m)
    return tuple(out)


def upperloss(row,t,hmap,w,skip_order3=False):
    """Enumerate all losses, or deliberately decline (OverflowError)."""
    x,s,d,_,ok=state(row);assert ok
    fixed=any(h%2 for _,h in row);cap=B//(x*d)
    need=dict(row)[t]-valuation(s,t);a,b=w.numerator,w.denominator
    loss={}
    def maybe(v):return v>=3 and v%2 and v not in dict(row) and v not in BANNED and all(v==k or v%k for k in SMALL) and pow(2,v-1,v)==1
    for o in domain(t):
        if skip_order3 and o==3:continue
        h=hmap[o]*b
        if not h:raise OverflowError('not positive reserve')
        if 3**h>=t**(need*a):continue
        # Cut by global budget on X y^hmap, even if atom overlaps D.
        bcap=max_positive_base(B//x+1,hmap[o])
        for m,rr in roots(t,o,need):
            goal=m**a
            hi=min(bcap,max_positive_base(goal,h)) if h<a else None
            for r in rr:
                if h<a:
                    vv=odd_lifts(r,m,hi)
                    if max(0,(vv.stop-1-vv.start)//vv.step+1)>50000:raise OverflowError('large high-weight AP: no exclusion')
                else: vv=(r,)
                for y in vv:
                    if y<3 or not y%2 or (y.bit_length()-1)*h>=goal.bit_length():continue
                    size=y**hmap[o]
                    fee=size**b
                    if fee>=goal or size//gcd(size,d)>cap:continue
                    z=isqrt(y)
                    if not (maybe(y) or not fixed and z*z==y and z%4==1 and maybe(z)):continue
                    prev=loss.get(y)
                    if not prev or prev[0]*fee<goal*prev[1]:loss[y]=(goal,fee)
    U=10**8
    for n,dn in loss.values():U=-(-(U*n)//dn)
    return need,-(-U//10**8),len(loss)


def one(row,t,w):
    x,s,d,blocks,ok=state(row); assert ok
    assert 1<=w<=3
    need,U,count=upperloss(row,t,{o:o-1 for o in domain(t)},w)
    wn,wd=w.numerator,w.denominator; price_cap=B**wd*U
    if any(h%2 for _,h in row):
        return [] if x**wd*t**(wn*need)>price_cap else [-1],count
    assert wn>=wd
    H=max(exclusive_components(blocks,x),default=1)
    V=3**wn*B**wn*U*H**(wn-wd)
    D=d**(wn-wd)
    out=[]
    for j in range(need+1):
        m=t**j;q=2*m-1;R=t**(wn*(need-j))
        if (x*q)**wd*R>price_cap:continue
        if not all((p==t and t%4==3 and j>0) or external(z,m) for (p,_),z in zip(row,blocks)):
            out.append((j,'internal'));continue
        if x*d*q>B or (2*x*q*q)**wn*D*R>V:continue
        out.append((j,'external'))
    return out,count


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);args=p.parse_args()
    for rr,score in json.loads(args.source.read_bytes())['unresolved']:
        r=tuple(map(tuple,rr)); seen=[]
        for t,h in r:
            if t not in FACTORS:continue
            for w in [Fraction(9,5),Fraction(2),Fraction(5,2),Fraction(3)]:
                try:ret,n=one(r,t,w)
                except OverflowError:continue
                seen.append((t,str(w),ret,n))
                if not ret:break
            if seen and not seen[-1][2]:break
        print(json.dumps({'row':rr,'windows':seen}),flush=True)
