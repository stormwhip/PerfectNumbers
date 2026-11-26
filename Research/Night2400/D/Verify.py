"""Cold-check the 21 residual masks at (19,316), using two exact forest recurrences.

Use python -I -S -B Research/Night2400/D/Verify.py at the frozen repository.
No discovery tools, generated caches, or prior verdicts are used. In addition
to the 57 projected masks, verify all other masks to close the exact exponent
without trusting the projection or any prior support exclusion.
"""
from pathlib import Path
from functools import cache
from fractions import Fraction
from hashlib import sha256
from math import gcd, prod
import argparse, gzip, json, sys

H = Path(__file__).resolve().parent
R = H.parents[1]
sys.path[:0] = [str(R / 'Session20261126'), str(R / 'Nov25/Compose')]
from PivotCheck import C, floor10
from IndependentForest import replay as second_forest

S8 = (19,7,11,31,13,3,5,17)
P, E, Q = 19, 316, 1255900817071954721881883552067931
B = 10**2400


def sigma(q, f):
    return (q**(f+1)-1)//(q-1)


def val(a, q):
    v = 0
    while a % q == 0:
        a //= q
        v += 1
    return v


def support(m):
    assert type(m) is int and 0 < m < 256 and m & 1
    return tuple(q for i,q in enumerate(S8[1:],1) if m >> i & 1), tuple(q for i,q in enumerate(S8[1:],1) if not m >> i & 1)


