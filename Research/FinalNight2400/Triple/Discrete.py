"""A mandatory Euler congruence at the canonical 19^358 root."""
from math import gcd,prod,isqrt
from fractions import Fraction
from pathlib import Path
from functools import lru_cache
import runpy
B=10**2400;p,e,s,t=19,358,38518547,1491133067
G=lambda r,h:(r**(h+1)-1)//(r-1)
A=G(p,e);A0=A//(s*t);x=p**e
@lru_cache(None)
def prime(n):return n>=2 and all(n%i for i in range(2,isqrt(n)+1))

def prove_source():
 assert all(prime(z) for z in (p,s,t,11,359,941,2207,4877)) and t-1==2*359*941*2207 and s-1==2*11*359*4877
 assert A==A0*s*t and gcd(A0,s*t)==1 and gcd(A,359*(p-1))==1 and t>8000 and 3**7999>B
 assert s%4==t%4==3
 # Odd ordinary orders dividing t-1: only these three are nontrivial below 8000;
 # Euler orders can include twice each. Order 1 and t|h+1 impossible by size.
 orders={d for d in range(1,8001) if (t-1)%d==0};assert orders=={1,2,359,718,941,1882,2207,4414}
 for o in sorted(orders-{1,2}):
    for inside in (False,True):
        step=718 if inside else 2;r=719 if inside else 3
        while x*(1 if inside else A)*r**(o-1)<=B:
            if r!=p and (not inside or A%r==0) and pow(r,o,t)==1:
                assert not prime(r)
            r+=step
 # Thus only Euler q can supply external t at order 2. Since t∤a+1, LTE gives q+1 valuation.


def check():
 prove_source();price=runpy.run_path(str(Path(__file__).resolve().parents[1]/'Disjoint/Verify.py'))['price']
 # Combining 19 and s via disjoint effective lengths. s orders begin at 11; 359,4877 factored.
 ds=tuple(sorted({prod(S) for S in [(),(11,),(359,),(4877,),(11,359),(11,4877),(359,4877),(11,359,4877)]}));assert gcd(19*9,s*(s-1)//2)==1 and 3**18>19**2 and 3**200>s**10
 us=price(s,95,10,ds);up=price(p,e,2,(1,3,9));u=us*up;U=(u.numerator+u.denominator-1)//u.denominator
 assert gcd(A,x)==1
 def top(z):
    h=1
    while x*(A//z)*z**h<=B:h+=1
    return h
 assert top(s)==197 and top(t)==163
 lives=[];cut=[];survive=[]
 for i in range(2,197,2):
    for j in range(2,163,2):
        X=x*s**i*t**j;S=A*G(s,i)*G(t,j);D=S//gcd(S,X)
        if X*D>B or gcd(X,D)!=1 or S>2*X:continue
        assert i<=96 and S%t==0 and (S//t)%t # all j−1 t-units come from q+1
        cp=e;cs=i;Y=S
        for l in (p,s):
            c=0
            while Y%l==0:c+=1;Y//=l
            if l==p:cp-=c
            else:cs-=c
        assert 0<=cp<=e and 0<=cs<=95
        lives.append((i,j));T=t**(j-1);Q=2*T-1
        # Even if q|D, X and q are disjoint. All residual non-q+1 units of p,s
        # paid at weights 2,10. m=T*p^a*s^b, q>=m. For q|a fixed emission,
        # reciprocity forces its own coordinate zero, or use simple cofactor bound.
        Z=[G(p,e),G(s,i),G(t,j)];Z=[z//gcd(z,X) for z in Z]
        assert prod(Z)==D
        cap=max((B//(X*D)+1)//2,min((Z[0]+1)//2,T*s**cs),min((Z[1]+1)//2,T*p**cp)) # t block forbidden since j>=2
        worst=0;pa=p**cp
        for b in range(cs+1):
            sb=s**b
            while pa>=p and T*pa*sb>cap:pa//=p
            if T*pa*sb>cap:break
            worst=max(worst,pa*sb**9)
        if X*T*p**(2*cp)*s**(10*cs)>B*U*worst:cut.append((i,j))
        else:
            V=p**(2*cp)*s**(10*cs);pp=[p**a for a in range(cp+1)];ss=[s**a for a in range(cs+1)]
            def outside(Z,m,Q):
                if Z<Q:return True
                if Z//Q>=4*m:return False
                u=Z*pow(Q,-1,4*m)%(4*m)
                return u==0 or u>Z//Q or Z%u!=0
            def all_windows():
                H=max(z*prod(gcd(z,k) for j,k in enumerate(Z) if j!=l) for l,z in enumerate(Z))
                for b,sb in enumerate(ss):
                    c1=s**(10*b);remS=ss[cs-b]
                    def ext(a):
                        pa=pp[a];m=T*sb*pa;Q=2*m-1
                        return (a>0 or outside(Z[0],m,Q)) and (b>0 or outside(Z[1],m,Q))
                    # Do not assume ext() monotone. It becomes permanent by size or QR.
                    # Direct XQV is decreasing in a: (2M z-1)/z² with M>=T>1.
                    lo,hi=0,cp+1
                    while lo<hi:
                        mid=(lo+hi)//2;pa=pp[mid];Q=2*T*sb*pa-1
                        if X*Q*V>B*U*pa**2*c1:lo=mid+1
                        else:hi=mid
                    if lo>cp:continue
                    # Supplier-price lower bound monotone increasing in p^a under relaxed Q>=m:
                    # Q²/pa² >= T² sb² and capped P*S^9 decreases. Use it from first weak a.
                    for a in range(lo,cp+1):
                        pa=pp[a];m=T*sb*pa;Q=2*m-1
                        if not ext(a):return False
                        if X*D*Q>B:
                            # size always sufficient above this a provided q external there;
                            # for b=0, test the maximum remaining uncertainty via block size.
                            if (a>0 or Z[0]<Q) and (b>0 or Z[1]<Q):break
                            continue
                        lim=3*B*H//(2*X*D*Q*Q)
                        # Exact discrete maximum P*S^9: take largest admissible S, then P.
                        # If S increases one level, a loss in P is <p*S_ratio unless
                        # the P cap binds; s^9>p*s suffices. Simpler: direct loop.
                        bound=0
                        import bisect
                        for vs in range(cs-b+1):
                            tv=ss[vs]
                            if tv>lim:break
                            u=min(cp-a,bisect.bisect_right(pp,lim//tv)-1)
                            bound=max(bound,pp[u]*tv**9)
                        if 2*X*Q**2*V<=3*B*U*pa**2*c1*bound:return False
                        # after a>=1 with b>=1, unconditional externality hence monotonicity
                        if a and b:break
                return True
            (cut if all_windows() else survive).append((i,j))
 print('joint live',len(lives),'excluded',len(cut),'remaining',len(survive),'first',sorted(set(i for i,j in lives)-set(i for i,j in survive)),'second',sorted(set(j for i,j in lives)-set(j for i,j in survive)),flush=True)
 return lives,cut,survive
if __name__=='__main__':
 assert __debug__
 L,C,R=check();assert (len(L),len(C),len(R))==(968,645,323)