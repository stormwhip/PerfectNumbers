"""Special complete CRT emitter elimination for the sole low internal q point."""
from Root856 import *
from PrefixIn856 import feasible
from math import gcd


def run():
    assert __debug__
    s,m,d=678,313,13;Y=3**s;q=2*Y*m-1;assert (q-1)%d==0
    k=E-s;M=tariff();RR=[R**(2*i) for i in range(E+1)]
    opts=[i for i in range(k+1) if feasible(q,s,i,RR,M)]
    assert opts
    # Once q and order fixed and q prime, r lies in exact-order roots mod q.
    # Because h=12 and exact supplier disjointness (outside-A credit not used
    # here), r^12<=B/(X*q*M[k]) giving r<q.
    C=B//(X*q*M[k]);assert q**(d-1)>C
    h=next(pow(a,(q-1)//d,q) for a in range(2,100) if pow(a,q-1,q)==1 and pow(a,(q-1)//d,q)!=1)
    assert pow(h,d,q)==1 and h!=1
    roots=[pow(h,j,q) for j in range(1,d)];assert len(set(roots))==d-1
    for r in roots:
        assert r%1714!=1 or r%12 not in (1,11) or r%2==0 or r<R or r**(d-1)>C or A%r!=0
    print('PASS internal 678 last (m,d)',m,d,'i viable',opts,'roots',len(roots),flush=True)
if __name__=='__main__':run()
