"""Exact integer Euler-one source/cost pilot on root-three prime index blocks.

Only used where the independently replayed root audit has ruled out high Euler,
physical root factors below 100000 are absent, and all remaining s are positive.
Run with Python -I -S -B (no factor database, package or network required).
"""
from functools import cache, lru_cache
from math import isqrt, gcd
from time import monotonic
from itertools import accumulate
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from Scout import E,J,V,HERE,frontier

B = V.B
I = J.I
BN = I.BAN
FREE_LIMIT = 16


def require(x,msg):
    if not x:
        raise ValueError(msg)


def ceildiv(n,d):
    return (n+d-1)//d


@lru_cache(maxsize=12000)
def iroot(n,k):
    if n<2 or k==1:
        return n
    if k==2:
        return isqrt(n)
    x = 1 << ((n.bit_length()+k-1)//k)
    while True:
        y=((k-1)*x+n//x**(k-1))//k
        if y>=x:
            return x
        x=y


def crt_divisor(a,c,lo,hi,step,res=1,cap=24):
    """Return True if a divisor in the box is possible; wide boxes stay open."""
    lo=lo+(res-lo)%step
    hi=hi-(hi-res)%step
    if lo>hi:
        return False
    if hi-lo<cap*step:
        return any(a%z**c==0 for z in range(lo,hi+1,step))
    if gcd(step,res)>1:
        return True
    wr=a*pow(res,-c,step)%step
    w0=ceildiv(a,hi**c)
    w0+=(wr-w0)%step
    w1=a//lo**c
    if w0>w1:
        return False
    if w1-w0<cap*step:
        return any(a%w==0 and (r:=iroot(a//w,c))**c*w==a and lo<=r<=hi and r%step==res%step
                   for w in range(w0,w1+1,step))
    return True


def strip_lower(a,m,span):
    base = 1 + 2*m*((I.T-1)//(2*m)+1)
    for r in range(base,base+2*m*span,2*m):
        if a%r==0:
            return r
    return base+2*m*span


def minimum_odd_square_multiplier(a, floor, m, ntry):
    """A*sf(A) is the least square multiple of A; inspect a bounded exact prefix."""
    if isqrt(a)**2==a:
        return 1
    # Every prime dividing A is 1 mod 2m, and sf(A)=A mod 8.
    step=8*m
    r=1+2*m*(((a-1)//2)*pow(m,-1,4)%4)
    z=floor+(r-floor)%step
    for k in range(z,z+ntry*step,step):
        # sf(A) necessarily divides A. This also avoids almost all square roots.
        if a%k==0 and isqrt(a//k)**2*k==a:
            return k
    return z+ntry*step


@cache
def free_levels(a, m, small):
    """Upper bound on prepaid units from repeated prime powers.

    A free j with f>=3^j-1 and f<=c requires c>=2j. Strike the short
    prefix of plausible r with r^2∤A before pricing these free units.
    """
    step=6*m
    lo=1+step*((small-1)//step+1)
    hi=lo+step*FREE_LIMIT
    for z in range(lo,hi,step):
        if a%(z*z)==0:
            hi=z
            break
    # If r^c|A and c is odd, f=(c+1) gets a parity unit for free only if
    # 3 | c+2; that unit is funded separately by ordinary tariff below.
    return J.powerlog(a,hi*hi),hi


@cache
def ordinary_prices(t, cap, nmax):
    standard=tuple(sorted(J.pricebase()))
    if cap>(I.T+1)**2 or t<=0 or nmax<0:
        raise ValueError('invalid ordinary price cap')
    return tuple(x for x in standard if x<=cap)[:nmax]


def reserve_items(a, e, low, cap):
    # Standard source pricing relaxation: r^c prepaid by A, with f>=c.
    ncheap=J.powerlog(a,low)
    vv=(*ordinary_prices(low,cap,e),*([min(low,cap)]*ncheap),*([cap]*e))
    return [1,*accumulate(sorted(vv)[:e],lambda x,y:x*y)]


@cache
def outside_tag_table(e, cutoff=229):
    """Minimum cost for sign − from ordinary prime r<=cutoff, assuming r∤A.

    A sign − necessarily has r=1 mod 3 and f+1=2·3^j mod 3^(j+1).
    As f is even, the least f+1 is 5·3^j. For each r<cutoff, compute
    the first legal f in this class, then price only one sign source.
    """
    out=[]
    cap=B//3**e
    for j in range(8):
        n=3**j
        best=(cutoff+1)**(5*n-1)
        for r in I.SUP:
            if r>cutoff:
                break
            m=5*n-1
            while r**m<best and r**m<=cap:
                if I.legal(r,m):
                    best=r**m
                    break
                m+=6*n
        out.append(best)
    return tuple(out)


def parity_supplier(a, e, s, room, low, rough_free, rates):
    """Reject an exact required sign-source: all possible tag producers price out.

    A sign may be prepaid by a rough r^c. Enumerate every c and f using
    relative room; remove only its own j units when asking for more tariffs.
    No summation of a square bonus and a sign-source surcharge.
    """
    k=e-s
    for j,cost in enumerate(outside_tag_table(e)):
        if j>k:
            break
        if cost*rates[max(0,k-j-rough_free)]<=room:
            return True
    h=e+1; step=6*h
    # Any rough component ≥ low and r^f <= A*room.
    maxf=J.powerlog(a*room,low)
    for j in range(8):
        if j>k:
            break
        n=3**j
        for f in range(5*n-1,maxf+1,6*n):
            residual=room//rates[max(0,k-j-rough_free)]
            if residual<1:
                continue
            for c in range(1,min(f,J.powerlog(a,low))+1):
                hi=iroot(a,c)
                if f>c:
                    hi=min(hi,iroot(residual,f-c))
                if crt_divisor(a,c,low,hi,step):
                    return True
    return False


@cache
def euler_least(s, tag):
    """Safe positive Euler lower; Fermat witness can reject composite, never certify."""
    y=3**s
    start=1 if tag==1 else 5 # odd k; 1 or 2 modulo 3
    for k in range(start,start+6*12,6):
        q=2*y*k-1
        if any(k%b==0 or q%b==0 for b in BN) or pow(2,q-1,q)!=1:
            continue
        return q
    return 2*y*(start+6*12)-1


@cache
def order_primes(n):
    ans=[]
    for p in range(3,isqrt(n)+1,2):
        if n%p:
            continue
        ans.append(p)
        while n%p==0:
            n//=p
    if n>1:
        ans.append(n)
    return tuple(p for p in ans if p!=3)


@lru_cache(maxsize=8192)
def outside_order_lower(y, q0, f, tag):
    """q divisor of an ordinary source sigma; maximal source index is tiny."""
    n=f+1
    if q0<=n:
        return q0
    primes=[]
    for p in order_primes(n):
        # q=2Y*k-1, odd k, hence k=Y^(-1) mod p in a class mod 2p.
        kmin=ceildiv(q0+1,2*y)
        k=pow(y,-1,p)
        if not k%2:
            k+=p
        k+=2*p*((tag-k)*pow(2*p,-1,3)%3)
        k=kmin+(k-kmin)%(6*p)
        primes.append(2*y*k-1)
    return min(primes,default=None)


def sigma_odd_lower(sigma_floor):
    # All ordinary root-three r ≥5; sigma(r^f) < (5/4)*r^f.
    return (4*sigma_floor)//5+1


def ext_possible(a,e,s,tag,q0,prices,gift):
    """Exterior source q|σ(r^f) and all its source divisor product.

    When r∤A, ord q(r) and exact root valuation constrain both r^f and
    A·σ(r^f)/3^j paid as an independent incoming demand on N. Because
    A alone and sigma(r^f) may share many other factors, do not multiply
    either by tariffs in the same comparison.
    """
    y=3**s; pe=3**e; room=B//(pe*a); k=e-s
    fmax=J.powerlog(room//q0,5)
    for f in range(2,fmax+1,2):
        q=outside_order_lower(y,q0,f,tag)
        if q is None:
            continue
        j=E.val(f+1,3)
        for b in (range(2) if 0<j<=k else range(1)):
            # b=0: source emits 0 units (any r residue relaxation). b=1: emits j.
            u=j*b
            v=prices[max(0,k-u-gift)]
            lo=iroot(sigma_odd_lower(q*3**u)-1,f)+1
            hi=iroot(min(room//(q*v),isqrt(room*3**u)),f)
            if hi<lo:
                continue
            if hi-lo>64:
                return True
            for r in range(max(5,lo)|1,hi+1,2):
                if a%r==0 or (r<2**64 and not E.mr(r)) or not I.legal(r,f):
                    continue
                if r%3!=1 and u or r%3==1 and j!=u:
                    continue
                # Retain any necessary source divisor. If q finitely enumerated
                # require exact s and its (q+1)/2 cofactor over the full product.
                sg=E.sigma(r,f)
                ymax=min(sg//3**u,room//(v*r**f))
                if ymax<q:
                    continue
                step=12*y; r0=(2*y if tag==1 else 10*y)-1
                start=q+(r0-q)%step
                if ymax-start>=64*step:
                    return True
                for z in range(start,ymax+1,step):
                    if (z+1)%(3*y)==0 or (z+1)%2 or any((z+1)%p==0 for p in BN) or a%z==0 or sg%z:
                        continue
                    X=pe*r**f*z;S=a*sg*(z+1);D=S//gcd(S,2*X)
                    if gcd(D,X)==1 and X*D<=B and S<=2*X:
                        return True
    return False


def int_possible(a,e,s,tag,q0,prices,gift,low,repeat_lower=0,witness=None):
    """Root-supported Euler source; enumerate exact exponent parity and source units."""
    y=3**s; p=3**(e+1); pe=p//3; room=B//(pe*a); k=e-s; h=e+1
    maxc=J.powerlog(a,low)
    # Necessary r^f <= room*3^u follows by dropping r^(f-c) >=1
    # from the incoming product. Globally 3^u <= f+1, but enumerate
    # only its largest size-permitted exponent before the exact u split.
    maxf=J.powerlog(a*(room//q0),low)
    while maxf>0 and low**maxf>room*(maxf+1):
        maxf-=1
    for f in range(2,maxf+1,2):
        q=outside_order_lower(y,q0,f,tag)
        if q is None:
            continue
        j=E.val(f+1,3)
        for u in (0,j) if 0<j<=k else (0,):
            v=prices[max(0,k-u-gift)]
            cap=room//(q*v)
            if cap<1:
                continue
            yy=y*3**u
            # Both balanced numerators are multiples of yy=Y*3^u: their
            # two terms contain either P or w*(q+1). For E nonzero use
            # v3(w*(q+1))=s+u<=e; for D use D=-P mod (r-1).
            bar=q*yy//(max(p,q)*(p//yy+4))
            for c in range(1,min(maxc,f)+1):
                g=f-c
                if not g and bar>=1:
                    continue
                rlo=max(low,repeat_lower if c>1 else low,
                        iroot(sigma_odd_lower(q*3**u)-1,f)+1,iroot(bar,g)+1 if g else low)
                rhi=min(iroot(a,c),iroot(room*3**u,f+g))
                if g:
                    rhi=min(rhi,iroot(cap,g))
                if rhi<rlo:
                    continue
                # Optimize arithmetical feasibility before a wide box is retained.
                if j>0 and u==0:
                    ok=crt_divisor(a,c,rlo,rhi,6*h,1+2*h*((2-1)*pow(2*h,-1,3)%3))
                else:
                    ok=crt_divisor(a,c,rlo,rhi,6*h if u else 2*h)
                if ok:
                    if witness is not None:
                        witness.update(c=c,f=f,u=u,lo=str(rlo),hi=str(rhi))
                    return True
    return False


def test(e, span, kernel, sample=False):
    require(e in frontier() and E.mr(e+1) and (e+1)%3,'unsupported exponent')
    a=E.sigma(3,e); pe=3**e
    ds, u = I.factor_small(a)
    require(not ds and u==a,'not a blind root block')
    one, high=J.audit(e,[])
    require(bool(one) and min(one)>0 and not high,'other Euler branches not ruled out')
    low=strip_lower(a,e+1,span)
    gift, freelo=free_levels(a,e+1,low)
    sq=minimum_odd_square_multiplier(a,low,e+1,kernel)
    prices=reserve_items(a,e,low,(I.T+1)**2)
    selected=[one[ix] for ix in sorted({0,len(one)//2,len(one)-1})] if sample else one
    out=dict(e=e,low=low,square_multiplier=sq,free_lower=freelo,free=gift,prior=len(one),tested=len(selected),
             left=[], counters={}, source_support={'exterior_only':0, 'interior_only':0, 'both':0})
    for s in selected:
        y=3**s; k=e-s
        for tag in (1,2):
            q=euler_least(s,tag); room=B//(pe*a*q)
            if pe*a*q*max(sq,prices[max(0,k-gift)])>B:
                reason='ordinary_or_square'
            elif tag==1 and not parity_supplier(a,e,s,room,low,gift,prices):
                reason='unit_parity'
            else:
                out1=ext_possible(a,e,s,tag,q,prices,gift)
                in1=int_possible(a,e,s,tag,q,prices,gift,low)
                if out1 or in1:
                    out['left'].append([s,tag,out1,in1])
                    typ='both' if out1 and in1 else ('exterior_only' if out1 else 'interior_only')
                    out['source_support'][typ]+=1
                    continue
                reason='two_source_classes'
            out['counters'][reason]=out['counters'].get(reason,0)+1
    return out


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--only', type=int, nargs='+', default=[1162,1108,990,970,856])
    p.add_argument('--span',type=int,default=4096)
    p.add_argument('--kernel',type=int,default=4096)
    p.add_argument('--out',action='store_true')
    p.add_argument('--sample',action='store_true',help='only probe the lowest/middle/highest surviving s')
    args=p.parse_args()
    rows=[]
    for e in args.only:
        start=monotonic()
        row=test(e,args.span,args.kernel,args.sample)
        rows.append(row)
        print(e,'left',len(row['left']),'of',2*row['tested'],'counters',row['counters'],
              'range',row['left'][-1:] + row['left'][:1], 'seconds',round(monotonic()-start,3),flush=True)
        if args.out:
            name='SourceUnitSample.json' if args.sample else 'SourceUnit.json'
            (HERE/name).write_text(json.dumps(rows,indent=1)+'\n',encoding='utf8')


if __name__=='__main__':
    main()
