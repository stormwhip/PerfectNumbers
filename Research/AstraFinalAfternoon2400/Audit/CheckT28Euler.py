"""Independent exponent partition, parity feedback and lifted class cap for (19,276), t^28."""
from fractions import Fraction
from functools import cache
from math import isqrt,lcm,prod

B=10**2400
P,T,S=19,1176672733,1109

@cache
def sigma(q,h):
    z=0
    for _ in range(h+1):z=z*q+1
    return z

def vp(n,p):
    a=0
    while n%p==0:n//=p;a+=1
    return a

def prime(q):return q>1 and all(q%d for d in range(2,isqrt(q)+1))

def main():
    assert __debug__ and all(map(prime,(P,T,S,277)))
    assert S%4==1 and P-1==2*9 and S-1==4*277 and 277*S>5031
    x=P**276*T**28;y=sigma(P,276)*sigma(T,28)
    assert vp(lcm(x,y),S)==1
    raw=lcm(x,y)//S; tail=1
    while raw*S**tail<=B:tail+=1
    live=[]
    for h in range(1,tail,4):
        X=x*S**h; a=y*sigma(S,h); odd=a//(a&-a)
        if a<=2*X and lcm(X,odd)<=B and all(vp(odd,q)<=k for q,k in ((P,276),(T,28),(S,h))):live.append(h)
    assert tail==394 and len(live)==50 and live[0]==1
    assert (2*S+1)**(S-1)>B and x*25000000**276>B
    r=[i for i in range(1,S) if pow(i,277,S)==1 and i>1]
    m=S; assert len(r)==276
    for z in range(1,5):
        low=min(i if i%2 else i+m for i in r)
        if z==4:
            assert low>=25000000
            break
        assert low**276>=S**(100*z)
        r=[pow(i,S,m*S) for i in r];m*=S
        assert len(set(r))==276 and all(pow(j,277,m)==1 for j in r)
    assert S%P!=1 and vp(S**3-1,P)==1 and P**3>5031
    # The weight-two loss bound for 19 is independently reconstructed in
    # Check19x276x1109x4.py at cap 276 and with the same omitted fixed bases.
    assert x*S**405*P**(2*(276-vp(y,P)-3))>B*10**6
    F=(3,5,37); assert 555==prod(F)
    bans=(7,11,13,17,23,29,31)
    assert all(prime(q) and q not in (P,T,S) for q in F+bans)
    I=lambda q,k:Fraction(sigma(q,k),q**k)
    fixed=I(P,276)*I(T,28)*I(S,1)
    for q in bans:assert fixed*prod(I(p,2) for p in F)*I(q,2)>2
    for e in (2,4):
        for q in F:assert any(sigma(q,e)%p==0 for p in bans)
    assert fixed*prod(I(p,6) for p in F)>2
    print('PASS independently rebuilt 50 Euler exponents, strict size tail 394, every lift class and h=1 abundance feedback')

if __name__=='__main__':main()
