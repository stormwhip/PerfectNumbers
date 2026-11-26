"""Deterministic Hasse-order primality checker. JSON is untrusted: only primality of the returned roots is inferred."""
from math import gcd,isqrt

def ecprime(n,chain,smallprime):
    q=n
    for N,t,k,a,(x,y) in chain:
        if N!=q or not(3<N and N%2 and 0<=x<N and 0<=y<N and 0<=a<N and k>0):return False
        m=N+1-t
        if m%k:return False
        q=m//k
        # If N composite there is a prime l<=sqrt(N), so |E(F_l)|<=(N^1/4+1)^2.
        if not ((isqrt(isqrt(N))+2)**2<q<N):return False
        b=(y*y-x*x*x-a*x)%N
        if gcd(4*a**3+27*b*b,N)!=1:return False
        def add(U,V):
            if U is None:return V
            if V is None:return U
            x,y=U;z,w=V
            if x==z:
                if (y+w)%N==0:return None
                if y!=w:raise ValueError('nonunit point denominator')
                d=(2*y)%N;c=(3*x*x+a)%N
            else:d=(z-x)%N;c=(w-y)%N
            h=c*pow(d,-1,N)%N;X=(h*h-x-z)%N
            return X,(h*(x-X)-y)%N
        def mul(k,P):
            U=None
            while k:
                if k&1:U=add(U,P)
                k//=2
                if k:P=add(P,P)
            return U
        P=mul(k,(x,y))
        if P is None or mul(q,P) is not None:return False
    return smallprime(q)
