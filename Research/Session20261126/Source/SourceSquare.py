"""Integer-only independent E3 valuation-source audit. Stdlib; never edits registry."""
from fractions import Fraction
from math import isqrt
import json

B=10**2400
BAN=(7,11,13,19,31)
ES=(856,970,990,1108,1162)

def primes(n):
    s=bytearray([1])*(n+1);s[:2]=b'\0\0'
    for i in range(2,isqrt(n)+1):
        if s[i]: s[i*i::i]=b'\0'*((n-i*i)//i+1)
    return [i for i in range(2,n+1) if s[i]]

def sigma(r,h):return (r**(h+1)-1)//(r-1)

def dual(R):
    K=R**2;D=Fraction(1)
    for r in primes(R-1):
        if r in BAN or r%3!=1:continue
        d=Fraction(1); k=1
        while True:
            h=3**k-1; c=Fraction(K**k,r**h)
            if c<=1 or any(sigma(r,h)%t==0 for t in BAN):break
            d=max(d,c);k+=1
        D*=d
    return K,D.numerator,D.denominator

def main():
    assert __debug__
    # A positive ordinary supplier prime is at least 43.
    assert all(r in BAN or sigma(r,2)%7==0 for r in primes(42) if r%3==1)
    # b>=7 forces r^f >=43^2186 > B.
    assert 43**(3**7-1)>B
    # These envelopes bound disjoint other ordinary supply, independent of A.
    duals=[dual(R) for R in (43,100,200,500,1000,2000,5000,10000)]
    M=[]
    for u in range(max(ES)+1):
        M.append(max((K**u*d)//n for K,n,d in duals))
    rows=[]
    for e in ES:
        pe=3**e; least=None; worst=None; count=0
        # q must be much larger than any possible exponent f+1.
        # Ordinary supply outside q is e-s, and source f+1 <= B.bit_length().
        assert all(pe*M[e-s]>B for s in range(1,9))
        assert 2*3**9-1>B.bit_length()+1
        for s in range(1,e+1):
            Q=2*3**s-1
            for b in range(0,min(6,e-s)+1):
                # Suppose q divides sigma(r^(m-1)) with m a proper divisor
                # of f+1. Then l=(f+1)/m is odd >=3, so r^f > r^2(2Q/3)^3.
                F=max(43**(3**b-1),(43 if b else 5)**2*(2*Q)**3//27)
                lower=max(pe*Q*F*M[e-s-b], (pe//3**b)*F**2)
                assert lower>B,(e,s,b)
                if least is None or lower<least:least,worst=lower,[s,b]
                count+=1
        # Strict integer certification of decimal digit floor.
        lg=len(str(least))-1; assert 10**lg<=least<10**(lg+1)
        rows.append(dict(e=e,window=[1,e],tested=count,min_log10_floor=lg,worst_s_b=worst))
    print(json.dumps(dict(status='VERIFIED_CONDITIONAL_ONLY',proof='Every E3 source is primitive: ord_q(r)=f+1 (in particular b=0)',accepted_actuals=[],rows=rows),indent=2))
if __name__=='__main__':main()
