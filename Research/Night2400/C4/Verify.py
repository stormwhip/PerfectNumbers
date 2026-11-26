"""Exact conditional replay for q-adic fibers of the key (19,82)."""
import gzip
import json
from collections import Counter
from fractions import Fraction
from functools import cache
from hashlib import sha256
from math import prod
from pathlib import Path
import sys

H = Path(__file__).resolve().parent
R = H.parents[1]
sys.path[:0] = [str(R/'Session20261126'), str(R/'Nov25/Compose'), str(R/'FinalSprint')]
from PivotCheck import C, B, floor10
from IndependentForest import replay
from JointValuation import excludes

P, E = 19, 82
Q = 4555750199199950437649290574576123158785621674690043100726048398827989978120480865989375363338094993243
S8 = (19, 7, 11, 31, 13, 3, 5, 17)


def abundance(s, roots):
    def ratio(z, odd):
        h = max(1, C.valuation(s.D, z))
        h += (1-h)%4 if odd else h%2
        while not C.permitted(z, h, s.bad):
            h += 4 if odd else 2
        return Fraction(C.sigma(z, h), z**h)
    even = {z: ratio(z, False) for z in roots}
    base = Fraction(s.S, s.X)*prod(even.values())
    return min([base, *[base/even[z]*ratio(z, True) for z in roots if C.euler(z, s.bad)]])


def dead(s):
    return s.conflict or s.base > B or prod(C.sigma(z, e) for z, e in s.rows.items()) > 2*s.X


def verify():
    assert __debug__
    raw = (H/'Fibers19x82.json.gz').read_bytes()
    d = json.loads(gzip.decompress(raw))
    assert set(d) == {'forest','known','ecpp'}
    book, used, taken = d['ecpp'], set(), set()

    @cache
    def prime(q):
        assert type(q) is int and q > 2
        x = q
        if q >= 2**64:
            used.add(str(q))
            for row in book[str(q)]:
                assert row[0] == x and x >= 2**64
                x = C.pc.level(*row)
        assert C.pc.prime64(x)
        return True

    assert S8 == C.ORDER and all(prime(q) for q in S8) and prime(Q)
    assert Q.bit_length() == 342 and Q%4 == 3
    s = C.State([(P,E)])
    assert not dead(s) and C.valuation(s.D,Q) == 1
    scale, f = s.base//Q, 1
    alive, direct, incompatible = [], [], []
    while scale * Q**f <= B:
        if not s.possible(Q,f,1): incompatible.append(f)
        elif dead(C.State([(P,E),(Q,f)])): direct.append(f)
        else: alive.append(f)
        f += 1
    assert (alive,direct,incompatible,f)==([2,4,6,8,10], list(range(12,23,2)), list(range(1,23,2)), 23)
    assert set(d['known']) == {'2','4','6','8'}
    print('DOMAIN P19_I00021', alive,'DIRECT',direct,'TAIL >=',f,flush=True)
    open6 = []
    for f in (2,4,6,8):
        parts = [(P,E),(Q,f)]
        known = d['known'][str(f)]
        s = C.State(parts)
        assert not dead(s) and sorted(set(known))==known
        assert all(prime(q) and q not in s.rows and s.D%q==0 for q in known)
        counts = Counter(); floors = []
        for mask in range(1,256,2):
            present = tuple(q for i,q in enumerate(S8[1:],1) if mask>>i&1)
            absent = tuple(q for q in S8[1:] if q not in present)
            t = C.State(parts,present,absent)
            if dead(t): counts['direct']+=1; continue
            roots = sorted(set(known)|set(present))
            if abundance(t,roots)>2: counts['abundance']+=1; continue
            tag = f'{f}:{mask}'
            if tag not in d['forest']:
                assert f == 6
                open6.append(mask); counts['open']+=1; continue
            row = d['forest'][tag]; taken.add(tag)
            assert set(row)=={'roots','owners','head'} and roots==row['roots']
            k,o,h = roots,row['owners'],row['head']
            C.validate_forest(t,k,o,h,prime)
            x = C.Forest(t,k,o,h).lower()[0]
            assert x>B, (f,mask,floor10(x))
            labels = [Q,*k,*dict(o)]
            independent = replay(dict(assigned=parts,present=present,absent=absent,leaf=dict(kind='forest',**row),ecpp={str(z):book[str(z)] for z in labels if z>=2**64}))
            floors.append(min(floor10(x),independent)); counts['forest']+=1
        assert sum(counts.values())==128
        print('MASKS',f,dict(counts),'minimum forest floor',min(floors,default=None),flush=True)
    assert taken == set(d['forest']) and used == set(book)
    receipt = excludes([(P,E),(Q,10)],(),[0,1]); assert receipt == (7,[629,2,199])
    print('PRICE 10',receipt,'OPEN f=6 masks',open6,'SHA256',sha256(raw).hexdigest(),flush=True)

if __name__=='__main__':verify()
