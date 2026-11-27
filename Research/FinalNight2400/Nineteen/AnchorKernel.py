"""Generic exact incoming price at an ordinary mandatory-prefix below the 2477 pivot."""
from pathlib import Path
from math import gcd,prod
from fractions import Fraction
from functools import cache
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent));import VerifyAnchorMore as M
import Verify618Credit as C
from InverseMore import cap
p,e,t,B,n,d=C.p,C.e,C.t,C.B,C.n,C.d
sig,val=C.sig,C.val

class Kernel:
    def __init__(self):
        C.zero_t();C.square();C.square_price();self.cut=cap();U,V=C.deficit()
        K=M.K;self.BU=K*(B**d*U//V+1).bit_length();self.LU=K*((3*B)**d*U//V+1).bit_length()
    def run(self, f, extra, hint, trace=False):
        # extra is a dictionary of distinct fixed even-exponent rows already proved forced.
        # hint bases must be certified primes by caller; divisibility checked here.
        X0=p**e*t**f;T=t**(f-1);Q=2*T-1;A=C.A;C0=C.strip(sig(t,f),p)
        assert M.outside(C0,T) and gcd(X0,A*C0)==1 and gcd(A,C0)==1
        rows={p:e,t:f,**extra};X=prod(z**h for z,h in rows.items());S=prod(sig(z,h) for z,h in rows.items());D=S
        assert len(rows)==len(extra)+2 and all(h>0 and h%2==0 for h in rows.values())
        for z,h in rows.items():
            if val(S,z)>h:return True
            D=C.strip(D,z)
        if X*D>B or S>2*X:return True
        if any(sig(z,h)%t==0 for z,h in extra.items()):return True
        if any(A%z==0 for z in extra):return False # no unsupported reuse of the giant A block
        assert D%A==0;H=D//A;c=e-val(S,p);Eos=[]
        for z,h in extra.items():
            Y=sig(z,h)
            for r in rows:Y=C.strip(Y,r)
            Eos.append(Y)
        raw={y for y in hint if y not in rows}; assert all(D%y==0 for y in raw)
        safe={y for y in raw if C0%y==0 or y%(4*T)!=Q}
        def credits(ys):
            F=prod(y for y in ys if val(D,y)%2);G=prod((M.net(y)[0] for y in ys),start=Fraction(1));M0=max([M.net(y)[1] for y in ys]+[0]);return F,d*(M.loglo(G.numerator)-M.loglo(G.denominator)-1),M0
        _,LG0,_=credits(safe);F,LG,MG=credits(raw);Lx=d*M.loglo(X);Lp=M.loglo(p)
        def simple(s):return Lx+d*M.loglo(2*T*p**s-1)+n*(c-s)*Lp+LG0>self.BU
        lo,hi=-1,c+1
        while hi-lo>1:
            m=(lo+hi)//2
            if simple(m):lo=m
            else:hi=m
        for s in range(hi,c+1):
            if s==0:return False
            m=T*p**s;q=2*m-1;LQ=M.loglo(q)
            if X0*A*C0*q>B:return True
            if any(not M.outside(z,m) for z in Eos):return False
            base=X*D*q
            if base*F>B:return True
            if Lx+d*LQ+n*(c-s)*Lp+LG>self.BU:continue
            cop=gcd(A,H)==1; ov=max(A,H) if cop else D
            def size(u):
                kk=base*(F if u>MG else 1);aH=2*q*p**u
                if kk*aH>3*ov*B or u>=self.cut and kk*aH>3*H*B:return True
                return cop and u>=C.U0 and kk*kk*aH>3*B**2 and kk*aH>3*H*B
            for left,right,add in [(0,min(MG,c-s),0),(MG+1,c-s,LG)]:
                if right<left:continue
                l,r=left-1,right+1
                while r-l>1:
                    mid=(l+r)//2
                    if size(mid):r=mid
                    else:l=mid
                if l>=left:
                    lower=d*(M.loglo(2)+M.loglo(X)+2*LQ+l*Lp)+n*(c-s-l)*Lp+add
                    if lower<=self.LU:
                        if trace:print('gap',f,extra,s,l,flush=True)
                        return False
        return True
