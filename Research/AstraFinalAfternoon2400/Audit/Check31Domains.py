"""Independent domain reconstruction for canonical root-31 sealed forests, not leaf pricing."""
import gzip
import hashlib
import json
from math import gcd, lcm, prod
from pathlib import Path
import subprocess
import sys

B = 10**2400
ROOT = 31
BANS = (19, 7, 11)
BASE = '495c59f55456a70994ce7848487e0c4e262c1984'


def vp(n, p):
    assert n > 0
    a = 0
    while n % p == 0:
        a += 1
        n //= p
    return a


def geometric(p, e):
    return sum(p**i for i in range(e+1))


def legal_exponents(row):
    fixed_odd = any(e % 2 for _, e in row)
    def legal(p, e):
        return e % 2 == 0 or (not fixed_odd and p % 4 == e % 4 == 1)
    return legal


def state(row, bans=BANS):
    assert len(dict(row)) == len(row)
    x = prod(p**a for p,a in row)
    total = prod(geometric(p,a) for p,a in row)
    s = total >> vp(total, 2)
    viable = (sum(a % 2 for _,a in row) <= 1 and all(a >= 1 and p not in bans
              and (a % 2 == 0 or p % 4 == a % 4 == 1) and vp(s,p) <= a for p,a in row)
              and not any(s % p == 0 for p in bans) and total <= 2*x and lcm(x,s) <= B)
    return x,s,viable


def split(row, p, bans=BANS):
    x, s, valid = state(row, bans)
    assert valid and p not in dict(row) and p not in bans and p > 2 and p % 2
    required = vp(s,p)
    assert required > 0
    l = lcm(x,s)
    live = {}
    f = required
    allowed = legal_exponents(row)
    # l|N before the split; q^f||N adds exactly f-required units.
    while l*p**(f-required) <= B:
        if allowed(p,f):
            new = (*row,(p,f))
            if state(new,bans)[-1]:
                live[f] = new
        f += 1
    assert l*p**(f-required) > B and (f == required or l*p**(f-required-1) <= B)
    return live, f


def verify_open(path):
    raw = path.read_bytes()
    data = json.loads(gzip.decompress(raw))
    frozen = json.loads(subprocess.check_output(['git','show', f'{BASE}:Research/FinalNight2400/OpenFrontier.json']))
    legal_e = frozen['RemainingByRoot']['31']
    e,q = data['e'],data['pivot']
    assert e in legal_e
    prefix = ((ROOT,e),)
    nsplit = nleaves = 0
    gaps=[]

    def visit(row,node):
        nonlocal nsplit,nleaves
        if node is None:
            gaps.append(row)
        elif node['type'] == 'forest':
            nleaves += 1
        else:
            assert node['type'] == 'split'
            nsplit += 1
            children, _ = split(row,node['q'])
            given = node['cases']
            assert given.keys() == {str(a) for a in children}
            for a,new in children.items():
                visit(new,given[str(a)])

    live,tail = split(prefix,q) if q is not None else ({e:prefix},None)
    assert data['cases'].keys() == {str(f) for f in live}
    for f,row in live.items():
        visit(row,data['cases'][str(f)])
    print('key', (ROOT,e), 'sha256', hashlib.sha256(raw).hexdigest())
    print('pivot', q, 'live', sorted(live), 'first strict size tail',tail)
    print('subdivisions', nsplit, 'forest leaves pending their arithmetic', nleaves,
          'open firsts', sorted({row[1][1] for row in gaps if len(row)>1}), 'total open leaves',len(gaps))


if __name__ == '__main__':
    assert __debug__ and len(sys.argv)>1
    for name in sys.argv[1:]:
        verify_open(Path(name))
