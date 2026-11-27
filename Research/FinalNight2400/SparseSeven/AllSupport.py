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

def possibilities(s):
    Y=p**s;Q=2*Y-1;T=B//(X*A*Q);out=set(); c=1
    # z|A ordinary; omega(A)>=3, z>C; at least two other A-primes >C beyond z^c.
    while rough**(c+2)<=A:
        # z^g <=N/(XAq)*z^c, and z^g >=2Q/3. Thus use exact [lo,hi].
        g=c+c%2
        while X*Q*rough**g<=B and rough**(g-c)<=T:
            h=g;g+=2;lo=max(rough+1,first((2*Q+2)//3,h));hi=root(A//(rough**2),c)
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
    for s in range(685,711):
        v=possibilities(s);assert v==({(6,4)} if s<=698 else set()),s
    print('PASS unrestricted A multiplicities: s<=698; every emitter has exact h=6,c=4 in 685..698',flush=True)
