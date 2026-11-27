"""Exact integer necessary profile for A with <=2 primes after Sparse906; no real logs in acceptance."""
from math import gcd,prod,isqrt
from functools import cache
from fractions import Fraction
from pathlib import Path
import sys
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P.parent/'Nineteen'));from Sparse906 import A,X,B,U,rootfloor
W=7*X;D=1814;C=10**7

def prime(n):return n>=2 and all(n%i for i in range(2,isqrt(n)+1))
@cache
def lowbounds(t,a,j):
    m=7**t;M=D*m;rr=[(v:=pow(b,7**(t-1),m))+m*((1-v)*pow(m,-1,D)%D) for b in (2,4)]
    lr=max(C*m,min(rr));
    if j%7==0:
        assert A**3%49==22 and all(pow(x,21,49) in (1,48) for x in range(1,49) if x%7);return None
    k=3*j;roots=[b for b in range(1,7) if pow(b,k,7)==pow(A,3,7) and A*pow(b,-j,7)%7 in {pow(v,a,7) for v in (2,4)}];mod=7
    for _ in range(1,t):
        K=7*mod;roots=[b+mod*((-((pow(b,k,K)-pow(A,3,K))//mod)*pow(k*pow(b,k-1,7),-1,7))%7) for b in roots];mod=K
    if not roots:return None
    lb=max(C,min(b+m*((1-b)*pow(m,-1,D)%D) for b in roots));return lr,lb

def perfectpowers():
    # If all prime multiplicities of A had a common prime d, A would be an integer dth power.
    for d in range(2,110):
        if prime(d):assert rootfloor(A,d)**d!=A

def order(u):
    j=0
    while u%7==0:u//=7;j+=1
    return j

def make():
    perfectpowers();out=set();sset=set();pairs=0;cacheproof={};witnesses=[]
    for u in range(82,144):
        t0=u-4;rmin=C*7**t0
        # A=r^a b^j, distinct ordinary primes, r supplies u. Both exceed C.
        assert rmin**12>A
        for a in range(1,12):
            if rmin**a>A:break
            for j in range(1,110):
                if rmin**a*C**j>A:break
                if (a==j==1) or gcd(a,j)>1:continue
                rough=lowbounds(t0,a,j)
                if rough is None:continue
                lr,lb=rough
                if lr**a*lb**j>A:continue
                k=max(2,a+a%2)
                while X*lr**k*(2*7**482-1)<=B:
                    h=k;k+=2
                    if (h+1)%3:continue
                    t=u-order(h+1);bound=lowbounds(t,a,j)
                    if bound is None:continue
                    R,L=bound
                    if R**a*L**j>A:continue
                    g0=max(2,j+j%2)
                    while X*R**h*L**g0*(2*7**482-1)<=B:
                        g=g0;g0+=2
                        # Q and outside price minima. Eliminate b^g using A^g=r^(ag)b^(jg).
                        diff=j*h-a*g;Mmin=R**diff*A**g if diff>=0 else 0
                        for s in range(482,666):
                            Y=7**s;Q=2*Y-1;v=max(0,906-s-5-u);budget=B*U//(X*Q*7**(2*v));
                            if budget<=0:continue
                            if diff>=0:
                                if Mmin>budget**j:continue
                            elif L**(-diff)*A**h>budget**a:continue
                            # For either emitter, enforce y^e>=ceil(2Q*7^uy/3), then account outside price.
                            for who in ['r','b']:
                                rr=R;bb=L
                                if who=='r':
                                    if R**h<2*Q*7**u//3:rr=max(R,rootfloor((2*Q*7**u+2)//3-1,h)+1)
                                elif L**g<2*Q//3:bb=max(L,rootfloor((2*Q+2)//3-1,g)+1)
                                if rr**a*bb**j>A:continue
                                if diff>=0:
                                    if rr**diff*A**g>budget**j:continue
                                elif bb**(-diff)*A**h>budget**a:continue
                                out.add((a,j,h,g,who));sset.add(s);pairs+=1;witnesses.append((s,u,a,j,h,g,who))
    return out,sset,pairs,witnesses
if __name__=='__main__':
    assert __debug__;sys.set_int_max_str_digits(0);out,s,pairs,v=make();assert out=={(1,2,2,2,'b'),(1,4,2,4,'b'),(2,1,2,2,'r'),(2,5,2,6,'b')} and min(s)==633 and max(s)==665 and len(v)==1490;print('PASS',sorted(out),min(s),max(s),pairs,flush=True)