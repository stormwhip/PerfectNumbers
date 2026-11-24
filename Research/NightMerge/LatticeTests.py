"""Finite regression tests for integer polynomial witness replay (no FLINT/SymPy)."""
from LatticeLeaf import no_real_roots,verify,build
from math import gcd
from fractions import Fraction
import random

def main():
    assert not no_real_roots([-1,0,1],-2,2) and no_real_roots([1,0,1],-100,100)
    assert not no_real_roots([1,-2,1],-1,2) and not no_real_roots([-1,1],1,3)
    rnd=random.Random(20261125);checked=0
    for _ in range(1500):
        root=rnd.randrange(2,130);c=rnd.randrange(1,4);C=root**c*rnd.randrange(1,65);T=rnd.randrange(2,40)
        if gcd(C,T)!=1:continue
        lo=rnd.randrange(2,root+1);hi=rnd.randrange(root,root+20);dim=rnd.randrange(2,5);m=rnd.randrange(1,dim);a=[rnd.randrange(-5,6) for _ in range(dim)]
        if verify(C,c,root%T,T,lo,hi,[dim,m,a,[]]):raise ValueError('false exclusion of a planted solution')
        first,rad,mid,center,K,rows=build(C,c,root%T,T,lo,hi,dim,m);x=(root-center)//T
        assert all(sum(v*x**j for j,v in enumerate(row))%root**m==0 for row in rows);checked+=1
    print('verified Sturm boundaries and',checked,'planted integer-divisor basis invariants')
if __name__=='__main__':main()
