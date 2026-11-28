"""Offline adversarial regressions for lift coverage, cofactor scans and paid support."""
from fractions import Fraction
from math import isqrt, prod
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from Propagation import partition, outside_progression, val, odd_price, introot


def tests():
    # Stress the omitted residue mechanism from PR #11: p=19, o=3,
    # w=6 > o-1. 83 lies above modulus 19 and gives a genuine loss.
    B=10**8
    U,N,o,L=odd_price(19,1,6,1,B,20,lambda x:x>=3 and x%2==1)
    brute={}
    for x in range(3,isqrt(19**6-1)+1,2):
        if x%19!=1 and pow(x,3,19)==1 and x*x<=B:
            brute[x]=Fraction(19**6,x*x)
    # Order 9 also divides 18, but 3^8 <= 19^6; add its independent losses.
    for x in range(3,introot(19**6-1,8)+1,2):
        if pow(x,9,19)==1 and pow(x,3,19)!=1 and x**8<=B:
            brute[x]=max(brute.get(x,1),Fraction(19**6,x**8))
    assert L==brute and U==prod(brute.values()) and L[83]>1 and o>0 and N>o
    try:
        odd_price(19,1,6,1,B,20,lambda x:x>=3 and x%2==1,quota=1)
    except ValueError: pass
    else: raise AssertionError('insufficient budget must fail, not truncate')
    # An Euler divisor only at a nonleast lift; additionally test a quota
    # exhaustion and both endpoints of a genuinely empty interval.
    assert not outside_progression(83*101,7,19,8,200)
    assert not outside_progression(83*101,7,19,8,200,quota=0)
    assert outside_progression(83*101,7,19,8,82)
    assert not outside_progression(83*101,7,19,83,83)
    assert outside_progression(83*101,7,19,84,100)
    emitted=[3**2*5*7,5**3*11,3**4*11**2*13,7**2*17]
    out=partition(emitted,13,(5,11))
    assert sorted(b for b,_ in out)==sorted([3**6,5**4,7**3,11**3,17])
    assert all(vec==tuple(q**val(z,q) for z in emitted)
               for q in (3,5,7,11,17) for b,vec in out if b%q==0)
    for k in [1,2,3,9,23,256]:
        for n in range(200):
            x=introot(n,k)
            assert x**k<=n<(x+1)**k
    print('PASS all-lift coverage above modulus, resource-cap fail closed, exact cofactor and paid supports')

if __name__=='__main__':
    tests()
