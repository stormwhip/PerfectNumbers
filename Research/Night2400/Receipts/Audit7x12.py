"""Independent task-20 audit, using only the packet and the standard library."""
import gzip
import json
from collections import Counter
from fractions import Fraction
from math import gcd, isqrt, prod
from pathlib import Path

B = 10**2400
Q = 16148168401
PACKET = Path('Research/Night2400/A/Fibers12.json.gz')


def sigma(p, e):
    return (p**(e+1)-1)//(p-1)


def v(n, q):
    h = 0
    while not n % q:
        n //= q
        h += 1
    return h


def state(parts, S=None):
    X = prod(p**e for p, e in parts)
    if S is None:
        S = prod(sigma(p, e) for p, e in parts)
    D = S >> v(S, 2)
    assert not D % 2 == 0
    fixed_excess = False
    for p, e in parts:
        a = v(D, p)
        fixed_excess |= a > e
        D //= p**a
    reasons = []
    if fixed_excess:
        reasons.append('fixed_incoming')
    if X * D > B:
        reasons.append('forced_size')
    if S > 2 * X:
        reasons.append('abundancy')
    return X, D, S, reasons


def domain(parts, q):
    X, D, S, reasons = state(parts)
    assert not reasons and q != 19 and q not in dict(parts) and D % q == 0
    h = v(D, q)
    base = X * (D // q**h)
    size = base * q**h
    assert size == X*D
    e = h
    counts = Counter()
    live = set()
    direct = {}
    while size <= B:
        if e % 2 and (q % 4 != 1 or e % 4 != 1 or any(f % 2 for p, f in parts)):
            counts['parity'] += 1
        else:
            s = sigma(q, e)
            if s % 19 == 0:
                counts['forbidden_19'] += 1
            else:
                reasons = state(parts + ((q, e),), S*s)[3]
                if reasons:
                    direct[e] = reasons
                else:
                    live.add(e)
        size *= q
        e += 1
    assert size == base*q**e and size > B
    if e > h:
        assert size//q <= B
    return live, direct, counts, (h, e-1, e)


def int_children(obj):
    assert all(k == str(int(k)) for k in obj)
    return {int(k): a for k, a in obj.items()}


def unique_keys(pairs):
    result = dict(pairs)
    assert len(result) == len(pairs), 'duplicate JSON key'
    return result


def check_domains():
    with gzip.open(PACKET, 'rt', encoding='utf-8') as fp:
        packet = json.load(fp, object_pairs_hook=unique_keys)
    root = ((7, 12),)
    assert packet['pair'] == [7, 12] and packet['pivot'] == sigma(7, 12) == Q
    assert all(Q % p for p in range(2, isqrt(Q)+1))
    live, dead, skip, bounds = domain(root, Q)
    assert bounds == (1, 234, 235) and len(live) == 83 and len(dead) == 84
    assert 7**12*Q**234 <= B < 7**12*Q**235
    claims = int_children(packet['cases'])
    gaps = sorted(live - claims.keys())
    assert claims.keys() <= live and len(claims) == 77 and gaps == [1,2,4,12,28,42]
    print('FIRST', 'bounds', bounds, 'skip', dict(skip), 'direct', len(dead), 'live', sorted(live), 'uncovered', gaps, flush=True)
    totals = Counter()
    price_sites = []

    def visit(prefix, node, tally):
        typ = node['type']
        tally[typ] += 1
        if typ == 'price':
            assert prefix in (root + ((Q, 100),), root + ((Q, 102),))
            assert set(node) == {'type'}
            price_sites.append(prefix[1][1])
        elif typ == 'split':
            q = node['q']
            kids = int_children(node['cases'])
            expected, removed, ruled_out, limits = domain(prefix, q)
            assert expected == kids.keys(), (prefix, q, sorted(expected - kids.keys()), sorted(kids.keys() - expected))
            tally['direct'] += len(removed)
            tally.update(ruled_out)
            print('SPLIT', prefix, q, 'bounds', limits, 'kept', sorted(expected), 'direct', sorted(removed), 'skip', dict(ruled_out), flush=True)
            for e in sorted(kids):
                visit(prefix + ((q, e),), kids[e], tally)
        else:
            assert typ == 'forest'

    for e, node in sorted(claims.items()):
        tally = Counter()
        visit(root + ((Q, e),), node, tally)
        totals.update(tally)
        if node['type'] != 'forest':
            print('FIBER', e, dict(tally), flush=True)
    assert sorted(price_sites) == [100,102]
    print('NESTED TOTAL', dict(totals), 'FIRST+NESTED DIRECT', len(dead)+totals['direct'], flush=True)


def fact(n):
    out = []
    p = 2
    while p*p <= n:
        if n % p == 0:
            e = v(n, p)
            n //= p**e
            out.append((p, e))
        p += 1
    if n > 1:
        out.append((n,1))
    return out


def lift(a, k, depth):
    # Newton doubling in Z/Q^depth, rather than linear-digit lifting.
    j = 1
    while j < depth:
        j = min(2*j, depth)
        m = Q**j
        a = (a - (pow(a,k,m)-1)*pow(k*pow(a,k-1,m),-1,m)) % m
    assert pow(a,k,Q**depth) == 1
    return a


def check_price(f):
    assert f in (100,102)
    # Exactly f incoming Q's, one supplied by sigma(7^12); sigma(Q^f) supplies none.
    # For each prime outside {7,Q,19}, lower-bound its size by Q^(2j) / loss.
    X = 7**12*Q**f
    D = sigma(Q, f)
    c = f-1
    assert gcd(D, 2*7*Q*19) == 1 and sigma(7,12) == Q
    max_h = 0
    cap = B//X
    while 3**(max_h+1) <= cap:
        max_h += 1
    assert max_h+1 < Q
    factors = fact(Q-1)
    assert prod(p**e for p,e in factors) == Q-1
    g = 2
    while any(pow(g,(Q-1)//p,Q)==1 for p,e in factors):
        g += 1
    assert pow(g,Q-1,Q) == 1
    # Find the allowed order divisors directly within the size-derived exponent range.
    P = [Q**j for j in range(c+2)]
    loss_by_supplier = {}
    orders = []
    for k in range(2, max_h+2):
        if (Q-1)%k or not k%4:
            continue
        e = 5 if k==2 else k-1
        base_power = 3**e
        if base_power > cap or base_power >= P[c]**2:
            continue
        orders.append(k)
        a = pow(g, (Q-1)//k, Q)
        a = lift(a, k, c+1)
        pk = P[c+1]
        for i in range(1,k):
            if gcd(i,k) != 1:
                continue
            u = pow(a,i,pk)
            for j in range(1,c+1):
                m = P[j]
                m2 = m*m
                if base_power >= m2:
                    continue
                r = u % m
                # r^e < m^2 and e>=2 imply r < m. If the least residue is even,
                # the least odd one is >=m and therefore never qualifies.
                if r <= 2 or r in (7,19,Q) or not r%2 or u % P[j+1] == r:
                    continue
                lower_bit = (r.bit_length()-1)*e
                if lower_bit >= min(m2.bit_length(),cap.bit_length()):
                    continue
                cost = r**e
                if cost > cap or cost >= m2:
                    continue
                if pow(2,r-1,r)!=1:
                    continue
                loss = Fraction(m2,cost)
                loss_by_supplier[r] = max(loss, loss_by_supplier.get(r,1))
    U = prod(loss_by_supplier.values(),start=Fraction(1))
    L_num = X*P[c]**2*U.denominator
    L_den = U.numerator
    assert L_num > B*L_den
    incoming = []
    internal = []
    empty = 0
    for s,m in enumerate(P[:c+1]):
        low = 2*m-1
        if L_num*low > B*L_den*m*m:
            incoming.append(s)
            continue
        assert X*D*low > B
        first = (-D) % (2*m)
        assert first % 2 == 1
        last = D//low
        if last < first:
            empty += 1
        else:
            assert (last-first)//(2*m) < 128
            assert all(D%r for r in range(first,last+1,2*m))
        internal.append(s)
    assert len(orders) == {100:102,102:101}[f] and len(loss_by_supplier) == 1
    assert (len(incoming),len(internal),empty) == {100:(64,36,36),102:(70,32,32)}[f]
    print('PRICE', f, 'max_h', max_h, 'orders', len(orders), 'suppliers', sorted(loss_by_supplier), 'incoming', len(incoming), 'internal', len(internal), 'empty', empty, flush=True)


if __name__ == '__main__':
    import sys
    assert __debug__
    args = sys.argv[1:]
    if args == ['domains']:
        check_domains()
    else:
        assert args in (['100'], ['102'])
        check_price(int(args[0]))
