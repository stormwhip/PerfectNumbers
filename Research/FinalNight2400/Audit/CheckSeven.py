"""Independent full odd-representative enumeration for the joint (7,882) f=72 audit."""
from fractions import Fraction
from math import gcd,isqrt,prod
from hashlib import sha256
from pathlib import Path
from time import perf_counter
start=perf_counter()
p,t=7,21193
assert all(n%d for n in (t,883,7) for d in range(2,isqrt(n)+1)) and t-1==8*3*883
# Raise an order-three residue to p on moving up one level (Teichmueller).
def levels(p,k):
    yield 1,(0,)
    a=next(i for i in range(2,p) if pow(i,3,p)==1);m=p
    for _ in range(k):
        b=(-1-a)%m
        assert a!=b and all((r*r+r+1)%m==0 and gcd(2*r+1,p)==1 for r in (a,b))
        yield m, (a,b)
        m*=p;a=pow(a,p,m)
exceptions={};cases=0
T=list(levels(t,71))
for m,grp in levels(p,882):
    for n,grt in T:
        mn=m*n
        i=pow(n,-1,m) if m>1 else 0
        for s in grp:
            for z in grt:
                r=z+n*(((s-z)*i)%m);cases+=1
                assert 0<=r<mn and r%m==s and r%n==z
                if r<3 or r%2==0:continue
                if (r.bit_length()-1)*20>=mn.bit_length()*19:continue
                ratio=Fraction(mn**19,r**20)
                if ratio>1:exceptions[r]=max(exceptions.get(r,1),ratio)
U=prod(exceptions.values(),start=Fraction(1)); assert cases==(2*882+1)*(2*71+1)
B=10**2400;X=p**882*t**72;A=(p**883-1)//(p-1);C=(t**73-1)//(t-1);D=A*C//t;M=X//t;cut=10**480
assert gcd(A*C,X)==t and A%t==0 and gcd(D,X)==1
assert 3**8000>B and 8000<t and pow(3,883,t)!=1
assert 3**282 >=16000**19 and 5**8500>=t**1349 and 3**26160>=t**1349
assert 3**180>7**19
assert all(3**h>=(h+1)**4 and 10*4*h>=19*(h+12) for h in range(20,8000))
assert all(3**h>=(h+1)**2 for h in range(2,8000))
assert X**10*M**19*U.denominator > B**10*cut**9*U.numerator
assert cut>t**71 and 2*cut-1>C and X*D*(2*cut-1)>B
print('PASS representatives',cases,'exceptions',len(exceptions),'U bits',U.numerator.bit_length(),U.denominator.bit_length(),'time',round(perf_counter()-start,3))
print('PASS exact two windows, all intermediate index comparisons, primitive-order lift and branch partition')
