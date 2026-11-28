"""Independent Hensel root sanity tests with brute-force toy progression cases."""
from Prices import *
from itertools import product

def run():
    for p,cap in ((5,3),(7,4),(13,3),(19,3),(31,3),(37,2),(73,2),(107,2)):
        for o in divisors(p-1):
            if o==1:continue
            for j,m,L in root_levels(p,o,cap):
                test={x for x in range(1,m) if pow(x,o,m)==1 and all(pow(x,o//d,p)!=1 for d in divisors(o) if prime(d))}
                assert test==set(L) and len(test)==len(L),(p,o,j)
    # PR #11: prove a valid negative-loss witness is outside the minimum lift.
    p=19;o=3; w=6; f=2;b=83
    assert prime(b) and b%p==7 and 7 in root_levels(p,o,1)[0][2]
    assert b**f<p**w and vp(b**o-1,p)==1
    # CRT parity composition is checked on all residue pairs of toy coprime moduli.
    for m,n in ((19,31),(49,13),(289,3)):
        for a,b in product(range(m),range(n)):
            z,M=crt(a,m,b,n);assert z%m==a and z%n==b and 0<=z<M==m*n
    print('PASS exhaustive Hensel, CRT, and nonminimal witness',flush=True)
if __name__=='__main__':run()
