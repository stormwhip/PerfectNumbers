"""Exact ordinary-anchor reduction under 19^618; certificates validated offline."""
from pathlib import Path
from functools import cache
from fractions import Fraction
from math import gcd,prod
import json,sys
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P));import Verify618Credit as C
p,e,t,B,n,d=C.p,C.e,C.t,C.B,C.n,C.d
sig,val=C.sig,C.val

def outside(Z,m):
    q=2*m-1
    if q>Z:return True
    k=Z*pow(q,-1,4*m)%(4*m)
    return Z//q<4*m and not (0<k<=Z//q and Z%k==0)

def certificates():
    pack=json.loads((P/'Anchor618.json').read_bytes());assert set(pack)=={'low','emit'}
    for mode,table in pack.items():
        for k,D in table.items():
            N=sig(t,int(k)) if mode=='low' else sig(int(k),2)
            for label,chain in D.items():
                z=y=int(label);assert N%z==0
                for row in chain:assert y==row[0];y=C.pc.level(*row)
                assert C.pc.prime64(y)
                while N%z==0:N//=z
            assert N==1
    return pack

def ilog(x):return x.bit_length()-1
K=512
@cache
def loglo(x):return ilog(x**K)
@cache
def net(z):
    # Omit X here: using all even h with z^h<=B gives conservative bounds.
    G=None;H=0;m=z*z;h=2
    while m<=B:
        u=val(sig(z,h),p);r=Fraction(m,p**(2*u));G=r if G is None else min(G,r);H=max(H,u);m*=z*z;h+=2
    assert G is not None
    return G,H

def main():
    assert __debug__;pack=certificates();C.zero_t();C.square();C.square_price();U,V=C.deficit(); A=C.A
    # Work entirely with rounded-down scaled binary log products for the four price comparisons.
    Lp=loglo(p);BU=K*ilog(B**d*U//V+1)+K;LU=K*ilog((3*B)**d*U//V+1)+K
    for f0,zzz in pack['low'].items():
        f=int(f0);Z0=set(map(int,zzz))-{p};z=max(Z0);X0=p**e*t**f;C0=C.strip(sig(t,f),p);T=t**(f-1);Q=2*T-1
        assert gcd(A,C0)==gcd(A*C0,X0)==1 and outside(C0,T) and val(C0,z)==1
        base0=X0*A*C0; rows=[];live=[];h=0
        while base0//z*z**(h+2)<=B:
            h+=2;X=X0*z**h;E=sig(z,h);c=e-val(sig(t,f)*E,p)
            if c<0 or val(E,t)+1>f:continue
            # t cannot be supplied by any such external even row in a valid configuration.
            if E%t==0:continue
            Eo=C.strip(C.strip(E,p),t);assert Eo%z
            H=C0//z*Eo;D=A*H
            if X*D>B:continue
            rows.append(h);rawz=(Z0-{z})|(set(map(int,pack['emit'].get(str(z),{}))) if h==2 else set()); rawz-=set((p,t,z))
            assert all(D%y==0 for y in rawz)
            # Sieve rows coming from E alone are not automatically ordinary at s=0.
            all0={y for y in rawz if y in Z0 or y%(4*T)!=Q};assert all(y%2 for y in all0)
            def credits(ys):
                F=prod(y for y in ys if val(D,y)%2);G=prod((net(y)[0] for y in ys),start=Fraction(1));MG=max([net(y)[1] for y in ys]+[0]);return F,G,MG
            F0,G0,MG0=credits(all0);F,G,MG=credits(rawz)
            # monotone basic price with the safe compulsory set, valid even if q|A or E.
            Lx=d*loglo(X);LG0=d*(loglo(G0.numerator)-loglo(G0.denominator)-1);LG=d*(loglo(G.numerator)-loglo(G.denominator)-1)
            def simple(s):return Lx+d*loglo(2*T*p**s-1)+n*(c-s)*Lp+LG0>BU
            # Exact price decreases with s, so a safe success at s proves all lower s.
            lo,hi=-1,c+1
            while hi-lo>1:
                mid=(lo+hi)//2
                if simple(mid):lo=mid
                else:hi=mid
            ok=True
            for s in range(hi,c+1):
                if s==0:ok=False;break
                m=T*p**s;q=2*m-1;LQ=loglo(q)
                if X0*A*C0*q>B:break
                if not outside(Eo,m):ok=False;break
                base=X*D*q
                if base*F>B:break  # later s: q may divide Eo? if outside true here via residue but not all future classes?
                # Divisibility classes are nested as s grows, so q∤Eo persists once established.
                if Lx+d*LQ+n*(c-s)*Lp+LG>BU:continue
                # The square lemma excludes r²|A, not r²|D if H shares r.
                # We conservatively avoid this benefit unless gcd(A,H)=1.
                oa=max(A,H) if gcd(A,H)==1 else D
                def size(u):
                    factor=F if u>MG else 1; kk=base*factor; aH=2*q*p**u
                    if kk*aH>3*oa*B:return True
                    return gcd(A,H)==1 and u>=C.U0 and kk*kk*aH>3*B**2 and kk*aH>3*H*B
                for left,right,extra in [(0,min(MG,c-s),0),(MG+1,c-s,LG)]:
                    if right<left:continue
                    l,r=left-1,right+1
                    while r-l>1:
                        mid=(l+r)//2
                        if size(mid):r=mid
                        else:l=mid
                    if l>=left:
                        lower=d*(loglo(2)+loglo(X)+2*LQ+l*Lp)+n*(c-s-l)*Lp+extra
                        if lower<=LU:ok=False;break
                if not ok:break
            if not ok:live.append(h)
        print('anchor 19^618',f,'direct',rows,'remaining',live,flush=True)
        assert not live,(f,live)
if __name__=='__main__':main()
