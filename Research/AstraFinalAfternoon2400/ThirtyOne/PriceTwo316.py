"""Exact fixed-Euler joint price for two exceptional descendants of (31,2), 331^316."""
from functools import cache
from fractions import Fraction
from itertools import product
import json,sys
from pathlib import Path
from math import gcd,isqrt,lcm,prod
sys.path.insert(0,str(Path(__file__).resolve().parent))
from Replay import B,BANNED,SMALL,state,prime_small,valuation,roots as tiny_roots
from GenericPrice import roots as huge_roots,domain
T=331;P=1510189
TORD=(3,5,11,15,33,55,165)


def check(row):
    assert __debug__ and row in {((31,2),(331,316),(1510189,f),(3,2),(13,2),(61,1)) for f in (52,58)}
    assert prime_small(T) and prime_small(P) and T-1==2*3*5*11 and P>8000 and 3**8000>B
    x,s,d,bs,ok=state(row);assert ok and sum(h%2 for _,h in row)==1
    nt,np=(dict(row)[z]-valuation(s,z) for z in (T,P));assert nt==315 and np==dict(row)[P]-1
    PO=domain(P);assert all(o%T for o in PO) and all(o%P for o in TORD)
    # w=2: only simultaneous cubic orders share their whole reserve. If one
    # charge is higher, reserve h=o-3, then both separate allowances fit L-1.
    reserve=lambda o:0 if o in (1,3) else o-3
    for a,b in product((1,*TORD),(1,*PO)):
        assert (2 if 3 in (a,b) else 0)+reserve(a)+reserve(b)<=lcm(a,b)-1
    assert 3**(T-1)>=T*T
    cap=B//(x*d);loss={};counts=[]
    def maybe(y):return y>=3 and y%2 and y not in dict(row) and y not in BANNED and all(y==k or y%k for k in SMALL) and pow(2,y-1,y)==1
    def add(y,h,goal):
        if y<3 or not y%2 or (y.bit_length()-1)*h>=goal.bit_length():return
        v=y**h
        if v>=goal or v//gcd(v,d)>cap or not maybe(y):return
        p=loss.get(y)
        if p is None or p[0]*v<goal*p[1]:loss[y]=goal,v
    def pay():
        u=10**8
        for p,q in loss.values():u=-(-(u*p)//q)
        counts.append(len(loss));loss.clear()
        return -(-u//10**8)
    A=tiny_roots(T,3,nt);E=((1,(0,)),*huge_roots(P,3,np))
    for v,rs in E:
        inv=1;step=pow(T,-1,v) if v>1 else 0
        for u,ss in A:
            for r,z in product(ss,rs):add(r+u*((z-r)*inv%v),2,(u*v)**2)
            inv=inv*step%v
    U=pay()
    for t,depth,os,R in ((T,nt,TORD,lambda p,o,z:tiny_roots(p,o,z)[1:]),(P,np,PO,huge_roots)):
        for o in os:
            if o==3:continue
            h=o-3
            if 3**h>=t**(2*depth):continue
            assert h>=2
            for m,rr in R(t,o,depth):
                for r in rr:add(r,h,m*m)
        U*=pay()
    return dict(first331=316,second1510189=dict(row)[P],losses=counts,U_digits=len(str(U)),excluded=x*(T**nt*P**np)**2>B*U)

if __name__=='__main__':
    for f in (52,58):print(json.dumps(check(((31,2),(331,316),(1510189,f),(3,2),(13,2),(61,1)))),flush=True)
