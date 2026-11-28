"""Exact factor-count restrictions for the unfactored Phi_809(7)."""
from fractions import Fraction
from math import gcd, prod
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from VerifyLattice import A, L, run

P,E=7,808
X=P**E
B=10**2400
C=10**7


def mod_roots(o):
    m=P
    roots=[r for r in range(2,P) if pow(r,o,P)==1 and all(pow(r,j,P)!=1 for j in range(1,o) if o%j==0)]
    for v in range(1,E+1):
        yield v,m,roots
        n=m*P
        roots=[r+j*m for r in roots for j in range(P) if pow(r+j*m,o,n)==1]
        m=n


def allowances():
    loss={}
    for v,m,rs in mod_roots(3):
        for r in rs:
            if r>=3 and r%2 and r not in (7,19) and pow(2,r-1,r)==1:
                loss[r]=max(loss.get(r,1),Fraction(m*m,r*r))
    assert prod(loss.values())<579125
    # High Euler exponent. Test each exact order and capped basic depth.
    # Any prime q>=7^z already pays the valuation with two of at least five powers.
    for o in (2,3,6):
        for v,m,rs in mod_roots(o):
            for q in rs:
                if q>=5 and q%4==1 and q!=19 and pow(2,q-1,q)==1:
                    assert q**5>=m*m
    assert 3**6>=P**2
    for o in (2,3,6):
        for j in range(1,5):
            assert o*P**j-6>=6*j
    assert 3**5030<=B<3**5031 and 7**5>5031


def verify():
    assert A%809 and all(809%j for j in range(2,29)) and gcd(A,42)==1 and pow(2,A-1,A)!=1
    assert all(pow(7,809,r)!=1 for r in range(L+1,C+1,L))
    assert pow(A,3,7)==1 and pow(A,3,49)!=1
    # At v>=227 no internal prime divisor; at v>=140 it cannot occur with multiplicity >=2.
    run(227,1);run(140,2)
    for v,m,rs in mod_roots(3):
        if v>=227:break
        for b in rs:
            r=b+m*((1-b)*pow(m,-1,L)%L)
            acc=1
            for y in range(r,C*m+1,L*m):acc=acc*y%A
            assert gcd(acc,A)==1, (v,b)
    allowances()
    U=579125
    # If A has two factors, one has base-depth 1 or is order-one. Its total supply <=5.
    low=5
    for u in range(231):
        extra=1 if u<144 else C*7**(u-4)
        # High Euler (external or internal, the latter priced as an A-prime), or q^1 s=0.
        # Internal q^1 receives separate allowance below; all covered internal high-u labels have exponent >=2.
        assert X*A*P**(2*(E-low-u))*extra>B*U
    for s in range(1,E+1):
        # Linear Euler exterior AND squarefree A: pay A^2, plus exterior pricing.
        q=2*P**s-1
        assert X*A*A*q*P**(2*max(0,E-low-230-s))>B*U
    # Linear Euler inside squarefree A: independently bound N by price*q and by mass/q.
    # At most one ordinary A-prime can still emit (u<=230). Internal q contributes s=0 by reciprocity.
    assert (X*A*A*P**(2*(E-230)))*(X*P**(2*E))>(B*U)**2
    # If A has exactly two primes and q^1 is one of them, let the other supply u;
    # its extra factor (if any) is disjoint from all outside A-prime suppliers.
    # The internal q has s=0; independently price all ordinary atoms to get q<=B U/(X 7^(2E)).
    # The basic X*A term with exterior pricing is enough even without using that upper q cap.
    for u in range(231):
        extra=1 if u<144 else C*7**(u-4)
        assert X*A*P**(2*(E-u))*extra>B*U
    # Linear exterior q with s=0 and squarefree A yields same full A^2 mass as the s>0 cases.
    assert 5*X*A*A*P**(2*(E-low-230))>B*U
    print('PASS for (7,808): <=2 distinct A-primes impossible if A squarefree, or if Euler high/linear with s=0')

if __name__=='__main__':
    assert __debug__
    verify()
