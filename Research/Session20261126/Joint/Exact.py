"""Standalone stdlib-only INTEGER global E3a base verification given the certified R.
Prove R separately via Trial.cpp or Range.py. Returns integral log10 floor.
"""
from functools import cache
from math import gcd,isqrt
E=1162;A=(3**1163-1)//2;P=3**E;B=10**2400;R=10670571520001
BAN=(7,11,13,19,31)
@cache
def extra(s):
    return min(81**(E-s-i)*max(A*R,R**(2*i)) for i in range(E-s+1))

def sourcefree(q):
    cap=B//(P*A*q);assert cap<q*q and cap<3**1800
    roots={}
    for f in range(2,1800,2):
        d=gcd(f+1,q-1)
        if d==1:continue
        if d not in roots:
            for a in range(2,64):
                g=pow(a,(q-1)//d,q);z=g;xs=[1]
                while z!=1 and len(xs)<d:xs.append(z);z=z*g%q
                if len(xs)==d and z==1:break
            else:return False
            roots[d]=min(xs[1:])
        # Exponent monotonic: for fixed d, the smallest f already gives the strongest test.
        if roots[d] is not None:
            if pow(roots[d],f)<=cap:return False
            roots[d]=None
    return True

def verify_base(target=2219,verbose=False):
    assert __debug__ and A%8==5 and R==1+2326*65536*70000
    sieve=bytearray(b'\1')*50000
    for p in range(2,isqrt(len(sieve)-1)+1):
        if sieve[p]:sieve[p*p::p]=bytes((len(sieve)-1-p*p)//p+1)
    primes=[p for p in range(5,len(sieve),2) if sieve[p]]
    total=0;cases=[]
    for s in range(1020,E+1):
        # The lower bound is 2*P*q^2*extra(s)/3. Include equality in the low prefix.
        ymax=isqrt((3*10**target)//(2*P*extra(s)));y=3**s;l=(1+ymax)//(2*y)
        if not l:continue
        ss=bytearray(b'\1')*(l+1);ss[::2]=bytes(l//2+1)
        for p in (*BAN,3):ss[::p]=bytes(l//p+1)
        for p in primes:
            k=pow(2*y,-1,p)
            if k<=l:ss[k::p]=bytes((l-k)//p+1)
        for m in range(1,l+1,2):
            if not ss[m]:continue
            q=2*m*y-1
            if pow(2,q-1,q)!=1:continue
            assert sourcefree(q),(s,m);cases.append((s,m))
        total+=l
    if verbose:print(dict(target=target,prefix=total,conditional_sources_excluded=cases))
    return target
if __name__=='__main__':print(verify_base(verbose=True))
