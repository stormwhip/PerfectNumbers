"""A tighter exact finite s=697 and s=679 scan using a direct modulus wheel."""
from Root856 import *
from Prefix856 import possible_orders
from PrefixIn856 import mceil
from math import gcd
from hashlib import sha256
try:
    from gmpy2 import powmod
except ImportError:
    powmod=pow

@cache
def root_set(q,d):
    # d may be composite. Explicit check of all prime order divisors.
    fs=[p for p in primes(d) if d%p==0]
    for a in range(2,81):
        x=pow(a,(q-1)//d,q)
        if pow(x,d,q)!=1 or any(pow(x,d//p,q)==1 for p in fs):continue
        L=[];z=1
        for i in range(1,d):
            z=z*x%q
            if gcd(i,d)==1:L.append(z)
        assert len(set(L))==len(L)
        return L
    return None

def sieve(s,H):
    y=3**s;out=bytearray([1])*(H+1);out[::2]=bytes(H//2+1)
    for p in (3,*BAN):out[p::p]=bytes(H//p)
    for p in SMALL:
        if p in (2,3):continue
        i=pow(2*y,-1,p)
        if i<=H:out[i::p]=bytes((H-i)//p+1)
    return out

def scan(exe,s,mode):
    range_receipt(exe);assert __debug__;primitive();block();M=tariff();k=E-s;Y=3**s
    RR=[R**(2*i) for i in range(k+1)]
    if mode:
        H=mceil(s,1,RR,M);X0=X*M[k];lower=R
    else:
        X0=X*min(M[k-i]*max(A*R,RR[i]) for i in range(k+1));H=(1+isqrt(3*B//(2*X0)))//(2*Y);lower=5
    assert (mode,s,H) in ((0,697,114235),(1,679,1689429))
    C=B//X0;maxd=1+floor_pow(C//(2*Y-1),lower)
    # Wheel over m: 2Y*m−2 must be divisible by an eligible primitive d.
    # At each d solve for m=Y^−1 mod d. For interval filtering, q≤C/lower^(d−1).
    avail=sieve(s,H);table={}
    for d in possible_orders(maxd):
        u=pow(Y,-1,d);lim=min(H,(1+C//lower**(d-1))//(2*Y));u+=d*(1-u%2)
        for m in range(u,lim+1,2*d):
            if avail[m]:table.setdefault(m,[]).append(d)
    print(mode,s,H,'order-positive m',len(table),flush=True)
    kept=[];before=[]
    for m,orders in sorted(table.items()):
        q=2*Y*m-1
        if any(powmod(a,q-1,q)!=1 for a in (2,3)):continue
        before.append((m,orders))
        room=C//q;hit=[]
        for d in orders:
            if q**(d-1)<=room:hit.append(d);continue
            T=root_set(q,d)
            if T is None:hit.append(d);continue
            for r in T:
                if r<lower or r%2==0:continue
                if mode and (r%1714!=1 or r%12 not in (1,11) or A%r!=0):continue
                if r**(d-1)<=room:hit.append(d);break
        if hit:kept.append((m,hit))
    digest=sha256(repr(before).encode()).hexdigest()
    if (mode,s)==(0,697):
        assert len(table)==4796 and len(before)==77 and not kept
        assert digest=='ea89bfe769cbf4bb644c85ba38b45441e2ca1838f524cd9b22294e7e85f48e80'
    elif (mode,s)==(1,679):
        assert len(table)==60008 and len(before)==860 and not kept
        assert digest=='590021d1b4eb607347ad85c41a5d498d9c044184defa0b1c28c6da5b936c3ecc'
    print(mode,s,H,'Fermat survivors',len(before),'unresolved',kept,'digest',digest,flush=True)
    return kept
if __name__=='__main__':scan(argv[1],int(argv[2]),int(argv[3]))
