"""Additive exact 19^618 cuts. Inverse residues exclude r^2 dividing A."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from Verify618 import p,e,t,B,n,d,zero_t,deficit,val,sig,strip,gcd

U0=206; A=sig(p,e)//t

def square():
    # r|A forces order 619, hence r=1 mod 1238.
    assert A%619 and (19-1)%619
    m=19; roots=[r for r in range(1,19) if pow(r,9,m)==1 and r!=1]
    for _ in range(U0-2):
        k=m*19; roots=[r+m*((-((pow(r,9,k)-1)//m)*pow(9*pow(r,8,19),-1,19))%19) for r in roots];m=k
    assert m==19**(U0-1) and len(roots)==8
    K=1238*m
    for r in roots:
        assert pow(r,9,m)==1
        R=r+m*((1-r)*pow(m,-1,1238)%1238);J=(A*pow(R*R,-1,K))%K
        assert R%1238==1 and J>0 and R*R*J>A
    # LTE extra v19(h+1)>=2 => h>=3*361-1, and if
    # r has nontrivial 19^203 root it is > a tiny minimum.
    assert 19**(U0-2)-1>1000**9 and 1000**(3*19**2-1)>B
    # Use the independent blunt h bound instead: h+1<19^3, so v19(h+1)<=2;
    # for the +2 case u0>=204 forces r>1000, contradiction above.
    assert 3**(19**3-1)>B and (2*19+1)**(19**3-1)>B

def main():
    assert __debug__;zero_t();square();U,V=deficit(); bound=B**d*U; b3=(3*B)**d*U
    def price(K,c):return K**d*p**(n*c)*V>bound
    for f in range(36,47,2):
        X=p**e*t**f;C=strip(sig(t,f),p);D=A*C;c=e-val(sig(t,f),p);T=t**(f-1);Q=2*T-1
        j=C*pow(Q,-1,4*T)%(4*T)
        assert C//Q<4*T and (not j or j>C//Q or C%j)
        assert gcd(A,C)==gcd(X,D)==1 and X*D*Q**5>B and price(X*Q**3,c) and price(X*Q,c)
        # Eliminate at all s<=lo by decreasing price; locate transition by
        # testing single most expensive boundary rather than large powers in inner loop.
        def q(s):return 2*T*p**s-1
        lo,hi=0,c+1
        while hi-lo>1:
            mid=(lo+hi)//2
            if price(X*q(mid),c-mid):lo=mid
            else:hi=mid
        # q(s+1)/q(s) <= 2p, and (2p)^d<p^n.
        assert (2*p)**d<p**n
        for s in range(hi,c+1):
            Qs=q(s);base=X*D*Qs
            if base>B:break
            # Bounds monotone in u. Ordinary source h>=2 with H=2Qs p^u/3.
            # For u>=U0 payment outside D is >=min(sqrt(H),H/C).
            def size(u):
                aH=2*Qs*p**u
                if base*aH>3*max(A,C)*B:return True
                return u>=U0 and base*base*aH>3*B**2 and base*aH>3*C*B
            lo2,hi2=-1,c-s+1
            while hi2-lo2>1:
                m=(lo2+hi2)//2
                if size(m):hi2=m
                else:lo2=m
            if lo2>=0:
                assert (2*X*Qs**2*p**lo2)**d*p**(n*(c-s-lo2))*V>b3,(f,s,lo2)
        print('PASS 19^618 square-supplier f=',f,flush=True)
if __name__=='__main__':main()
