"""Exact finite weighted supply price: all translates under the tested inequality.
No primality assumptions on candidates retained by the loss generator.
"""
from fractions import Fraction as F
from functools import cache
from itertools import product
from math import gcd, isqrt, prod

B=10**2400
BAN=(7,11,13,19,31)
SMALL=(3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97)

def vp(n,p):
    assert n>0
    s=0
    while n%p==0:
        s+=1;n//=p
    return s

def sig(p,h):return (p**(h+1)-1)//(p-1)
def prime(p):return p>1 and all(p%j for j in range(2,isqrt(p)+1))

def floor10(n):
    k=F(n);j=len(str(k.numerator//k.denominator))-1
    return -1 if k<1 else j

@cache
def divisors(n):return tuple(sorted({d for i in range(1,isqrt(n)+1) if n%i==0 for d in (i,n//i)}))

@cache
def root_levels(p,o,cap):
    assert o>1 and (p-1)%o==0
    if cap<=0:return ()
    x=next(pow(a,(p-1)//o,p) for a in range(2,p) if all(pow(a,(p-1)//t,p)!=1 for t in divisors(o) if prime(t)))
    roots=tuple(sorted(pow(x,j,p) for j in range(1,o) if gcd(j,o)==1));M=p;result=[]
    if o==2:return tuple((j,(m:=p**j),(m-1,)) for j in range(1,cap+1))
    # Lift only one modular generator; its coprime powers are precisely the
    # distinct exact-order roots at every subsequent depth. For the small
    # orders, lifting the entire set costs less than generating all powers.
    if o>15:
        m=p;a=x;inv=pow(o*pow(x,o-1,p),-1,p)
        for j in range(1,cap):
            N=m*p;a+=m*((-((pow(a,o,N)-1)//m)*inv)%p);m=N
        N=m;assert a%p==x and pow(a,o,N)==1
        js=tuple(i for i in range(1,o) if gcd(i,o)==1)
        # Compute the maximal-depth powers once; their reductions are the
        # sub-depth systems. Split the powers using a modest window so no
        # large repeated gcd or exponentiation is needed at each depth.
        powers=tuple(pow(a,i,N) for i in js)
        for j in range(1,cap+1):
            result.append((j,M,tuple(z%M for z in powers)));M*=p
    else:
        inverses=tuple(pow(o*pow(z,o-1,p),-1,p) for z in roots)
        for j in range(1,cap+1):
            result.append((j,M,roots));nextM=M*p
            if j<cap:roots=tuple(z+M*((-((pow(z,o,nextM)-1)//M)*inv)%p) for z,inv in zip(roots,inverses))
            M=nextM
    return tuple(result)

@cache
def qpow(p,i):return p**i

def less(x,h,A):return max(0,x.bit_length()-1)*h<A.bit_length() and x**h<A

def exact_supply(r,h,p,cap):
    t=h+1
    if r%p==1:return vp(t,p)
    M=qpow(p,cap+1);u=(pow(r,t,M)-1)%M
    return vp(u or M,p)

def crt(a,m,b,n):return (a+m*((b-a)*pow(m,-1,n)%n),m*n)

@cache
def get_context(rows):
    fixed=dict(rows);assert len(rows)==len(fixed)
    assert all(prime(p) and h>0 and p not in BAN for p,h in rows)
    odd=sum(h%2 for p,h in rows)
    assert odd<=1 and all(h%2==0 or h%4==p%4==1 for p,h in rows)
    X=prod(p**h for p,h in rows);S=prod(sig(p,h)//(1+h%2) for p,h in rows)
    assert all(vp(S,p)<=h for p,h in rows)
    blocks=[sig(p,h)//(1+h%2) for p,h in rows]
    blocks=[x//prod(p**vp(x,p) for p in fixed) for x in blocks]
    D=prod(blocks);assert D==S//gcd(X,S) and X*D<=B
    assert gcd(D,prod(BAN))==1 and gcd(D,X)==1
    return fixed,odd,X,S,D,[x for x in blocks if x!=1]

def price(rows, targets, *, even_only=False):
    """targets=(prime, integral weight). Returns X*full_price/product(losses), losses.
    Set even_only only for the analysis of ordinary rows (or fixed Euler).
    Otherwise also include h >=5 with h,r=1 mod 4.
    """
    fixed,odd,X,S,D,blocks=get_context(rows)
    Q=tuple((p,w,fixed[p]-vp(S,p)) for p,w in targets)
    assert all(w>0 and c>=0 for p,w,c in Q) and len({p for p,w,c in Q})==len(Q)
    H=sum(w for p,w,c in Q if c);odd=odd or even_only
    E={};M=prod(qpow(p,c*w) for p,w,c in Q); tested=set()
    hmax=0
    while qpow(5,hmax+1)<=min(B//X,M-1):hmax+=1
    def legalh(h):return h%2==0 or (not odd and h%4==1)
    def charge(r,h):
        if r<5 or r%2==0 or r in fixed or r in BAN or (h%2 and r%4!=1):return
        if any(r!=p and r%p==0 for p in SMALL):return
        if (r,h) in tested:return
        tested.add((r,h))
        if any(((h+1)%p==0 if r%p==1 else pow(r,h+1,p)==1) for p in BAN):return
        if any(exact_supply(r,h,p,0) for p in fixed if vp(S,p)==fixed[p]):return
        vv=[exact_supply(r,h,p,c) for p,w,c in Q]
        if any(v>c for v,(p,w,c) in zip(vv,Q)):return
        lim=prod(qpow(p,w*v) for v,(p,w,c) in zip(vv,Q))
        if not less(r,h,lim):return
        mass=r**h
        if X*D*(mass//gcd(D,mass))>B or pow(2,r-1,r)!=1:return
        E[r]=max(E.get(r,F(1)),F(lim,mass))
    def reps(a,m,h,b):
        a+=(max(5,a)-a+m-1)//m*m
        while less(a,h,b):
            charge(a,h);a+=m
    def local(p,c,w,h):
        yield 0,1,1
        s=vp(h+1,p)
        if 0<s<=c:yield 1,p,qpow(p,w*s)
        for o in divisors(gcd(h+1,p-1)):
            if o>1:
                for j,m,roots in root_levels(p,o,c-s):
                    for z in roots:yield z,m,qpow(p,w*(j+s))
    for h in range(2,min(H,hmax+1)):
        if not legalh(h):continue
        for opt in product(*(local(p,c,w,h) for p,w,c in Q)):
            a,m,b=0,1,1
            for z,v,n in opt:
                if v>1:a,m=crt(a,m,z,v)
                b*=n
            reps(a,m,h,b)
    for p,w,c in Q:
        if not c:continue
        smax=0
        while qpow(p,smax+1)<=hmax+1:smax+=1
        for h in range(max(2,H),hmax+1):
            if legalh(h):
                s=vp(h+1,p)
                if 0<s<=c:reps(1,p,h,qpow(p,H*s))
        for o in divisors(p-1):
            if o==1 or o>hmax+1 or (odd and o%2==0) or not less(5,o-1,qpow(p,H*c)):continue
            first=(((max(2,H)+1)+o-1)//o)*o-1
            for j,m,roots in root_levels(p,o,c):
                high=qpow(p,H*min(c,j+smax))
                for a in roots:
                    for h in range(first,hmax+1,o):
                        if not less(max(5,a),h,high):break
                        if not legalh(h):continue
                        s=vp(h+1,p)
                        if j+s<=c:reps(a,m,h,qpow(p,H*(j+s)))
    return X*M/prod(E.values(),start=F(1)),E
