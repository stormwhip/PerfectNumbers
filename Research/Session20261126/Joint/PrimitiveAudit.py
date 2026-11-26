"""Independent coarse proof of the five primitive-source results.
Only e=824 and the two sides of a supply/source cut enter the checks.
"""
from math import isqrt
from fractions import Fraction

def prime(n): return n>=2 and all(n%j for j in range(2,isqrt(n)+1))
def main():
    B=10**2400;e=824
    # For r>10000 every unit costs >=10000^2. Below 10000 use a much
    # coarser single discount for every allowed prime, independent of k.
    R=10000;K=R**2; D=Fraction(1); ban=(7,11,13,19,31)
    for r in range(7,R,6):
        if r in ban or not prime(r) or any((r*r+r+1)%t==0 for t in ban):continue
        assert r>=43
        # k>=2 never costs less/unit than k=1 as soon as r^6>=K;
        # ratio of successive discounts <=K/r^6 for k>=1.
        assert r**6>K
        D*=max(Fraction(1),Fraction(K,r*r))
    # Round the total discount in the conservative direction.
    assert D<10**266
    assert 43**2186>B
    # Uniformly e>=824, f+1<q and r!=1 mod q, since q|sigma(r^f).
    assert 3**e * K**(e-8)>B*10**266 and 2*3**9-1>B.bit_length()+1
    # Uniformly b<=6, r>=5, F>5^2(2Q/3)^3 and Q>=3^s.
    # Cost one is decreasing with s because 3^4<K. Cost two increases.
    # Check a fixed dividing value of s; bounds for e>=824 only improve.
    split=701
    assert 3**4<K
    # For s<=split, e-s-6>=0 and Q>=3^s; use K^(e-s-6)/D.
    num1=3**e*3**(4*split)*25*8*K**(e-split-6)
    den1=27*10**266
    assert num1>B*den1
    # For s>=split+1 same F used twice and s>=split+1.
    num2=3**(e-6)*625*64*3**(6*(split+1));den2=729
    assert num2>B*den2
    print('PASS uniform e>=824; cutoff s=',split,'floor bounds:',len(str(num1//den1))-1,len(str(num2//den2))-1,'discount < 10^266')
if __name__=='__main__':
    assert __debug__
    main()
