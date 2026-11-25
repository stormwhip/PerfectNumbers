"""Exact terminal dual for all external q^1 supplying s>=445 at root (5,520)."""
from functools import cache
import gzip
from hashlib import sha256
import json
from math import gcd, prod
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
R = HERE.parents[1]
for path in (R/'Session20261122'/'Python', R/'RootFiveNext'):
    sys.path.insert(0, str(path))
from PrimeCheck import prime64
from RoadblockDual import log_bounds, SCALE, odd_primes
from TerminalCertificate import DYADIC, sigma, verify as verify_archive

E, S0 = 520, 445
BAD = (3, 7, 11, 13, 19, 31)
P5 = 5**E
A = sigma(5, E)
Q = 2*5**S0-1
FILES = R/'Session20261122'/'Certificates'
CAP = 32
L0 = 100001
TRACE = R/'NightUniform'/'ThreeAvoid.json'


def req(b, message):
    if not b:
        raise ValueError(message)


def permitted(p, f):
    return all(pow(p, f+1, z*(p-1)) != 1 for z in BAD)


def intlog(n, p):
    e = 0
    while n >= p:
        n //= p
        e += 1
    return e


@cache
def primeprod(n):
    return prod(odd_primes(n))


def model(logs=log_bounds, verify_all=True, lower_q=Q):
    Q = lower_q
    if verify_all:
        req(gcd(A, primeprod(L0-1)*2*5) == 1, 'root rough threshold')
    auth = json.loads(TRACE.read_bytes()); ext, = auth['cases']
    raw = []
    for label in ('Original','Replacement'):
        data = (FILES/f'Terminal{label}.json.gz').read_bytes()
        req(sha256(data).hexdigest() == auth['archive_sha256'][label], 'wrong frozen archive')
        arc = json.loads(gzip.decompress(data))
        if verify_all:
            req(verify_archive(arc), 'invalid frozen terminal archive')
        raw.append(arc)
    arcprime = {q for arc in raw for p, f, q, c in arc['edges']}
    base = {p: CAP for p in odd_primes(5000) if p not in BAD+(5,)}

    @cache
    def prime(n):
        if n in arcprime or n in base_primes or prime64(n):
            return True
        F, seen = 1, set()
        for p, k, a in auth['proof'].get(str(n), []):
            if not (type(p) == type(k) == type(a) == int and 1 < p < n and p not in seen
                    and 0 < k <= n.bit_length() and 1 < a < n and prime(p)):
                return False
            seen.add(p)
            F *= p**k
            if (n-1)%F or pow(a,n-1,n) != 1 or gcd(pow(a,(n-1)//p,n)-1,n) != 1:
                return False
        return F*F > n

    base_primes = set(odd_primes(5000)) | {2}
    for p, f in ext['promoted']:
        if p in BAD+(5,):
            continue
        req(1 <= f <= 400 and (not verify_all or prime(p)), 'unproved promoted base')
        base[p] = max(f, base.get(p, 0))

    edges = {}
    for source, check_new in [(arc['edges'], False) for arc in raw]+[(ext['new'], True)]:
        for p, f, q, c in source:
            if p in BAD+(5,) or q in BAD+(5,) or f%2 or not permitted(p,f):
                continue
            if verify_all and check_new:
                req(p != q and 1 <= f <= 400 and 1 <= c <= 255 and prime(p) and prime(q)
                    and sigma(p,f)%q**c == 0, 'unproved new factor edge')
            base[p] = max(f, base.get(p,0))
            base.setdefault(q,0)
            edges[p,f,q] = max(c,edges.get((p,f,q),0))

    covered = prod(base)
    req(max(base) < Q and gcd(A, covered) == 1, 'root/Euler intersects terminal explicit support')
    costs, abundance, groups, exact = [], [], {}, {}
    for p in sorted(base):
        G = groups.setdefault(p, [])
        ell = logs(p)[0]
        for f in range(2,base[p]+1,2):
            if permitted(p,f):
                j = len(costs); G.append((j,f,True)); exact[p,f] = j
                costs.append(f*ell); abundance.append(logs(sigma(p,f),p**f)[1])
        f = 2*(1+base[p]//2)
        while not permitted(p,f):
            f += 2
        G.append((len(costs),f,False)); costs.append(f*ell); abundance.append(logs(p,p-1)[1])

    used = {}; selected = set()
    for p,f,n,L in ext['blocks']:
        if (p,f) not in exact:
            continue
        req((p,f) not in selected and 5001 <= L <= 5000001 and 1 < n < Q
            and n%2 == 1 and sigma(p,f)%n == 0, 'invalid anonymous cofactor')
        selected.add((p,f))
        suppress = A*covered*prod(v for z,v in used.items() if z != p)
        while (g:=gcd(n,suppress))>1:
            n //= g
        if n == 1:
            continue
        if verify_all:
            req(gcd(n, primeprod(L-1)) == 1, 'false cofactor rough threshold')
        used[p] = used.get(p,1)*n
        j = exact[p,f]; costs[j] += logs(n)[0]
        abundance[j] += intlog(n,L)*logs(L,L-1)[1]

    # All remaining primes outside the explicit bases, root and charged blocks
    # are >=5001 and ordinary. Bound their log cost per unit log abundance.
    tail = len(costs)
    L = 5001
    costs.append(2*logs(L)[0]*SCALE//logs(L,L-1)[1]); abundance.append(SCALE)
    # Fractional/negative RHS offsets all use upper bounds on the free abundance.
    free = logs(5,4)[1] + intlog(A,L0)*logs(L0,L0-1)[1] + logs(Q,Q-1)[1]
    rows = [(list(enumerate(-h for h in abundance)), free-logs(2)[0])]
    rows += [([(j,SCALE) for j,f,k in group],SCALE) for group in groups.values()]
    for (p,f,q), c in sorted(edges.items()):
        i = exact[p,f]
        rows.append(([(i,SCALE)]+[(j,-SCALE) for j,f,k in groups[q] if not k or f>=c],0))
    return costs, rows, groups, tail, len(selected)


def weighted(m, weights):
    costs, rows, groups, tail, _ = m
    reduced = [c*DYADIC for c in costs]
    total = 0; previous = -1
    for i,w in weights:
        req(type(i) is int and type(w) is int and previous < i < len(rows) and w>0, 'bad dual weight')
        previous = i
        terms,b = rows[i]
        total -= w*b
        for j,a in terms:
            reduced[j] += w*a
    req(reduced[tail]>=0, 'negative unbounded-tail coefficient')
    return total + sum(min(0,*(reduced[j] for j,_,_ in g)) for g in groups.values())


def verify(verbose=False, *, logs=log_bounds, verify_all=True, lower_q=Q):
    packet = json.loads((HERE/'Late520Dual.json').read_bytes())
    m = model(logs, verify_all=verify_all, lower_q=lower_q)
    v = weighted(m, packet['weights'])
    bound = v + DYADIC*logs(P5*A*lower_q)[0]
    req(bound > 2400*DYADIC*logs(10)[1], 'insufficient terminal lower bound')
    if verbose:
        print('late Euler dual: floor log10(N)', bound//(DYADIC*logs(10)[1]),
              'options/rows/blocks',len(m[0]),len(m[1]),m[-1])
    return bound


if __name__ == '__main__':
    verify(verbose=True)
