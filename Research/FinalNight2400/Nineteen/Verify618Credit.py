"""Four lower exact fibers by compulsory even-row credits and the inverse lemma."""
from pathlib import Path
from math import gcd,isqrt,prod
from functools import cache
import json,sys
P=Path(__file__).resolve().parent;sys.path[:0]=[str(P),str(P.parents[1]/'RootFiveNext')]
from Verify618Square import p,e,t,B,n,d,zero_t,deficit,val,sig,strip,square,U0,A
import PrimeCheck as pc
z3=323053;z5=328481;z5b=114648701;z7=564854977327481;z9=230970247403894346223;z11=378187870792379499171334894532489
Z={26:[z3,z9,17443,9067249,77906087711754572666230250269017193635821716680301],30:[311,sig(t,30)//311],32:[z3,23,z11,67,1123,1895587,529842126314909260537315631043514267502364019238091140587],34:[z5,z5b,127,3221,z7,2801,303731,3343848272002999896155880134802741498105728532347653401024211521657446011]}

def primes():
    cert=json.loads((P/'CreditOther.json').read_bytes());cert.update(json.loads((P/'Credit30.json').read_bytes()))
    @cache
    def check(z):
        if z<2**64:return pc.prime64(z)
        k,v=cert[str(z)]
        if k=='ec':assert v[0]==z;return check(pc.level(*v))
        assert k=='pock' and len(v)==len({x for x,h,g in v})
        F=prod(x**h for x,h,g in v);assert (z-1)%F==0 and F**2>z
        return all(1<x<z and h>0 and check(x) and pow(g,z-1,z)==1 and gcd(pow(g,(z-1)//x,z)-1,z)==1 for x,h,g in v)
    assert all(check(z) for zz in Z.values() for z in zz)

def square_price():
    # Ordinary price treats primes only. Check that Euler square atoms need NO deficit.
    for o in (3,9):
        m=p;rr=[r for r in range(1,p) if pow(r,o,p)==1 and pow(r,o//3,p)!=1]
        for u in range(1,e+1):
            for z in rr:
                q=isqrt(z)
                if q*q==z and q%4==1:assert z**(d*(o-1))>=m**n
            if u<e:
                M=m*p;rr=[r+m*((-((pow(r,o,M)-1)//m)*pow(o*pow(r,o-1,p),-1,p))%p) for r in rr];m=M

def main():
    assert __debug__;primes();zero_t();square();square_price();U,V=deficit()
    for f,zz in Z.items():
        X=p**e*t**f;C=strip(sig(t,f),p);D=A*C;c=e-val(sig(t,f),p);T=t**(f-1);Q=2*T-1
        assert gcd(A,C)==gcd(X,D)==1
        j=C*pow(Q,-1,4*T)%(4*T);assert C//Q<4*T and (not j or j>C//Q or C%j)
        # Thus all z in zz are ordinary. Each is paid exactly once by D.
        assert len(zz)==len(set(zz)) and all(val(C,z)==1 for z in zz)
        F=prod(zz);MG=0;EN=1;ED=1
        for z in zz:
            h=2; earN=earD=None
            while X*z**h<=B:
                u=val(sig(z,h),p);MG=max(MG,u);a,b=z**h,p**(2*u)
                if earN is None or a*earD<b*earN:earN,earD=a,b
                h+=2
            assert earN is not None
            EN*=earN;ED*=earD
        g=gcd(EN,ED);EN//=g;ED//=g
        # EN/ED <= product z^h / p^(n sum(u)/d), since n/d<2.
        # Outside the multiplier, even Euler-square source requires no additional deficit.
        big=B**d*U*ED**d; ev=V*EN**d; rhs3=(3*B)**d*U
        def price(K,c):return K**d*p**(n*c)*ev>big
        assert price(X*Q,c)
        def q(s):return 2*T*p**s-1
        lo,hi=0,c+1
        while hi-lo>1:
            mid=(lo+hi)//2
            if price(X*q(mid),c-mid):lo=mid
            else:hi=mid
        assert (2*p)**d<p**n
        for s in range(hi,c+1):
            Qs=q(s);base=X*D*Qs
            if base*F>B:break
            # q cannot be fixed or in A,C as s>0. y supplying q is ordinary.
            def size(u):
                factor=F if u>MG else 1
                K=base*factor; aH=2*Qs*p**u
                if K*aH>3*max(A,C)*B:return True
                return u>=U0 and K*K*aH>3*B**2 and K*aH>3*C*B
            # Price changes at MG. Check both monotone slices separately.
            for beg,end,cred in [(0,min(MG,c-s),False),(MG+1,c-s,True)]:
                if end<beg:continue
                low,high=beg-1,end+1
                while high-low>1:
                    mid=(low+high)//2
                    if size(mid):high=mid
                    else:low=mid
                if low>=beg:
                    K=2*X*Qs**2*p**low
                    L=K**d*p**(n*(c-s-low))*V
                    if cred:assert L*EN**d>rhs3*ED**d,(f,s,low)
                    else:assert L>rhs3,(f,s,low)
        print('PASS 19^618 compelled-credit f=',f,'roots',len(zz),'max supply',MG,flush=True)
if __name__=='__main__':main()
