"""Close the first internal-source 856 windows by exact Euler-prefix bounds."""
from Root856 import *
from math import gcd
from Prefix856 import prod_small_odd, possible_orders
from hashlib import sha256


def feasible(q,s,i,RR,M):
    y=3**s;k=E-s;r=RR[i];u=X*q*M[k-i]
    if u*max(A*R,r)>B or 2*u*q*r>3*B:return False
    d=max(W,q)*(W//y+4)
    return u*q*y*max(A,r)<=B*d


def mceil(s,tag,RR,M):
    y=3**s;k=E-s
    def good(m):
        q=2*y*m-1
        return any(feasible(q,s,i,RR,M) for i in range(k+1))
    lo,hi=0,1
    if not good(1):return 0
    while good(hi):hi*=2
    while lo+1<hi:
        h=(lo+hi)//2
        if good(h):lo=h
        else:hi=h
    return lo


def run(exe):
    range_receipt(exe);assert __debug__;primitive();block();M=tariff();RR=[R**(2*i) for i in range(E+1)]
    rows=[]
    for s in (678,):
        y=3**s;k=E-s;H=mceil(s,1,RR,M)
        assert H==911
        qtest=[];q0count=0
        for m in range(1,H+1,2):
            if gcd(m,3*7*11*13*19*31)>1:continue
            q=2*y*m-1
            if any(q%p==0 for p in SMALL):continue
            # Internal emitter is disjoint from ALL other ordinary 3 suppliers.
            room=B//(X*q*M[k]);dm=1+floor_pow(room,R)
            ds=[d for d in possible_orders(dm) if (q-1)%d==0]
            if not ds:continue
            q0count+=1
            if pow(2,q-1,q)!=1 or pow(3,q-1,q)!=1:continue
            qtest.append((m,ds))
        assert q0count==35 and qtest==[(313,[13])]
        rows.append((s,H,q0count,len(qtest),qtest));print(rows[-1],flush=True)
    from Single856 import run as finish
    finish()
    return rows
if __name__=='__main__':run(argv[1])
