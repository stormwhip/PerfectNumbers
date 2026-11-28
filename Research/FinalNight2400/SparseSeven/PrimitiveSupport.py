"""Unconditional high-s internal Euler emitter bounds at 7^906, independent of omega and squarefreeness.
Recheck the one historical input via Seven906 before using this structural deduction."""
from math import gcd
from functools import cache
from pathlib import Path
import sys
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P.parent/'Nineteen'));from Sparse906 import rootfloor
p=7;X=7**906;W=p*X;A=(W-1)//6;B=10**2400;rough=10**7
@cache
def root(n,k):return rootfloor(n,k)
def first(n,k):return root(n-1,k)+1

@cache
def minQ(s,h):
    Y=7**s;u=pow(Y,-1,h+1);u+=(h+1)*((1-u)%2)
    for _ in range(8):
        q=2*u*Y-1
        if gcd(u,7*19)==1 and all(q%v for v in (3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97)):break
        u+=2*(h+1)
    return 2*u*Y-1

def possibilities(s):
    Y=p**s;Q=2*Y-1;T=B//(X*A*Q);out=set(); c=1
    # z|A ordinary; omega(A)>=3, z>C; at least two other A-primes >C beyond z^c.
    while rough**(c+2)<=A:
        # z^g <=N/(XAq)*z^c, and z^g >=2Q/3. Thus use exact [lo,hi].
        g=c+c%2
        while X*(2*Y-1)*rough**g<=B and X*A*(2*Y-1)*rough**(g-c)<=B:
            h=g;g+=2;# Proper order at q would force h >= 3*(o-1) and z^h>(2q/3)^3.
            assert X*(2*Y-1)*(2*(2*Y-1))**3>27*B and 2*Y-1>5100 and 3**5100>B
            if (h+1)%7==0:continue
            # ord_q(z)=h+1, hence h+1 divides q-1. q=2ny-1, n odd,
            # 7-free by exact s; 19-free by canonical absence from sigma(q).
            Q=minQ(s,h);T=B//(X*A*Q)
            lo=max(rough+1,first((2*Q+2)//3,h));hi=root(A//(rough**2),c)
            if h>c:hi=min(hi,root(T,h-c))
            if hi<lo:continue
            if h==2 and c==2 and (18*A)**2+9*A*Q<Y*Q*Q:continue
            # Balanced B0 signed upper bound: if z large, D sigma(z^(c-1))<W/(z-1), and D*w<(3/2)(W/q)z^(h-c).
            # If 3*W*T < Y*Q, then |B0|<Y when z>2W/Y+1. Lower bound for negative B0 is -3T/2 > -Y.
            if 3*W*T<Y*Q and 3*T<2*Y:
                hi=min(hi,2*(W//Y)+1)
            if hi<lo:continue
            d=h+1-c;Dh=6*(A//lo**c)
            # A0 = ((W-1)/q-1) z^d - D(1+1/q). Nonzero because another A-prime divides D, not z.
            # Z0 modulo 1814 equals -1-6A because z=1 there. Y is invertible mod 1814.
            pos=(W-1)*hi**d//(Q*Y);neg=(Q*hi**d+(Q+1)*Dh)//(Q*Y);L=1814;J=(-1-6*A)*pow(Y,-1,L)%L
            if (J or L)>pos and ((-J)%L or L)>neg:continue
            out.add((h,c))
        c+=1
    return out
if __name__=='__main__':
    assert __debug__
    counts=[]
    for s in range(682,711):
        v=possibilities(s);assert v==({(4,2)} if s<=684 else set()),s
        for h,c in v:
            Y=7**s;cap=root((B//(X*A))**h*3**(h-c)//(2**(h-c)),2*h-c);M=(cap+1)//(2*Y);counts.append(M)
            for m in range(1,M+1,2):
                q=2*m*Y-1
                if gcd(m,7*19)==1 and (q-1)%(h+1)==0:assert pow(2,q-1,q)!=1
    assert counts==[300,42,6]
    print('PASS canonical 7^906 all Euler configurations: s<=681. All 682..710 eliminated.')