"""Joint price for the fixed (19^276,1176672733,1109^2,13^276) branch.
The compact cubic/lower-order loss calculation enumerates every positive deficit.
"""
from functools import cache
from fractions import Fraction
from math import gcd,prod

B=10**2400
PREFIX=((19,276),(1176672733,1),(1109,2),(13,276))
X=prod(q**a for q,a in PREFIX)
A=prod((q**(a+1)-1)//(q-1) for q,a in PREFIX)
S=A//2

def vp(n,p):
    assert n>0
    a=0
    while n%p==0:n//=p;a+=1
    return a

def oddroots(p,o,c):
    rr=[r for r in range(2,p) if pow(r,o,p)==1 and all(pow(r,d,p)!=1 for d in range(1,o) if o%d==0)]
    assert len(rr)==o-o//3
    m=p
    for z in range(1,c+1):
        assert all(0<r<m and pow(r,o,m)==1 for r in rr)
        yield m,tuple(rr)
        m*=p
        rr=[pow(r,p,m) for r in rr]

def probable(r):
    return r>=3 and r%2==1 and r not in dict(PREFIX) and all(pow(a,r-1,r)==1 for a in (2,3,5,7,11,13,17) if a<r)

def short(r,e,n):return e*(r.bit_length()-1)<n.bit_length() and r**e<n

def add(tab,r,theta,n,e):
    if r>=3 and short(r,e,n) and probable(r):
        if (p:=r**2)*X>B:return
        g=Fraction(n,r**e)
        tab[r]=max(g,tab.get(r,1))

@cache
def loss():
    # Both coordinates have exponent weight 19/10. The 19 order 9 and
    # 13 order 3 together can pay two base powers per coordinate.
    p,q=19,13;c=276-vp(S,p);d=276-vp(S,q)
    assert (c,d)==(275,276)
    assert p-1==2*9 and q-1==4*3 and gcd(p*q,9)==1
    assert 3**(10*(p-1))>=p**19 and 3**(10*(q-1))>=q**19
    cr=tuple(oddroots(p,3,c));dr=tuple(oddroots(q,3,d));er=tuple(oddroots(p,9,c))
    pp={m:m**19 for m,_ in cr}; qq={m:m**19 for m,_ in dr}
    P={};Q={};Z={}
    for m,roots in [*cr,*er]:
        for r in roots:add(P,r,(m,),pp[m],20)
    for n,roots in dr:
        for r in roots:add(Q,r,(n,),qq[n],20)
    for m,rr in cr:
        for n,ss in dr:
            U=m*n; W=pp[m]*qq[n]; inv=pow(m,-1,n)
            for r in rr:
                for s in ss:
                    v=r+m*((s-r)*inv%n)
                    add(Z,v,(m,n),W,20)
    keys=P.keys()|Q.keys()|Z.keys(); one=Fraction(1)
    return {r:max(Z.get(r,one),P.get(r,one)*Q.get(r,one)) for r in sorted(keys)}

D=S//gcd(X,S)
C,D13=276-vp(S,19),276-vp(S,13)
M=(19**C*13**D13)**19

def baseprice():return Fraction(X**10*M,prod(loss().values()))

def sig(p,h):return (p**(h+1)-1)//(p-1)

def atom(p,h):
    s=sig(p,h)
    a,b=vp(s,19),vp(s,13)
    if a>C or b>D13:return None
    return Fraction(p**(10*h),(19**a*13**b)**19)*loss().get(p,1)

@cache
def gain(p,a):
    best=None;where=None
    for h in range(a+a%2,5031,2):
        price=p**h
        if X*price>B:break
        if best is not None and price**10>=best*M:break
        value=atom(p,h)
        if value is not None and (best is None or value<best):best,where=value,h
    return best,where

if __name__=='__main__':
    from math import log10
    def dl(q):return (log10(q.numerator)-log10(q.denominator))/10
    print('Base',dl(baseprice()),'losses',list(loss()))
    K=[67,967,8311,11621,50627,392233,44119464395283956806299428681]
    print('credits',[(q,dl(gain(q,1)[0]),gain(q,1)[1]) for q in K])
    print('grand',dl(baseprice()*prod(gain(q,1)[0] for q in K)))
