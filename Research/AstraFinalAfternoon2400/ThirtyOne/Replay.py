"""Exact-integer first domains, conservative joint atom prices, optional finite high-weight progressions."""
from fractions import Fraction
from functools import cache
from hashlib import sha256
from itertools import product
from math import gcd, isqrt, prod
from pathlib import Path
import argparse
import json

B = 10**2400
P = 31
BANNED = (19, 7, 11)
EXPECTED = {2:'P31_I00000', 6:'P31_I00002', 268:'P31_I00055',
            456:'P31_I00086', 466:'P31_I00089'}
SMALL = (3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97)
HERE = Path(__file__).resolve().parent


def sigma(p, e):
    return (p**(e+1)-1)//(p-1)


def valuation(n, p):
    assert n > 0 and p > 1
    k = 0
    while n%p == 0:
        n //= p
        k += 1
    return k


def strip(n, support):
    while (g:=gcd(n,support)) > 1:
        n //= g
    return n


def prime_small(n):
    return n>1 and all(n%d for d in range(2,isqrt(n)+1))


@cache
def state(prefix):
    assert prefix[0][0] == P and len({p for p,e in prefix}) == len(prefix)
    x = prod(p**e for p,e in prefix)
    blocks = tuple(sigma(p,e)//(1+e%2) for p,e in prefix)
    assert all(z%2 for z in blocks)
    s = prod(blocks)
    d = strip(s,x)
    valid = (all(p not in BANNED and (not e%2 or p%4==e%4==1) for p,e in prefix)
             and sum(e%2 for p,e in prefix) <= 1
             and gcd(s,prod(BANNED)) == 1 and s*prod(1+e%2 for p,e in prefix)<=2*x
             and all(valuation(s,p)<=e for p,e in prefix) and x*d<=B)
    return x, s, d, blocks, valid


def split(prefix, t):
    x,s,d,_,ok = state(prefix)
    assert ok and t not in dict(prefix) and t not in BANNED
    v = valuation(d,t)
    assert v > 0
    out = []
    f = v
    z = x*(d//t**v)*t**f
    while z <= B:
        if not f%2 or t%4==f%4==1:
            row = prefix+((t,f),)
            if state(row)[-1]:
                out.append(row)
        f += 1
        z *= t
    return out, f


@cache
def roots(t, order, c):
    """Independently obtain all simple lifts, digit by digit (not powering the old lift)."""
    assert c >= 0 and (t-1)%order == 0 and order>1
    divisors=[d for d in range(1,order) if order%d==0]
    level=tuple(r for r in range(1,t) if pow(r,order,t)==1
                and all(pow(r,d,t)!=1 for d in divisors))
    out=[(1,(0,))]
    m=t
    for depth in range(1,c+1):
        out.append((m,level))
        if depth==c:
            break
        step=m*t
        level=tuple(r+m*(-((pow(r,order,step)-1)//m)
                          *pow(order*pow(r,order-1,t),-1,t)%t) for r in level)
        assert all(0<r<step and pow(r,order,step)==1 for r in level)
        m=step
    return tuple(out)


def max_positive_base(goal, h):
    """Return largest integer y with y^h < goal, including equality guard."""
    if h==2:
        return isqrt(goal-1)
    lo,hi=0,1 << ((goal.bit_length()+h-1)//h)
    while hi-lo>1:
        m=(lo+hi)//2
        if m**h<goal:
            lo=m
        else:
            hi=m
    return lo


def odd_lifts(r, modulus, upper):
    """All odd y>=3 over r modulo odd modulus; never just the least lift."""
    assert modulus%2 and 0<=r<modulus
    k=max(0,-((r-3)//modulus))
    if (r+k*modulus)%2==0:
        k+=1
    return range(r+k*modulus,upper+1,2*modulus)


def crt(r,m,s,n):
    return r+m*((s-r)*pow(m,-1,n)%n) if n>1 else r


def atoms(prefix, targets, wn=2, wd=1):
    """Price denominator-power U for common weight wn/wd <= 2."""
    assert 0<wn<=2*wd
    x,s,d,_,ok=state(prefix)
    assert ok and len(targets) in (1,2)
    fixed=any(e%2 for p,e in prefix)
    prizes=[]
    for t in targets:
        assert prime_small(t) and t in dict(prefix) and 3**(t-1)>=t*t
    odds=[tuple(o for o in range(3,t,2) if (t-1)%o==0) for t in targets]
    assert all(all(o%t for t in targets) for os in odds for o in os)
    for o,p in product(*odds) if len(odds)==2 else ():
        h=(2 if 3 in (o,p) else 0)+(0 if o==3 else o-3)+(0 if p==3 else p-3)
        assert h<=o*p//gcd(o,p)-1
    needs=[dict(prefix)[t]-valuation(s,t) for t in targets]
    cap=B//(x*d)
    banned=(*BANNED, *dict(prefix))
    def prime_maybe(y):
        return y>=3 and y%2 and y not in banned and all(y==k or y%k for k in SMALL) and (y.bit_length()>128 or pow(2,y-1,y)==1)
    loss={}
    def add(y,h,goal):
        if y<3 or not y%2:
            return
        v=y**h
        if v>=goal or v//gcd(v,d)>cap:
            return
        # Fermat is only necessary. It is deferred on large candidates in
        # weight-two mode; rationally sparse scans can afford the full test.
        r=isqrt(y)
        if not prime_maybe(y) and (fixed or r*r!=y or r%4!=1 or not prime_maybe(r)):
            return
        old=loss.get(y)
        if old is None or goal*old[1]>old[0]*v:
            loss[y]=(goal,v)
    # Joint order 3: independent optional contributions (zero depth = no modulus).
    cs=[roots(t,3,k) for t,k in zip(targets,needs)]
    if len(cs)==1:
        cs.append(((1,(0,)),))
    def rounded_upper(factors):
        # Repeated upward rounding preserves a universal bound and avoids
        # cancellation of products of very large denominators.
        scale=10**8;u=scale
        for numerator,denominator in factors:
            u=-(-(u*numerator)//denominator)
        return -(-u//scale)
    for n,bb in cs[1]:
        inv,step=1,(pow(targets[0],-1,n) if n>1 else 0)
        for m,aa in cs[0]:
            # Required y < m*n, hence no additional representatives.
            bound=m*n
            q=bound**wn
            for r,z in product(aa,bb):
                y=r+m*((z-r)*inv%n)
                if wn<2*wd and y.bit_length()>(q.bit_length()+2*wd-1)//(2*wd)+1:
                    continue
                add(y,2*wd,q)
            inv=inv*step%n
    prizes.append(('joint3',len(loss),rounded_upper(loss.values())))
    for t,c,os in zip(targets,needs,odds):
        loss={}
        for o in os:
            if o==3:
                continue
            h=(o-3)*wd
            if 3**h>=t**(wn*c):
                continue
            for m,aa in roots(t,o,c)[1:]:
                goal=m**wn
                assert h>=wn # power test requires y<m or smaller
                for r in aa:
                    add(r,h,goal)
        prizes.append((str(t),len(loss),rounded_upper(loss.values())))
    return prod(p[2] for p in prizes), needs, [(p[0],p[1]) for p in prizes]


def external(z,m):
    q=2*m-1
    hi=z//q
    residue=z*q%(4*m) # q^2 = 1 modulo 4m
    first=residue or 4*m
    return first>hi or (first+4*m>hi and z%first!=0)


def exclusive_components(blocks, x):
    pending=[strip(z,x) for z in blocks]
    out=[]
    while pending:
        a=pending.pop()
        if a==1:
            continue
        intersect=[z for z in pending if gcd(a,z)>1]
        if not intersect:
            out.append(a)
        else:
            for z in intersect:
                pending.remove(z)
                a*=z
            pending.append(a)
    assert prod(out)==prod(strip(z,x) for z in blocks)
    assert all(gcd(a,b)==1 for i,a in enumerate(out) for b in out[i+1:])
    return out


def price(prefix, targets, wn=2, wd=1):
    x,s,d,bs,ok=state(prefix)
    assert ok
    u,needs,counts=atoms(prefix,targets,wn,wd)
    factor = prod(t**c for t,c in zip(targets,needs))
    price_cap=B**wd*u
    if any(e%2 for p,e in prefix):
        return ([] if x**wd*factor**wn>price_cap else ['fixed-euler']), counts
    h=max(exclusive_components(bs,x),default=1)
    windows=[]
    for alloc in product(*(range(c+1) for c in needs)):
        m=prod(t**c for t,c in zip(targets,alloc))
        q=2*m-1
        rest=(factor//m)**wn
        if (x*q)**wd*rest>price_cap:
            continue
        # For a 3 mod 4 fixed prime, positive inflow makes the Euler base exterior
        # by reciprocity: its order in the fixed sum has to be odd.
        a=dict(zip(targets,alloc))
        if not all((p%4==3 and a.get(p,0)>0) or external(z,m) for (p,_),z in zip(prefix,bs)):
            windows.append((alloc,'possibly-internal'))
            continue
        if x*d*q>B:
            continue
        # For w >= 1 eliminate Y from 2XD Q^2 Y < 3BH and
        # (2XQ^2)^wd * rest < 3^wd B^wd U * Y^(wn-wd).
        if wn>=wd and (2*x*q*q)**wn*d**(wn-wd)*rest>3**wn*B**(wn-wd)*price_cap*h**(wn-wd):
            continue
        windows.append((alloc,'external'))
    return windows, counts


def high_regression():
    # PR #11's exact hazard: odd valid candidates occur beyond the least residue.
    p=19; order=3; w=6
    m, rr=roots(p,order,1)[1]
    u=max_positive_base(m**w,order-1)
    got=sorted(y for r in rr for y in odd_lifts(r,m,u))
    expected=[y for y in range(3,u+1,2) if pow(y,order,m)==1 and y%m!=1]
    assert u==6858 and got==expected and any(y>m and prime_small(y) for y in got)
    # Strict bound and parity at endpoints, roots completeness against brute force.
    for p,o,z in [(7,3,3),(19,3,2),(31,5,2)]:
        for modulus,rr in roots(p,o,z)[1:]:
            assert len(rr)==len(set(rr))
            assert set(rr)=={r for r in range(1,modulus) if pow(r,o,modulus)==1 and
                             all(pow(r,d,p)!=1 for d in range(1,o) if o%d==0)}
            for a,b,h in [(1,1,2),(2,1,2),(3,2,4)]:
                u=max_positive_base(modulus**a,h*b)
                assert u**(h*b)<modulus**a<=(u+1)**(h*b)
                assert sorted(y for r in rr for y in odd_lifts(r,modulus,u))==[y for y in range(3,u+1,2) if y%modulus in rr]
    return len(got)


def ledger():
    j=json.loads((HERE.parents[1]/'FinalNight2400/OpenFrontier.json').read_bytes())
    assert j['RemainingByRoot']['31']==list(EXPECTED)
    rows={k:v for k,v in j['ShardRemainders'].items() if k.startswith('P31')}
    assert rows=={s:[[31,e]] for e,s in EXPECTED.items()}
    return rows


def key(e):
    prefix=((P,e),)
    assert state(prefix)[-1]
    if e==268:
        t=3229
        assert prime_small(t) and valuation(sigma(P,e),t)==1
        return t,*split(prefix,t)
    if e==2:
        assert sigma(31,2)==3*331 and prime_small(3) and prime_small(331)
        return 331,*split(prefix,331)
    if e==6:
        t=917087137
        assert sigma(31,6)==t and prime_small(t)
        return t,*split(prefix,t)
    return None,[prefix],None


def main():
    assert __debug__ and 3**8000>B and (2*3229+1)**(3229-1)>B
    pa=argparse.ArgumentParser()
    pa.add_argument('--key',type=int,default=268,choices=EXPECTED)
    pa.add_argument('--domain-only',action='store_true')
    pa.add_argument('--first',type=int)
    pa.add_argument('--weight',type=Fraction,default=Fraction(2))
    args=pa.parse_args()
    k=args.key
    print(json.dumps({'shards':ledger(),'high_weight_19_regression_candidates':high_regression()}),flush=True)
    t,domain,tail=key(k)
    exponents=[r[-1][1] for r in domain]
    print(json.dumps({'key':[31,k], 'pivot':t, 'tail':tail,'direct_count':len(domain),'direct':exponents}),flush=True)
    if args.domain_only:
        return
    rows={}
    assert args.first is None or args.first in exponents
    for r in domain:
        if args.first is not None and r[-1][1]!=args.first:
            continue
        targets=(31,3229) if k==268 else (31,)
        windows,cs=price(r,targets,args.weight.numerator,args.weight.denominator)
        rows[r[-1][1]]=windows
        print(json.dumps({'prefix':r,'loss_labels':cs,'surviving_windows':len(windows), 'closed':not windows}),flush=True)
    print(json.dumps({'closed':[r for r,w in rows.items() if not w], 'open':[r for r,w in rows.items() if w],
          'window_digest':sha256(json.dumps(rows,separators=(',',':')).encode()).hexdigest()},separators=(',',':')),flush=True)


if __name__=='__main__':
    main()
