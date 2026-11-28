"""Recompute root-31 strict forest arithmetic with a parity-capacity DP."""
from functools import cache
from math import gcd, lcm, prod
from pathlib import Path
import argparse
import gzip
import json
import runpy
import sys

H = Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from Check31Domains import B, BANS, state, split, vp
R = H.parents[1]

# Reuse only the frozen prime-certificate primitive, not a frontier/forest loader.
PR = runpy.run_path(str(R/'NightSevenForest/Release/PrimeCheck.py'))


def forest(row, descriptor, bans=BANS):
    X,S,ok = state(row,bans)
    assert ok
    D = lcm(X,S)//X
    assert gcd(X,D)==1
    roots = descriptor['roots']
    edges = dict(descriptor['owners'])
    vertices = {*roots,*edges}
    assert len(roots)+len(descriptor['owners'])==len(vertices)
    assert all(D%p==0 for p in roots) and all(D%p for p in edges)
    assert all(parent in vertices for parent in edges.values())
    assert not vertices.intersection((*bans,*dict(row)))
    children = {p:[q for q,parent in edges.items() if parent==p] for p in vertices}
    expected = set()
    def walk(q):
        assert q not in expected
        expected.add(q)
        for child in children[q]:
            walk(child)
    for q in roots:
        walk(q)
    assert expected == vertices
    head = descriptor['head']
    assert type(head)==int and 1<=head<=1024
    pool = X*D*prod(edges)
    ban = prod(bans)
    pick_euler = not any(e%2 for _,e in row)
    sentinel = B+1

    def join(left, right):
        # Both tuples represent a minimum for zero or at most one Euler role.
        a,b = left
        c,d = right
        return min(sentinel,a*c), min(sentinel,a*d,b*c)

    @cache
    def lower(p, required):
        ordinary = either = sentinel
        # Size alone is an admissible one-sided estimate for all unchecked tails.
        for parity in (0,1):
            if parity and (not pick_euler or p%4!=1 or gcd(p+1,ban)>1):
                continue
            step = 4 if parity else 2
            e = required + (parity-required)%step
            checked = 0
            while checked<head and p**e<(either if parity else ordinary):
                size = p**e
                h = e+1
                ss = (p*size-1)//(p-1)
                if gcd(ss,ban)==1:
                    checked += 1
                    a = ss >> vp(ss,2)
                    other = a
                    while (g:=gcd(other,pool))>1:
                        other //= g
                    value = (min(sentinel,size*other),)*2
                    for q in children[p]:
                        if a%q==0:
                            value = join(value,lower(q,vp(a,q)))
                    if parity:
                        either = min(either,value[0])
                    else:
                        ordinary,either = min(ordinary,value[0]),min(either,value[1])
                e += step
            tail = p**e
            if not parity:
                ordinary = min(ordinary,tail)
            either = min(either,tail)
        return ordinary,either

    v = (1,1)
    for p in roots:
        v = join(v,lower(p,vp(D,p)))
    factor = X*(D//prod(p**vp(D,p) for p in roots))
    return factor*v[int(pick_euler)]


def accept(path):
    data=json.loads(gzip.decompress(path.read_bytes()))
    ecpp=data['ecpp']; seen=set(); strict=[]; spans=[]

    @cache
    def prime(p):
        assert type(p)==int and p>=3
        if p>=2**64:
            key=str(p)
            seen.add(key)
            assert ecpp[key]
            for row in ecpp[key]:
                assert row[0]==p
                p=PR['level'](*row)
        assert PR['prime64'](p)

    def visit(row, n):
        if n is None:
            return False
        if n['type']=='forest':
            for z in (*n['roots'],*(z for z,_ in n['owners'])):
                prime(z)
            out = forest(row,n)
            assert out>B,row
            strict.append(out)
            return True
        assert n['type']=='split'
        q=n['q']; prime(q)
        domain, tail=split(row,q)
        assert set(map(str,domain))==n['cases'].keys()
        spans.append((q,sorted(domain),tail))
        return all([visit(new,n['cases'][str(e)]) for e,new in domain.items()])

    p=31; e=data['e']; q=data['pivot']; prefix=((p,e),)
    prime(p)
    if q is not None:
        prime(q); domain,tail=split(prefix,q)
    else:
        domain,tail={e:prefix},None
    assert set(map(str,domain))==data['cases'].keys()
    good=[f for f,row in domain.items() if visit(row,data['cases'][str(f)])]
    assert seen==ecpp.keys()
    print('PASS independent exact-sigma splitting and parity-capacity forest DP', path.name,
          'initial count/tail', (len(domain),tail), 'strict leaves',len(strict), 'ECPP',len(seen), 'accepted fibers',good)
    print('Nested exact domains:',spans)
    if strict:
        print('Minimum lower bound floor(log10)',min(len(str(v))-1 for v in strict))


if __name__=='__main__':
    assert __debug__
    parser=argparse.ArgumentParser()
    parser.add_argument('packets',nargs='+',type=Path)
    for file in parser.parse_args().packets:
        accept(file)
