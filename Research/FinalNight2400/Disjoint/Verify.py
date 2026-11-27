"""Coprime source lengths. Exact integer prices for prime or Euler-square bases."""
import math,sys
from functools import lru_cache
from fractions import Fraction
P,T,E=13,3543791,388
B=10**2400

def prime(n):return n>=2 and all(n%d for d in range(2,math.isqrt(n)+1))
def geom(x,h):return (x**(h+1)-1)//(x-1)
@lru_cache(None)
def price(p,c,w,divs):
    # Target charge is p^(w*u); no rounding penalty. Keep primes and possible Euler squares.
    exc={};g=1
    while any(pow(g,(p-1)//l,p)==1 for l in {2,*[l for l in divs if prime(l)]}):g+=1
    assert pow(g,p-1,p)==1
    for o in divs:
        if o==1 or 3**min(8000,o-1)>=p**(w*c):continue
        assert o-1>=w
        def cost(r,u):
            if r<3 or r%2==0 or any(r%k==0 and r not in (k,k*k) for k in (3,5,7,11,13,17,19,23,29,31,37)):return
            num=p**(w*u)
            if (r.bit_length()-1)*(o-1)<num.bit_length() and r**(o-1)<num:
                root=math.isqrt(r)
                if pow(2,r-1,r)!=1 and not (root*root==r and root%4==1 and pow(2,root-1,root)==1):return
                exc[r]=max(exc.get(r,1),Fraction(num,r**(o-1)))
        if o>100:
            R=3
            while R**(o-1)<p**(w*c):R*=2
            if R<200000:
                for r in range(3,R,2):
                    if pow(r,o,p)==1:
                        z=math.gcd(r**o-1,p**c);u=0
                        while z>1:z//=p;u+=1
                        cost(r,u)
                continue
        a=pow(g,(p-1)//o,p);rs=[pow(a,j,p) for j in range(1,o) if math.gcd(o,j)==1];m=1
        for u in range(1,c+1):
            m*=p
            for r in rs:cost(r,u)
            if u<c:rs=[r+m*((-((pow(r,o,m*p)-1)//m)*pow(o*pow(r,o-1,p),-1,p))%p) for r in rs]
    loss=math.prod(exc.values(),start=Fraction(1))
    print('price',p,c,'exceptions',len(exc),'loss bits',loss.numerator.bit_length()-loss.denominator.bit_length(),flush=True)
    return loss

def check(f):
    p,t,e=P,T,E
    assert prime(t) and t-1==2*5*389*911 and all(prime(l) for l in (5,389,911))
    divs=lambda n:tuple(d for d in range(1,n+1,2) if n%d==0)
    Dp,Dt=divs(3),divs((t-1)//2)
    assert math.gcd(p*3,t*((t-1)//2))==1
    assert 3**(p-1)>p**2 and 3**200>t**4 and t-1>200
    A=geom(p,e);C=geom(t,f);X=p**e*t**f
    cp=e;S=A*C
    while S%p==0:cp-=1;S//=p
    ct=f
    while S%t==0:ct-=1;S//=t
    D=S;assert math.gcd(D,X)==1 and min(ct,cp)>=0 and f%2==0
    U=price(p,cp,2,Dp)*price(t,ct,4,Dt);a,b=U.as_integer_ratio();fail=[];cnt=[0,0,0]
    # Sharper upper bound on the ordinary q-source overlap in either mandatory
    # block. Tests at independent p-adic/t-adic thresholds persist for larger
    # supply. Restrict the order by the index budget for the large target.
    @lru_cache(None)
    def banned_block(Z,l,u):
        if u<1:return False
        shift=0
        while l**(shift+1)<=8000:shift+=1
        if u<=shift:return False
        if l**(2*(u-shift))<=Z:return False
        mod=l**(u-shift);L0=1
        # For each possible odd order. Instead of listing roots, test divisibility via
        # gcd(Z, candidates) only for limited orders. Large orders handled separately.
        for o in (Dp if l==p else Dt):
            if o==1 or o>8000:continue
            if o>100:
                # Any r contributing at this order has X r^(o-1)<=B.
                # Any r contributing u also satisfies l^u<=r^o, but only
                # prime divisors of the block with that size need be tested.
                if X*3**(o-1)>B:continue
                R=3
                while X*R**(o-1)<=B:R*=2
                if R>=1000000:return False
                for r in range(3,R,2):
                    if Z%r==0 and pow(r,o,mod)==1:return False
                continue
            g=1
            while pow(g,(l-1)//o,l)==1 or any(pow(pow(g,(l-1)//o,l),o//k,l)==1 for k in range(2,o+1) if o%k==0 and prime(k)):g+=1
            z=pow(g,(l-1)//o,l);rts=[pow(z,j,l) for j in range(1,o) if math.gcd(j,o)==1];m=l
            while m<mod:
                rts=[r+m*((-((pow(r,o,m*l)-1)//m)*pow(o*pow(r,o-1,l),-1,l))%l) for r in rts];m*=l
            for r in rts:
                if r>1 and r%2 and Z%r==0:return False
                k=Z*pow(r,-1,mod)%mod
                if k and k<=Z//mod and Z%k==0:return False
        return True
    # All blocks struck at fixed primes before testing interiors or overlap.
    blocks=[A//math.gcd(A,X),C//math.gcd(C,X)];H=max(blocks) if math.gcd(*blocks)==1 else D
    def outside(Z,m,Q):
        if Z<Q:return True
        if Z//Q>=4*m:return False
        k=Z*pow(Q,-1,4*m)%(4*m)
        return not(0<k<=Z//Q and Z%k==0)
    for j in range(ct+1):
        for i in range(cp+1):
            m=p**i*t**j;Q=2*m-1;rp=cp-i;rt=ct-j
            V=p**(2*rp)*t**(4*rt)
            if X*Q*V*b>B*a:cnt[0]+=1;continue
            if outside(blocks[0],m,Q) and (j>0 or outside(blocks[1],m,Q)):
                if X*D*Q>B:cnt[1]+=1;continue
                # Condition on t-supply of one ordinary q-source; cap p-supply using mandatory size.
                for v in range(rt+1):
                    # For fixed v, decreasing secondary price gives minimum u needed.
                    L=2*X*Q**2*V*b; K=3*B*a*t**(3*v)
                    if L>K*p**rp:continue
                    lo,hi=0,rp
                    while lo<hi:
                        mid=(lo+hi)//2
                        if L<=K*p**mid:hi=mid
                        else:lo=mid+1
                    ov=math.prod(Z for Z in blocks if not (banned_block(Z,t,v) or banned_block(Z,p,lo))) if math.gcd(*blocks)!=1 else max([1]+[Z for Z in blocks if not (banned_block(Z,t,v) or banned_block(Z,p,lo))])
                    if 2*X*D*Q**2*p**lo*t**v<=3*B*ov:break
                else:cnt[2]+=1;continue
            fail.append((i,j, outside(blocks[0],m,Q), j>0 or outside(blocks[1],m,Q)))
    print(f,'pass' if not fail else 'open',cnt,len(fail),fail[:1],fail[-1:],flush=True)
    return not fail
if __name__=='__main__':
    assert __debug__
    for f in (72,78):assert check(f)
