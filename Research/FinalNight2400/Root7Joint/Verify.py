"""Exact odd-atom pricing; no factoring cache, primality sieve or float tests."""
from fractions import Fraction
from math import gcd, isqrt


def roots(p, cap):
    a = [b for b in range(1,p) if (b*b+b+1)%p==0]
    assert len(a)==2
    yield 1, [0]  # absent coordinate; not an order-one root
    m=1
    for _ in range(cap):
        m *= p
        yield m,a
        a = [b+m*((-((b*b+b+1)//m)*pow(2*b+1,-1,p))%p) for b in a]


def check(f=72):
    p,t=7,21193
    assert all(t%i for i in range(2,isqrt(t)+1)) and all(883%i for i in range(2,30))
    assert t-1==8*3*883
    B=10**2400
    X=p**882*t**f
    A=(p**883-1)//6
    C=(t**(f+1)-1)//(t-1)
    assert gcd(A*C,X)==t
    D=A//t*C
    M=p**882*t**(f-1)
    assert 3**8000>B and 8000<t
    # High order pays both coordinates, reserving 32 powers for 7.
    assert (2*8000)**19 < 3**(320-38)
    assert pow(3,883,t)!=1
    assert 5**(10*(882-32))>=t**(19*(f-1))
    assert 3**(10*(2648-32))>=t**(19*(f-1))
    # order 1 at 7 and order 3 at t: h>=20; h+1 <= 3^(h/4) for h>=20
    assert 21**4<=3**20 and 22**4<3*21**4
    # 7-adic LTE increments in the cubic sector (h+1=3k).
    assert 3**(10*3*6)>7**19
    best={}
    r7=list(roots(p,882))
    for n,bs in roots(t,f-1):
        inv=1
        pinv=pow(p,-1,n) if n>1 else 0
        for m,aa in r7:
            L=m*n
            for a in aa:
                for b in bs:
                    r=a+m*(((b-a)*inv)%n)
                    if r<3 or not r%2 or 20*(r.bit_length()-1)>=19*L.bit_length(): continue
                    if r**20<L**19:
                        best[r]=max(best.get(r,1),Fraction(L**19,r**20))
            inv=inv*pinv%n
    U=Fraction(1)
    for k in best: U*=best[k]
    cut=10**480
    assert X**10*M**19*U.denominator>B**10*U.numerator*cut**9
    assert t**(f-1)<cut and C<2*cut-1 and X*D*(2*cut-1)>B
    print(f'PASS 7^882, 21193^{f}; {len(best)} exceptional odd bases; U numerator/denominator bits {U.numerator.bit_length()}/{U.denominator.bit_length()}')

if __name__=='__main__':
    check()
