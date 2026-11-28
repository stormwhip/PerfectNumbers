"""Exact replay of the first exterior-source Euler multiplier windows at 856."""
from Root856 import *
from math import gcd
from hashlib import sha256

@cache
def possible_orders(dmax):
    return [d for d in range(5,dmax+1,2) if d%3]

def run(exe):
    range_receipt(exe); assert __debug__; primitive(); block()
    M=tariff(); data=[]
    for s in (696,697) if '--next' in argv else (696,):
        y=3**s;k=E-s
        xnet=min(M[k-i]*max(A*R,R**(2*i)) for i in range(k+1));pre=X*xnet
        Q=2*y-1; maxd=1+floor_pow(B//(Q*pre),5);L=tuple((d,5**(d-1)) for d in possible_orders(maxd)); lc=prod_small_odd(maxd)
        # N > (2/3) pre q^2, from the compulsory A-support and all 3 supply
        # disjoint from the exterior emitter. Use a weak closed endpoint.
        H=(1+isqrt(3*B//(2*pre)))//(2*y)
        assert H in (74,114235)
        n0=n1=n2=n3=0;left=[]
        for m in range(1,H+1,2):
            if gcd(m,3*7*11*13*19*31)>1:continue
            q=2*y*m-1;n0+=1
            if any(q%p==0 for p in SMALL):continue
            # Check order membership and cheapest feasible source mass first.
            # Every possible f satisfies r^f≤B/(q pre), r≥5. q is primitive,
            # exactly ord_q(r)=f+1, so f+1|q−1 and 3 does not divide f+1.
            room=B//(q*pre);d0=gcd(q-1,lc)
            ds=[d for d,z in L if d0%d==0 and z<=room]
            if not ds:continue
            n1+=1
            if pow(2,q-1,q)!=1 or pow(3,q-1,q)!=1:continue
            n2+=1
            # If r<q, every base is its least positive residue. Reconstruct
            # each relevant finite cyclic group without assuming q is prime:
            # primality is required only for an actual OPN Euler prime. For a
            # conditional q show generator has exactly d powers, then any
            # actual primitive source must be in this list.
            assert room<q*q
            used=[]
            for d in ds:
                a=next((pow(j,(q-1)//d,q) for j in range(2,180) if pow(j,q-1,q)==1 and all(pow(j,(q-1)//p,q)!=1 for p in primes(d) if d%p==0)),None)
                if a is None:used.append(d);continue
                roots=[];z=1
                for h in range(1,d):
                    z=z*a%q
                    if gcd(h,d)==1:roots.append(z)
                assert a*z%q==1 and len(set(roots))==len(roots)
                if any(r>=5 and r%2 and r**(d-1)<=room for r in roots):used.append(d)
            if used:left.append((m,used));n3+=1
        row=(s,H,n0,n1,n2,n3,left)
        if s==696:assert row==(696,74,16,3,0,0,[])
        print(row,flush=True);data.append(row)
    return data

@cache
def prod_small_odd(n):
    # LCM of all feasible d (just odd <=n except multiples of 3); no q
    # primality assumption in this performance optimization.
    z=1
    for p in primes(n):
        if p<=3:continue
        h=p
        while h*p<=n:h*=p
        z*=h
    return z
if __name__=='__main__':run(argv[1])
