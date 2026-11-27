"""The only unfixed 349667-source has Euler order two (7^486)."""
from math import gcd,isqrt,prod
from functools import cache
B=10**2400;p,e,s,t=7,486,349667,1229048719
G=lambda b,h:(b**(h+1)-1)//(b-1)
@cache
def prime(n):return n>=2 and all(n%d for d in range(2,isqrt(n)+1))
def source():
 A=G(p,e);X=p**e;assert all(prime(r) for r in (p,s,t,359,487)) and s-1==2*359*487 and gcd(A,X)==1 and A%(s*t)==0 and gcd(A//(s*t),s*t)==1 and gcd(A,487*(p-1))==1
 assert 3**7999>B and s>8000
 orders=[o for o in range(1,8001) if (s-1)%o==0];assert orders==[1,2,359,487,718,974]
 hits=[]
 for o in orders[2:]:
    n=o-1
    # If r belongs to A, it is 1 mod 974; no factorization of A. If r outside, charge A fully.
    for inside in (False,True):
        r=975 if inside else 3;step=974 if inside else 2
        while X*(1 if inside else A)*r**n<=B:
            if r!=p and (not inside or A%r==0) and pow(r,o,s)==1 and prime(r):
                # Need only this shorter geometric block, even for multiples of o.
                Z=G(r,n);assert (A*Z)%2==0 or n%2==0
                raw=A*(Z//gcd(Z,2));assert gcd(raw,r)==1 or A%r==0
                # If r|A account for its exact overlap; Xr^n divides N and raw divides N.
                assert X*r**n*raw//gcd(X*r**n,raw)>B
                hits.append((o,r))
            r+=step
 assert hits==[(359,22129),(359,25183)]
 print('PASS s-supply exclusively Euler via q+1; all exceptional large-order hits eliminated',hits,flush=True)

@cache
def basic():
 # Common cubic supply: at the exceptional minimal exponent 2, low deficits
 # imply b|... not assumed. Enumerate CRT representatives once for ALL cells.
 import runpy
 from pathlib import Path
 from fractions import Fraction
 core=runpy.run_path(str(Path(__file__).resolve().parents[1]/'Root7Joint/Verify.py'));roots=core['roots']
 # Charge high t orders separately with o-3 powers. t-1=2*3*41*487*10259.
 assert t-1==2*3*41*487*10259 and all(prime(k) for k in (3,41,487,10259)) and gcd(t-1,7)==1
 low={};high={};pt=list(roots(p,e));ct=85
 # A strict component-size limit independent of i,j; fixed root and both compulsory squares divide N.
 maxsize=B//(p**e*s**2*t**2)
 def charge(tab,b,m,h):
    if b<3 or b%2==0 or 10*h*(b.bit_length()-1)>=19*m.bit_length() or h*(b.bit_length()-1)>=maxsize.bit_length():return
    if b in (p,s,t,19) or any(b%r==0 and b not in (r,r*r) for r in (3,5,7,11,13,17,19,23,29,31,37,41,43)):return
    v=m**19;y=b**(10*h)
    if y>=v:return
    if pow(2,b-1,b)!=1:
        k=isqrt(b)
        if k*k!=b or k%4!=1 or k in (p,s,t,19) or pow(2,k-1,k)!=1:return
    tab[b]=max(tab.get(b,1),Fraction(v,y))
 # Lift roots of order three directly rather than trial-generating all residues mod t.
 def r3(q,c):
    y=next(z for a in range(2,100) if (z:=pow(a,(q-1)//3,q))!=1);rr=[y,y*y%q];m=q
    yield 1,(0,)
    for k in range(1,c+1):
        yield m,rr
        if k<c:rr=[a+m*((-((a*a+a+1)//m)*pow(2*a+1,-1,q))%q) for a in rr];m*=q
 for n,rs in r3(t,ct):
    inv=1;pi=pow(7,-1,n)
    for m,ys in pt:
        for a in ys:
            for b in rs:charge(low,a+m*((b-a)*inv%n),m*n,2)
        inv=inv*pi%n
 div=[1]
 for l in (3,41,487,10259):div+=[l*k for k in div]
 g=next(a for a in range(2,100) if all(pow(a,(t-1)//l,t)!=1 for l in (2,3,41,487,10259)))
 for o in div:
    if o<=3 or o>8000 or 3**(o-3)>=t**(2*ct):continue
    h=o-3
    if o>=123:
        r=3
        while r**h<t**(2*ct) and r<200000:r*=2
        if r<200000:
            for b in range(3,r,2):
                if pow(b,o,t)==1:charge(high,b,gcd(pow(b,o,t**ct)-1,t**ct),h)
            continue
    z=pow(g,(t-1)//o,t);rs=[pow(z,k,t) for k in range(1,o) if gcd(k,o)==1];m=t
    for k in range(1,ct+1):
        for b in rs:charge(high,b,m,h)
        if k<ct:rs=[b+m*((-((pow(b,o,m*t)-1)//m)*pow(o*pow(b,o-1,t),-1,t))%t) for b in rs];m*=t
 loss=prod(low.values(),start=Fraction(1))*prod(high.values(),start=Fraction(1));print('exception base counts',len(low),len(high),flush=True)
 return (loss.numerator+loss.denominator-1)//loss.denominator

def check():
 source();U=basic();A=G(p,e);live=[];left=[];done=[]
 assert xbound(p**e*A//s,s)==286 and xbound(p**e*A//t,t)==175
 for i in range(2,286,2):
    for j in range(2,175,2):
        X=p**e*s**i*t**j;Z=[A,G(s,i),G(t,j)];S=prod(Z);D=S//gcd(S,X)
        if X*D>B or gcd(D,X*19)!=1 or S>2*X:continue
        cp=e;cs=i;ct=j
        for T in (p,s,t):
            k=0
            while S%T==0:k+=1;S//=T
            if T==p:cp-=k
            elif T==t:ct-=k
            else:cs-=k
        assert S==D and cs==i-1 and 0<=ct<=85 and cp>=0
        live.append((i,j));T=s**cs;M=p**cp*t**ct;z=[v//gcd(X,v) for v in Z];assert prod(z)==D
        cap=max((B//(X*D)+1)//2,min((z[0]+1)//2,T*t**ct),min((z[2]+1)//2,T*p**cp))
        # Since q>=T*m, where m is its joint p,t-supply, mandatory and price give m<=cap/T and N>=X*T*M²/(U*m).
        if (X*T)**10*M**19*T**9>B**10*U*cap**9:done.append((i,j));continue
        # Refined bound under an exterior Euler component. Conditional on a linear
        # p,t contribution m, remove the ordinary q-emitter before pricing.
        Hm=max(a*prod(gcd(a,b) for jj,b in enumerate(z) if ii!=jj) for ii,a in enumerate(z))
        K=X**10*M**19;D0=X*D
        def outside(Z,m,Q):
            if Z<Q:return True
            if Z//Q>=4*m:return False
            k=Z*pow(Q,-1,4*m)%(4*m);return not(0<k<=Z//Q and Z%k==0)
        def allwin():
            pp=[p**u for u in range(cp+1)]
            for b in range(ct+1):
                tv=t**b;lo,hi=0,cp+1
                while lo<hi:
                    mid=(lo+hi)//2;m=pp[mid]*tv;Q=2*T*m-1
                    if K*Q**10>B**10*U*m**19:lo=mid+1
                    else:hi=mid
                if lo>cp:continue
                for a in range(lo,cp+1):
                    m=pp[a]*tv;Q=2*T*m-1
                    if (a==0 and not outside(z[0],T*m,Q)) or (b==0 and not outside(z[2],T*m,Q)):return False
                    if D0*Q>B:
                        if (a or Q>z[0]) and (b or Q>z[2]):break
                        continue
                    y=min(M//m,3*B*Hm//(2*D0*Q**2))
                    if (2*Q**2)**10*K<=(3*B)**10*U*m**19*y**9:return False
                    if a and b:break
            return True
        (done if allwin() else left).append((i,j))
 print('joint live',len(live),'cut',len(done),'remain',len(left), 'first s',sorted(set(a for a,b in live)-set(a for a,b in left)),'second t',sorted(set(b for a,b in live)-set(b for a,b in left)),flush=True);return live,done,left

def xbound(z,t):
 k=1
 while z*t**k<=B:k+=1
 return k
if __name__=='__main__':
 assert __debug__
 L,C,R=check();assert len(L)==1517 and (len(C),len(R))==(905,612)
