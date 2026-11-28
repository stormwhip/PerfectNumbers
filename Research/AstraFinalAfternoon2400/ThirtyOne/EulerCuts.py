"""Exact conditional Euler exponent and ordinary source cuts for root 31."""
import json,sys
from hashlib import sha256
from math import gcd,isqrt
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from Replay import B, P, EXPECTED, BANNED, prime_small, sigma, valuation, ledger


def scan(e):
    ell=e+1
    assert prime_small(ell) and P%4==3 and all(prime_small(z) for z in BANNED)
    x=P**e; a=sigma(P,e)
    assert gcd(31,30)==1 and ell!=31 and pow(31,ell,a)==1
    assert all(a%q for q in BANNED) and gcd(a,P*(P-1))==1
    assert pow(2,a-1,a)!=1 and isqrt(a)**2!=a
    # Every divisor q is 1 mod 2ell (proof); exact elementary consequences.
    assert a%(2*ell)==1
    alpha=1
    while 5**alpha<=B:
        alpha+=4
    hits={};shape={}
    for j in range(1,e+1):
        q=2*P**j-1
        # Exact root source argument imposes q external. Check N by paying q**alpha
        # as well as an ordinary q-emitter, which is distinct from q and the root.
        qt=q
        for h in range(1,alpha,4):
            if x*a*qt>B or 2*x*qt*q>3*B:
                hits[str(j)]=h;break
            qt*=q**4
        for index in (3,5,P):
            if q<=8000:
                continue
            f_lo=(2*q)**index//3
            c=(P**j*f_lo*f_lo>B or x*q*f_lo>B)
            ex=(P**j*a*f_lo*f_lo>B or x*a*q*f_lo>B)
            if c:shape.setdefault(f'{index}:all',j)
            if ex:shape.setdefault(f'{index}:external',j)
    assert list(map(int,hits))==list(range(min(map(int,hits)), e+1))
    assert all(h0>=h1 for h0,h1 in zip(hits.values(),list(hits.values())[1:]))
    return dict(e=e, root_shard=EXPECTED[e], D_bits=a.bit_length(), first_j_by_euler_min={str(h):next((int(j) for j,m in hits.items() if m<=h),None) for h in (1,5,9,13,17,21)}, first_j_by_source_index=shape, euler_high_digest=sha256(json.dumps(hits,separators=(',',':')).encode()).hexdigest(), largest_euler_exponent_checked=alpha-4)


if __name__=='__main__':
    assert __debug__;ledger(); assert 3**8000>B
    for e in (456,466):print(json.dumps(scan(e),sort_keys=True))
