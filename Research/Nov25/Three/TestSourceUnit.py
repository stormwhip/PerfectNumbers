"""Exact sanity checks for the integer root, CRT enclosure and lifted balance."""
from itertools import product
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from SourceUnit import E, I, crt_divisor, iroot, order_primes, outside_order_lower


def test_arithmetic():
    for n in range(1,800):
        for k in range(1,10):
            x=iroot(n,k)
            assert x**k<=n<(x+1)**k
    for a,c,lo,hi,step,res in product(range(11,75,3),(1,2),(2,5),(12,25),(1,2,5,7),(1,2,3)):
        brute=any(a%z**c==0 and z%step==res%step for z in range(lo,hi+1))
        assert not brute or crt_divisor(a,c,lo,hi,step,res,cap=2)
    for n in range(3,200,2):
        assert set(order_primes(n))=={p for p in range(5,n+1,2) if n%p==0 and E.mr(p)}


def test_unit_and_order():
    # j=0 is allowed: the tag -1 does not imply a positive valuation.
    assert E.val(E.sigma(43,4),3)==0 and E.sigma(43,4)%3==2 and I.legal(43,4)
    for q in I.PS[:500]:
        if q%4!=1 or q%3!=2:
            continue
        s=E.val(q+1,3); y=3**s; a=(q+1)//(2*y);tag=a%3
        for f in range(2,30,2):
            if q<=f+1 or not any(E.sigma(r,f)%q==0 for r in range(5,100,2)):
                continue
            lb=outside_order_lower(y,2*y-1,f,tag)
            assert lb is not None and lb<=q


def test_lifted_balances():
    found=set()
    for e,r in ((10,23),(6,1093),(16,1871),(16,34511),(18,1597),(28,59),(28,28537)):
        P=3**(e+1);A=(P-1)//2;c=E.val(A,r)
        for f in range(max(2,c+c%2),38,2):
            S=E.sigma(r,f);u=E.val(S,3)
            for q in I.PS[2:]:
                if q%4!=1 or q%3!=2 or S%q:
                    continue
                s=E.val(q+1,3); z=3**(s+u)
                if s+u>e:
                    continue
                w=S//q;U=(P-1)//r**c;t=r**(f-c)
                D=U*w*(r-1)-U-r*t
                K=U*(w+E.sigma(r,c-1))-E.sigma(r,f-c)
                assert D%z==K%z==0 and D!=0 and K!=0
                assert t*max(P,q)*(P//z+4)>q*z
                found.add(bool(u))
    assert found=={False,True},'need both zero and positive supplier controls'


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('run without -O')
    test_arithmetic()
    test_unit_and_order()
    test_lifted_balances()
    print('PASS arithmetic, finite order constraints and both lifted balance cases')
