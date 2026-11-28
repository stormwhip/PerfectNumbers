"""Independent 31/3229 free-Euler price; 210 uniform cap, 156 full allocation."""
from functools import cache
from fractions import Fraction
from itertools import product
from math import gcd,lcm,isqrt,prod
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from Check31Domains import B,BANS,geometric,state,split,vp
from Check31Masks import prime
P,T=31,3229

@cache
def family(p,o,c):
    divs=[j for j in range(1,o) if o%j==0]
    g=next(j for j in range(2,p) if pow(j,o,p)==1 and all(pow(j,k,p)!=1 for k in divs))
    powers=[i for i in range(1,o) if gcd(i,o)==1]
    out=[(1,(0,))];m=p
    for _ in range(c):
        assert pow(g,o,m)==1
        rr=tuple(pow(g,j,m) for j in powers)
        assert len(set(rr))==len(rr) and all(0<r<m for r in rr)
        out.append((m,rr))
        m*=p;g=pow(g,p,m)
    return out


def loss(f):
    prefix=((P,268),(T,f));X,S,ok=state(prefix)
    assert ok and (268-vp(S,P),f-vp(S,T))==(268,f-1)
    D=lcm(X,S)//X
    orders=[[d for d in range(3,5032,2) if (p-1)%d==0] for p in (P,T)]
    assert orders==[[3,5,15],[3,269,807]]
    for o,r in product([1,*orders[0]],[1,*orders[1]]):
        assert gcd(o*r,P*T)==1
        assert 2*(3 in (o,r))+sum(k-3 for k in (o,r) if k>3)<=lcm(o,r)-1
    tabs=[{},{},{}]
    def insert(i,m,y,h):
        if y<3 or y%2==0 or y in (P,T,*BANS) or 10*h*(y.bit_length()-1)>=19*m.bit_length():return
        z=isqrt(y)
        if z*z==y and (z%4!=1 or z in (P,T,*BANS)):return
        if z*z!=y:z=y
        if any(z!=a and z%a==0 for a in PRIMES):return
        if z.bit_length()<=512 and any(pow(a,z-1,z)!=1 for a in (2,3,5,7,11) if a<z):return
        power=y**h
        if X*lcm(D,power)>B:return
        den=power**10; num=m**19
        if den<num:tabs[i][y]=max(tabs[i].get(y,1),Fraction(num,den))
    for m,rr in family(P,3,268):
        for n,ss in family(T,3,f-1):
            if m==1: ys=ss
            else:
                u=n*pow(n,-1,m)
                ys=((s+u*(r-s))%(m*n) for r,s in product(rr,ss))
            for y in ys:insert(0,m*n,y,2)
    for k,(p,orders_p,c) in enumerate(zip((P,T),orders,(268,f-1)),1):
        for o in orders_p:
            if o==3 or 3**(10*(o-3))>=p**(19*c):continue
            for m,rr in family(p,o,c)[1:]:
                for r in rr:insert(k,m,r,o-3)
    out=prod(u for tab in tabs for u in tab.values())
    return X,D,(out.numerator+out.denominator-1)//out.denominator,[len(t) for t in tabs]


def entire(f):
    X,D,U,ls=loss(f)
    A=geometric(P,268)//T; C=geometric(T,f)
    assert D==A*C and gcd(A,C)==1 and gcd(D,P*T)==1
    W=X**10*(P**268*T**(f-1))**19
    if f==210:
        cap=max(A,C,B//(X*D))
        assert W>B**10*cap**9*U
        print('PASS uniform Euler all-exponent cap',f,'losses',ls,'rounded U digits',len(str(U)),flush=True)
        return
    assert f==156
    counts=[0,0,0]
    pp=[P**i for i in range(269)];tt=[T**j for j in range(f)]
    for i,j in product(range(269),range(f)):
        m=pp[i]*tt[j];q=max(5,2*m-1)
        if W*q**10>B**10*U*m**19:
            counts[0]+=1;continue
        if X*D*q<=B:
            assert W*(X*D)**9*(2*q*q)**19>B**19*U*max(A,C)**9*3**19*m**19,(i,j)
            counts[1]+=1
        for k,block in enumerate((A,C)):
            if (k==0 and i) or block<q:continue
            period=4*m
            c=block*(2*m-1)%period or period
            hi=block//q
            if c<=hi:
                assert hi<c+20*period and all(block%n for n in range(c,hi+1,period)),(i,j,k)
        counts[2]+=1
    assert counts[0]+counts[2]==269*f
    print('PASS exact Euler price and full cofactor checks',f,counts,'losses',ls,flush=True)

if __name__=='__main__':
    assert __debug__ and all(prime(p) for p in (P,T,269))
    assert 3**5030<=B<3**5031 and all(3**(10*(p-1))>=p**19 for p in (P,T))
    PRIMES=tuple(v for v in range(3,98,2) if prime(v))
    domain,tail=split(((P,268),),T)
    assert len(domain)==76 and tail==458 and all(x in domain for x in (102,156,210))
    for f in map(int,sys.argv[1:] or [210]):entire(f)
