"""Quadratic incoming valuation price for the (7,12,Q,100/102) leaves.
The caller proves Q prime and binds the exact prefix and canonical scope.
"""
from functools import cache
from itertools import count
from math import gcd,isqrt,prod
from fractions import Fraction

Q=16148168401
B=10**2400
SMALL=(3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97)

@cache
def ds(n):
    return sorted({d for k in range(1,isqrt(n)+1) if n%k==0 for d in (k,n//k)})

@cache
def order_x(order):
    for g in count(2):
        x=pow(g,(Q-1)//order,Q)
        if x and all(pow(x,order//p,Q)!=1 for p in ds(order)[1:] if len(ds(p))==2):
            return x

@cache
def powers(c):
    return tuple(Q**j for j in range(c+2))


def enough(f,report=False):
    assert __debug__ and f in (100,102)
    X=7**12*Q**f
    d=(Q**(f+1)-1)//(Q-1)
    assert d%Q and d%7 and d%19 and Q%4==1
    assert f%2==0
    assert (7**13-1)//6==Q and 3**(Q.bit_length()**3)>B and Q.bit_length()**3<Q-1
    c=f-1
    P=powers(c)
    cap=B//X
    rates={}; orders=0
    # Drop restrictions on exponent parity (except h>1). For each order k,
    # h+1 is a multiple of k. LTE makes the incoming valuation independent
    # of that multiple because no viable exponent can reach Q-1.
    for k in ds(Q-1)[1:]:
        if k%4 == 0:
            continue  # h+1 would be divisible by 4, impossible at an odd exponent
        if k>Q.bit_length()**3:
            break
        e=5 if k==2 else k-1
        if 3**e>=P[c]**2 or 3**e>cap:
            continue
        orders+=1
        maxroot=1<<((cap.bit_length()+e-1)//e)
        first=next((j for j in range(1,c+1) if 3**e<P[j]**2),c+1)
        u=order_x(k)
        inv=pow(k*pow(u,k-1,Q),-1,Q)
        for j in range(1,c+1):
            m=P[j]; nxt=P[j+1]
            u+=m*((-(pow(u,k,nxt)-1)//m)*inv%Q)
        # All units of exact order k are powers of a single lifted generator.
        # At each depth only the least positive odd representative can be
        # cheap: e >= 2 implies the strict root limit is at most Q**j.
        top=P[c+1]
        y=1
        for i in range(1,k):
            y=y*u%top
            if gcd(i,k)!=1:
                continue
            for j in range(first,c+1):
                z=y%P[j]; r=z if z%2 else z+P[j]
                if r>maxroot:break  # least positive odd representatives never decrease
                limit=P[j]**2; bits=limit.bit_length()
                if r>2 and r not in (7,19,Q) and (r.bit_length()-1)*e<bits and r**e<limit and r**e<=cap and all(r==p or r%p for p in SMALL) and pow(2,r-1,r)==1:
                    if y%P[j+1]!=r:
                        loss=Fraction(limit,r**e)
                        rates[r]=max(rates.get(r,1),loss)
    U=prod(rates.values(),start=Fraction(1)); V=Fraction(X*P[c]**2)/U
    assert V>B, ('non-unit Euler',f)
    counts=[0,0,0]
    for s in range(c+1):
        m=P[s]; low=2*m-1
        if V*low>B*m*m:
            counts[0]+=1;continue
        assert X*d*low>B, ('external Euler',f,s)
        if low>d:
            counts[1]+=1;continue
        # q=2km-1 is the (possible) Euler prime and q=1 mod 4.
        # The odd quotient d/q is then d/(-1) mod 2m.
        lo=((-d)%(2*m)) or 2*m;hi=d//low
        if hi>=lo:
            assert (hi-lo)//(2*m)<128, ('inner Euler window too large',f,s)
            assert all(d%r for r in range(lo,hi+1,2*m)), ('inner Euler candidate',f,s)
        counts[2]+=1
    assert orders=={100:102,102:101}[f] and len(rates)==1
    assert counts=={100:[64,0,36],102:[70,0,32]}[f]
    if report:print('PASS',f,counts,'exceptional suppliers',len(rates),'orders',orders,flush=True)
    return counts

if __name__=='__main__':
    import sys
    for f in map(int,sys.argv[1:]):
        enough(f,report=True)
