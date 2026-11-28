"""Independently check canonical (7,438) reserved Euler prior and exact graph domain."""
from functools import cache
import gzip
from hashlib import sha256
import json
from math import gcd, isqrt
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from CheckSevenForestDomains import exact_state, sig, split

R = Path(__file__).resolve().parents[1]
B = 10**2400
T = 572749682520506652634407616247
P = [(7,438),(T,10)]
TARGETS = {14,20,44,48,56,60,62,82}


def trial(p):
    return p>1 and all(p%d for d in range(2,isqrt(p)+1))


def main():
    assert __debug__
    x = 7**438*T**10
    a,c = sig(7,438)//T,sig(T,10)
    assert T%4==3 and (T-1)%4==2
    assert sig(7,438)==a*T and a%T and c%T==1 and gcd(a*c,x)==1
    assert 3**5030 <= B < 3**5031 and T>5031
    assert [d for d in range(3,5032,2) if (T-1)%d==0] == [439]
    # Exact monotone endpoints independent from the applicant calculator.
    assert x*9014**438 <= B < x*9015**438
    assert x*96**877 > B and x*93**877 <= B
    assert not any(trial(z) and z not in (7,19) and pow(z,439,T)==1 for z in range(3,9015,2))
    assert not any(trial(z) and pow(z,878,T)==1 and pow(z,2,T)!=1 for z in range(5,97,4))
    m=T**9; lo=2*m-1; modulo=4*m
    # Inverse free: lo^2 is 1 modulo 4m.
    assert lo*lo%modulo==1
    k=a*lo%modulo or modulo
    assert k>a//lo or (k+modulo>a//lo and a%k)
    assert x*a*c*lo**5>B
    live, _ = split(P,{19},67)
    assert TARGETS <= live.keys()
    data = (R/'Seven/Forest438d.json.gz').read_bytes()
    assert sha256(data).hexdigest() == '58e8aad743b97dde1b36e3600a20d4e4b6f279280d6b2f35b3786dbb42c6ca53'
    d = json.loads(gzip.decompress(data)); seen=set(); cert=set()
    for row in d['records']:
        assert not row['unresolved'] and row['bad']==[19]
        parts=[tuple(item) for item in row['P']]; h=parts[-1][1]
        assert h not in seen and parts==live[h];seen.add(h)
        _,_,M=exact_state(parts,{19}); node=row['tree']
        assert node['type']=='reserve' and 0<node['head']<=1024
        roots, owners = set(node['roots']), dict(node['owners'])
        assert len(roots)==len(node['roots']) and len(owners)==len(node['owners']) and not roots&owners.keys()
        V=roots|owners.keys()
        assert all(z%modulo!=lo for z in V) and not V & (dict(parts).keys()|{19})
        assert all(M%r==0 for r in roots) and all(M%z for z in owners)
        cert |= {str(z) for z in V|dict(parts).keys() if z>=2**64}
        for z in owners:
            visits=set()
            while z not in roots:
                assert z in owners and z not in visits
                visits.add(z);z=owners[z]
    assert seen==TARGETS and cert==d['ecpp'].keys()
    print('PASS independent Euler-source caps, reciprocal progression, eight exact graph scopes and 392 ECPP labels')


if __name__=='__main__':
    main()
