"""Exact arithmetic verifier for stated conditional exclusions. Python 3.8+."""
from math import gcd, isqrt
from fractions import Fraction
from functools import lru_cache
import sys

P, E, T, B = 19, 432, 11842464881317660217, 10**2400
TF = (11,101,433,3077160600929)

def trial(n):
    return n >= 2 and all(n%d for d in range(2,isqrt(n)+1))

def gen(t, factors):
    for g in range(2,100):
        if pow(g,t-1,t)==1 and all(gcd(t,pow(g,(t-1)//d,t)-1)==1 for d in factors):
            return g
    raise ArithmeticError

def sigma(r,h): return (r**(h+1)-1)//(r-1)

def val(n,p):
    assert n>0
    k=0
    while n%p==0:
        k+=1;n//=p
    return k

@lru_cache(None)
def deficit(p,c,w):
    # Base may be a prime or Euler prime squared: do not primality-filter.
    if p==P: orders=[3,9];g=gen(P,[2,3])
    else:
        assert p==T
        orders=[1]
        for d in TF: orders += [o*d for o in orders]
        orders.remove(1);g=gen(T,[2,*TF])
    # For order one or a length multiplier p^k, the exponent surcharge
    # is >= k*(p-1); r>=3 so it costs at least p^(w*k).
    assert 3**min(p-1,4096)>=p**w
    loss={}
    for o in orders:
        h=o-1
        if 3**min(h,16384)>=p**(w*c):continue
        assert h>=w
        if o>460:
            R=3
            while R**h<p**(w*c):R*=2
            assert R<1000000
            for r in range(3,R,2):
                if pow(r,o,p)!=1 or any(pow(r,o//d,p)==1 for d in TF if o%d==0):continue
                u=min(c,val(pow(r,o)-1,p));rat=Fraction(p**(w*u),r**h)
                if rat>loss.get(r,1):loss[r]=rat
            continue
        go=pow(g,(p-1)//o,p)
        roots=[pow(go,j,p) for j in range(1,o) if gcd(j,o)==1]
        m=1
        for u in range(1,c+1):
            m*=p
            for r in roots:
                if r<3 or not r%2:continue
                rat_num=m**w // (p**(u//20) if p==P else 1)
                if (r.bit_length()-1)*h < rat_num.bit_length() and r**h < rat_num:
                    rat=Fraction(rat_num,r**h)
                    if rat>loss.get(r,1):loss[r]=rat
            if u<c:
                M=m*p
                roots=[r+m*((-(pow(r,o,M)-1)//m*pow(o*pow(r,o-1,p),-1,p))%p) for r in roots]
    U=Fraction(1)
    for ratio in loss.values():U*=ratio
    return U

@lru_cache(None)
def roots19(z):
    if z==1:return tuple(r for r in range(2,P) if pow(r,9,P)==1)
    m=P**(z-1); M=m*P
    return tuple(r+m*((-(pow(r,9,M)-1)//m*pow(9*pow(r,8,P),-1,P))%P) for r in roots19(z-1))

@lru_cache(None)
def cannot_supply_from(Z,u):
    if u<=2:return False
    z=u-2; m=P**z
    if m*m<=Z:return False
    for r in roots19(z):
        if r>1 and r%2 and Z%r==0:return False
        k=(Z*pow(r,-1,m))%m
        if k and k<=Z//m and Z%k==0:return False
    return True

def outside(Z,m,Q):
    # q == 2m-1 (mod 4m); Q=2m-1; hence k=Z/q constrained.
    if Q>Z:return True
    k=Z*pow(Q,-1,4*m)%(4*m)
    return Z//Q<4*m and not(0<k<=Z//Q and Z%k==0)

def check(f,verbose=False):
    assert f==18
    X=P**E*T**f; A=sigma(P,E)//T; C=sigma(T,f)
    assert sigma(P,E)==A*T and A%T and C%T and C%P and gcd(A,C)==1
    D=A*C; ct=f-1; W=9; w=2
    U=P**(E//20)*deficit(P,E,w)*deficit(T,ct,W)
    # A and C are odd, coprime to X. D|N/X.
    assert gcd(D,X)==1
    assert C==sigma(T,P-1) and gcd(C,P*(T-1))==1 and (2*P+1)**(P-1)>=P**16
    a,b=U.numerator,U.denominator
    pending=[];count=[0,0,0]
    for j in range(ct+1):
        tj=T**j;remt=T**(W*(ct-j))
        for i in range(E+1):
            m=tj*P**i;Q=2*m-1; remp=P**(w*(E-i))
            if X*Q*remp*remt*b>B*a:
                count[0]+=1;continue
            ext=(i>0 or outside(A,m,Q)) and outside(C,m,Q)
            if ext and f==18 and (X*Q*remp*b)**8*C**7>(B*a)**8:
                count[1]+=1;continue
            if ext and X*D*Q>B:
                count[1]+=1;continue
            # Extra supplier of q even when v_q(N)>1. Partition on its
            # units v of t, u of p; both size bounds monotone in u.
            if ext:
                ok=True
                for v in range(ct-j+1):
                    z=2*X*D*Q*Q*T**v
                    lo,hi=0,E-i+1
                    while lo<hi:
                        mid=(lo+hi)//2
                        overlap=max(1,*(n if not cannot_supply_from(n,mid) else 1 for n in (A,C)))
                        if z*P**mid>3*overlap*B:hi=mid
                        else:lo=mid+1
                    u=lo-1
                    if u>=0 and f==18:
                        # If supplier r is not in C, get full C^(7/8) on top of remaining p-price;
                        # if it is in C, its p-supply is at most 2.
                        def zprice(u):return 2*X*Q*Q*T**v*P**u*P**(w*(E-i-u))*b
                        if zprice(min(2,u))*T**(W*(ct-j-v))>3*B*a and zprice(u)**8*C**7>(3*B*a)**8:continue
                    if u>=0 and 2*X*Q*Q*T**v*P**u*P**(w*(E-i-u))*T**(W*(ct-j-v))*b<=3*B*a:
                        ok=False;break
                if ok:count[2]+=1;continue
            pending.append((i,j))
    print('f',f,'counts priced/mandatory/supplier',count,'pending',len(pending), 'endpoints',pending[:2],pending[-2:],flush=True)
    return pending

def main():
    assert trial(P) and all(trial(d) for d in TF) and 8*11*101*433*3077160600929==T-1
    assert 3**(P**3-1)>B
    gen(T,[2,*TF]);assert gcd(P*(P-1),T*(T-1)//8)==1
    for f in [int(s) for s in sys.argv[1:]] or [18]:
        assert not check(f)

if __name__=='__main__':main()