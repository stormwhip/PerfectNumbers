"""Independent 19/1109 even-first Euler and high-normal checks."""
from fractions import Fraction
from functools import cache
from math import gcd,isqrt,lcm,prod
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from Check19x276x1109x4 import B,P,S,Q as T,geom,vp,plainprime,composite_witness


def state(rows):
    X=prod(p**h for p,h in rows)
    incoming=prod(geom(p,h) for p,h in rows)
    Y=incoming>>vp(incoming,2)
    return X,Y,lcm(X,Y),incoming<=2*X and lcm(X,Y)<=B and all(vp(Y,p)<=h for p,h in rows)


@cache
def loss(free):
    tab={}
    for o in (3,9):
        rr=[z for z in range(2,P) if pow(z,o,P)==1 and (o==3 or pow(z,3,P)!=1)]
        m=P
        for z in range(1,277):
            for r in rr:
                if r>=3 and r%2 and r not in (P,T,S) and r**(o-1)<m*m and ((free and isqrt(r)**2==r) or not composite_witness(r)):
                    tab[r]=max(tab.get(r,1),Fraction(m*m,r**(o-1)))
            if z<276:
                rr=[r+k*m for r in rr for k in range(P) if pow(r+k*m,o,m*P)==1]
                m*=P
                assert len(rr)==(2 if o==3 else 6)
    return prod(tab.values())


def lift277():
    g=next(x for k in range(2,S) if (x:=pow(k,4,S))!=1)
    m=S
    for z in range(1,5):
        rr={pow(g,k,m) for k in range(1,277)}
        assert len(rr)==276 and all(pow(r,277,m)==1 for r in rr)
        lo=min(r if r%2 else r+m for r in rr)
        if z==4:
            assert lo>=50_000_000
        else:
            assert lo**276>=S**(100*z)
        m*=S;g=pow(g,S,m)


def internal(A,m):
    q=max(5,2*m-1)
    if A<q:return False
    mod=4*m
    k=A*(2*m-1)%mod or mod
    last=A//q
    if k>last:return False
    if last>=k+20*mod:return True
    while k<=last:
        if A%k==0:return True
        k+=mod
    return False


def euler(f,base,tail,dom):
    X,Y,_,_=state(base)
    assert (S**3-1)%P==0 and vp(S**3-1,P)==1 and P**3>5031
    assert X*S**809*P**(2*(276-vp(Y,P)-3))>B*10**6
    assert loss(False)<10**6
    xx,yy,_,_=state((*base,(S,5)))
    if X*S**405*P**(2*(276-vp(Y,P)-3))<=B*10**6:
        K=63700
        assert 5-vp(yy,S)==4 and xx*P**(2*(276-vp(yy,P)))*K**276>B*10**6
        p=[b for b in range(3,K,2) if b not in (P,T,S) and pow(b,277,S)==1 and plainprime(b)]
        assert all(pow(b,277,S*S)!=1 for b in p) and prod(p[:4])>=K
    E=(*base,(S,1)); rows=(*E,(3,2),(5,2),(37,2))
    _,y,_,_=state(E)
    assert all(y%b==0 for b in (3,5,37))
    def abund(rows): return prod(Fraction(geom(p,h),p**h) for p,h in rows)
    A=abund(rows)
    bad=[p for p in (7,11,13,17,23,29,31) if A*Fraction(geom(p,2),p*p)>2]
    assert len(bad)==7
    assert all(any(geom(p,h)%q==0 for q in bad) for p in (3,5,37) for h in (2,4))
    assert abund((*E,(3,6),(5,6),(37,6)))>2
    print('PASS',f,'all Euler-at-1109 exact',len([h for h in dom if h%4==1]),'tail',tail,flush=True)


def main():
    assert __debug__ and all(plainprime(p) for p in (P,T,S,277))
    assert 3**5030<=B<3**5031 and S*277>5031 and (2*S+1)**1108>B
    assert gcd(P*9,S*277)==1 and 3**18>P**2
    lift277()
    U=loss(True)
    ex={2:(137,184,274,549),8:(128,172,256,514),16:(116,156,232,466),28:(98,132,196,394)}
    for f,(n,start,end,want) in ex.items():
        base=((P,276),(T,f)); X,Y,M,ok=state(base)
        assert ok and vp(M,S)==1 and vp(Y,S)==1 and X*50_000_000**276>B
        h=1; live=[]; closed=[]
        while M*S**(h-1)<=B:
            if (h%2==0 or h%4==1) and state((*base,(S,h)))[-1]:live.append(h)
            h+=1
        assert h==want
        euler(f,base,h,live)
        for h in [a for a in live if a%2==0]:
            row=(*base,(S,h)); Xh,Yh,Mh,_=state(row)
            cP,cS=276-vp(Yh,P),h-vp(Yh,S)
            assert cS==h-1
            sig=[geom(p,k) for p,k in row]
            # Each q+1 allocation m; atom price is evaluated arithmetically before
            # independently checking all relevant outer/inner Euler possibilities.
            p19=[P**j for j in range(cP+1)]; s1109=[S**i for i in range(cS+1)]; margin=B*U.numerator
            unresolved=False
            for i,si in enumerate(s1109):
                price=Xh*s1109[cS-i]**100*U.denominator
                if price*max(5,2*si-1)>B*U.denominator:continue
                for j,pj in enumerate(p19):
                    m=si*pj; q=max(5,2*m-1)
                    if Xh*q>B or price*q*p19[cP-j]**2>margin:continue
                    if Mh*q<=B or any(internal(a,m) for k,a in enumerate(sig) if k!=0 or j==0):
                        unresolved=True; break
                if unresolved:break
            if not unresolved:closed.append(h)
        assert len([a for a in live if a%2==0])==n and closed==list(range(start,end+1,2))
        print('PASS',f,'ordinary',n,'closed',start,end,len(closed),'tail',want,flush=True)


if __name__=='__main__':main()
