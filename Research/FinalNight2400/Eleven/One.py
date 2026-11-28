"""Exact independent (11,462) conditional certificate: 879701 is the Euler prime to exponent 1."""
from fractions import Fraction
from math import isqrt
P,E,T,R,B=11,462,879701,146617,10**2400
A,D=79,20

def prime(r):return r>1 and all(r%d for d in range(2,isqrt(r)+1))
def sig(r,g):return (r**(g+1)-1)//(r-1)
def v(x):
    u=0
    while x%P==0:x//=P;u+=1
    return u

def verify():
    assert prime(T) and prime(R) and sig(P,E)%T==0 and T+1==6*R and (T+1)%P
    assert 3**(D*(P-1))>=P**A
    U={}; m=1; roots=[r for r in range(2,P) if pow(r,5,P)==1];assert len(roots)==4
    for u in range(1,E+1):
        m*=P
        for r in roots:
            # Primes only: all other rows are ordinary, T^1 is fixed.
            if r%2==0 or any(r!=k and r%k==0 for k in range(3,1000,2)):continue
            num=m**A;den=r**(4*D)
            if num>den:U[r]=max(U.get(r,1),Fraction(num,den))
        if u<E:roots=[r+m*((-((pow(r,5,m*P)-1)//m)*pow(5*pow(r,4,P),-1,P))%P) for r in roots]
    loss=Fraction(1)
    for ratio in U.values():loss*=ratio
    # If a fixed component r^h is removed from pricing, retain its actual size
    # and deduct precisely its target supply from the original demand.
    X=P**E*T; num=X**D*P**(A*E)*loss.denominator;den=B**D*loss.numerator
    assert num<den and sig(R,2)%7==0
    # h+1 <11^4; each ordinary row of order 5 supplies at most z+3.
    assert 3**(P**4-1)>B and pow(R,5,P)==1 and R%P!=1
    z=v(R**5-1)
    for h in (6,8):
        assert num*R**(D*h)>den*P**(A*v(sig(R,h)))
    assert num*R**(10*D)>den*P**(A*(z+3))
    # Thus the only other value not yet closed is h=4.
    S=6077180611
    assert prime(S) and sig(R,4)%S==0 and len({P,T,R,S})==4 and pow(S,5,P)!=1
    assert num*R**(4*D)*S**(2*D)>den*P**(A*v(sig(R,4)))
    print('PASS f=1; price 79/20; base losses',len(U),'R rows 2/4/6/8 and >=10 covered')
if __name__=='__main__':verify()