def domain(m):
    """Raw split, including all legal f above the live range up to the exact tail."""
    _, a = support(m)
    A = sigma(P,E)
    x = P**E
    c = val(A,Q)
    assert c >= 1
    forced = x*(A//Q**c)
    alive = []
    f = c
    while forced*Q**f <= B:
        if Q % 4 == f % 4 == 1 or f % 2 == 0:
            fixed = x * Q**f
            raw = A * sigma(Q,f)
            odd = raw // (1+f%2)
            remainder = odd
            for q in (P,Q):
                if val(odd,q) > (E if q == P else f):
                    break
                remainder //= q**val(odd,q)
            else:
                if fixed*remainder <= B and gcd(odd*Q,prod(a)) == 1 and raw <= 2*fixed:
                    alive.append(f)
        f += 1
    assert forced*Q**(f-1) <= B < forced*Q**f
    return alive, f


def proving_primes(table):
    seen = set()
    @cache
    def prime(q):
        assert type(q) is int and q > 2
        n = q
        if q >= 2**64:
            chain = table[str(q)]
            assert chain
            for level in chain:
                assert level[0] == n
                n = C.pc.level(*level)
            seen.add(str(q))
        assert C.pc.prime64(n)
        return True
    return prime, seen


def forest(rows, present, absent, leaf, table, prime):
    s = C.State(rows, present, absent)
    assert not s.conflict and s.base <= B
    k,o,h = (leaf[n] for n in ('roots','owners','head'))
    C.validate_forest(s,k,o,h,prime)
    first = C.Forest(s,k,o,h).lower()[0]
    assert first > B, ('first forest underpriced',rows,present,absent,floor10(first))
    labels = set(dict(rows)) | set(k) | set(dict(o)) | set(present) | set(absent)
    independent = second_forest(dict(assigned=rows,present=present,absent=absent,leaf=dict(kind='forest', roots=k, owners=o, head=h),ecpp={str(q): table[str(q)] for q in labels if q >= 2**64}))
    return min(floor10(first),independent)


def abundant(rows, present, absent, roots, prime):
    """Minimize the exact elementary abundancy over one optional Euler factor."""
    s = C.State(rows, present, absent)
    assert not s.conflict and not s.fixed_euler
    assert sorted(set(roots)) == roots
    assert all(prime(q) and q not in s.rows and q not in absent and (q in present or s.D%q == 0) for q in roots)
    def earliest(q, odd):
        j = max(1,val(s.D,q))
        step = 4 if odd else 2
        j += (1-j)%4 if odd else j%2
        while not all(pow(q,j+1,b*(q-1)) != 1 for b in absent):
            j += step
        return Fraction(sigma(q,j), q**j)
    even = {q: earliest(q,False) for q in roots}
    norm = Fraction(prod(sigma(q,f) for q,f in rows),s.X)*prod(even.values())
    values = [norm]
    for q in roots:
        if q%4 == 1 and gcd(q+1,prod(absent)) == 1:
            values.append(norm/even[q]*earliest(q,True))
    lb = min(values)
    assert lb > 2, ('abundancy not strict', lb)
    return lb.numerator*10**6//lb.denominator


def verify(packet):
    if not __debug__:
        raise RuntimeError('assertions required; do not use -O')
    old = json.loads(gzip.decompress((R/'FinalSprint/Support/Pivot316.json.gz').read_bytes()))
    source = json.loads((R/'Session20261126/OpenSupport.json').read_bytes())
    assert source['order'] == list(S8)
    all_masks = source['rows']['19:316']
    assert sorted(set(all_masks)) == all_masks and len(all_masks) == 57
    old_masks = old['masks']
    assert sorted(set(old_masks)) == old_masks and len(old_masks) == 36 and set(old_masks) <= set(all_masks)
    missing = sorted(set(all_masks)-set(old_masks))
    raw = packet.read_bytes()
    d = json.loads(gzip.decompress(raw))
    assert set(d) == {'cases','ecpp'} and sorted(d['cases'],key=int) == list(map(str,missing))
    op, ou = proving_primes(old['ecpp'])
    np, nu = proving_primes(d['ecpp'])
    assert op(P) and op(Q) and np(Q) and val(sigma(P,E),Q) == 1
    assert Q % 4 == 3
    history = {}
    for row in old['rows']:
        f = row['f']
        assert f > 0 and f not in history and (not f%2 or Q%4 == f%4 == 1)
        history[f] = forest([(P,E),(Q,f)],(),(),row,old['ecpp'],op)
    assert set(history) == {6,8,10,12,14,16,18,20,22,24} and ou == set(old['ecpp'])
    for m in old_masks:
        fs, tail = domain(m)
        assert tail == 50 and set(fs) <= set(history), (m,fs)
    # The projection is convenient for reporting, but not trusted for completeness.
    # Every odd mask is a possible S8 intersection for a candidate with 19 present.
    extras = {'old_forest_or_direct': 0, 'root_abundance': 0}; extra_floors = []
    for m in sorted(set(range(1,256,2))-set(all_masks)):
        fs, tail = domain(m)
        assert tail == 50
        if set(fs) <= set(history):
            extras['old_forest_or_direct'] += 1
        else:
            present, absent = support(m)
            extra_floors.append(abundant([(P,E)],present,absent,list(sorted(present)),op))
            extras['root_abundance'] += 1
    assert extras == {'old_forest_or_direct': 36, 'root_abundance': 35}
    assert len(all_masks)+sum(extras.values()) == 128
    counts={'abundance':0,'forest':0}; fs_counts = {}; min_floor = None
    for m in missing:
        f0, tail = domain(m)
        assert tail == 50
        t = d['cases'][str(m)]; f=t['f']; kind=t['kind']
        assert set(f0) - set(history) == {f}, (m,f0,f)
        fs_counts[f] = fs_counts.get(f,0)+1
        present, absent = support(m)
        rows = [(P,E),(Q,f)]
        if kind == 'abundance':
            assert set(t) == {'f','kind','roots'}
            level = abundant(rows,present,absent,t['roots'],np)
        else:
            assert kind == 'forest' and set(t) == {'f','kind','roots','owners','head'}
            level = forest(rows,present,absent,t,d['ecpp'],np)
            min_floor = level if min_floor is None else min(min_floor,level)
        counts[kind] += 1
        print('PASS', m, 'f', f, 'cases', f0, 'tail', tail, kind, level, flush=True)
    assert nu == set(d['ecpp'])
    print('FULL MASK AUDIT', 128, 'outside projection', extras, 'root abundance min ppm', min(extra_floors), flush=True)
    print('VERIFIED', (P,E), 'old', len(old_masks), 'new', len(missing), 'pivot', Q, 'new split', fs_counts, counts, 'new forest min floor', min_floor, 'old floor', min(history.values()), 'ECPP', len(nu), 'SHA256', sha256(raw).hexdigest(), flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--packet', type=Path, default=H/'Pivot316Residual.json.gz')
    verify(ap.parse_args().packet)
