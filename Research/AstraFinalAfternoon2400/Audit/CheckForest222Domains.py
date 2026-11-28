"""Independently reconstruct the issued 222 deep domains and forest support."""
import gzip
from hashlib import sha256
import json
from math import lcm, prod
from pathlib import Path
import subprocess

BASE = '495c59f55456a70994ce7848487e0c4e262c1984'
R = Path(__file__).resolve().parents[1]
B = 10**2400
T, U = 7579985624053, 3705121363


def parts(rows):
    if sum(h % 2 for p,h in rows) > 1 or any(h % 2 and (h % 4,p % 4)!=(1,1) for p,h in rows):
        return None
    x = prod(p**h for p,h in rows)
    z = prod(sum(p**i for i in range(h+1)) for p,h in rows)
    odd = z // (z & -z)
    m = lcm(x,odd)
    if z <= 2*x and m <= B and all(odd % p**(h+1) for p,h in rows):
        return m


def live(rows, q):
    m = parts(rows)
    assert m and m % q == 0 and q not in dict(rows)
    lower = 0
    while m % q == 0:
        m //= q
        lower += 1
    legal = set()
    f = lower
    while m*q**f <= B:
        if parts(rows+[(q,f)]):
            legal.add(f)
        f += 1
    return legal, f


def main():
    assert __debug__
    raw = (R/'Nineteen/Forest222.json.gz').read_bytes()
    assert sha256(raw).hexdigest() == '4f5d3a750a8f1d6bc120e6e2217157172f146ffd3c0d7df6a9924997e0941440'
    oldraw = subprocess.check_output(['git','show',BASE+':Research/FinalNight2400/Root222/ThirdForests.json.gz'],cwd=R)
    old = json.loads(gzip.decompress(oldraw))['cases']
    overlay = json.loads(subprocess.check_output(['git','show',BASE+':Research/GeminiFrontier/November28/Results.json'],cwd=R))
    roll = next(x for x in overlay['Entries'] if x['Key']==[19,222])
    assert roll['Fixed']==[[str(T),1]] and roll['Excluded']==[58]
    assert roll['Further']['Fixed']==[[str(U),16]] and roll['Further']['Excluded']==[40,42]
    wanted = {(1,2): {12,42}, (2,2):{2,28}, (18,2):{8,16}, (18,16):{8}, (18,22):{8}}
    pack = json.loads(gzip.decompress(raw))
    assert pack['frozen'] == BASE
    assert sha256(oldraw).hexdigest() == pack['thirds_sha256']
    group = {}
    primes = set()
    for row in pack['cases']:
        p = [tuple(x) for x in row['prefix']]
        assert p[0]==(19,222) and p[1][0]==T and p[2][0]==U
        f,g = p[1][1],p[2][1]
        q,j = p[3]
        scope = f'{f}:{g}'
        hist = old[scope]
        assert q == hist['q'] and j in hist['left']
        assert j in wanted[(f,g)] and j not in group.setdefault((f,g),set())
        group[(f,g)].add(j)
        for i in (1,2):
            assert p[i][1] in live(p[:i],p[i][0])[0]
        viable, first_invalid = live(p[:3],q)
        assert viable == {int(x) for x in hist['children']} | set(hist['left'])
        assert not {int(x) for x in hist['children']} & set(hist['left'])
        assert first_invalid == pack['windows'][scope]['strict_raw_tail']
        m = parts(p)
        K, edges, head = row['forest']; k, owners = set(K), dict(edges)
        assert len(k)==len(K) and len(owners)==len(edges) and not k & owners.keys() and 0<head<=1024
        assert all(m % v == 0 and v not in dict(p) for v in k)
        for v in owners:
            assert m % v and v not in dict(p)
            visited=set()
            while v not in k:
                assert v in owners and v not in visited
                visited.add(v)
                v = owners[v]
        primes.update(k | owners.keys() | dict(p).keys())
    assert group == wanted
    assert set(pack['ecpp']) == {str(q) for q in primes if q>=2**64}
    print('PASS independently reconstructed 5 frozen deep domains, 8 new prefixes, 157 reached ECPP labels')


if __name__ == '__main__':
    main()
