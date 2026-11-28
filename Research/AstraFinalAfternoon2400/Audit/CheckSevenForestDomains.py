"""Independent proof-domain reconstruction for two exact root-seven packs."""
import gzip
from functools import cache
from hashlib import sha256
import json
from math import gcd, lcm, prod
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent / 'Seven'
B = 10**2400
Q = 16148168401
R438 = 572749682520506652634407616247


@cache
def sig(x, e):
    # Independent finite sum, not the applicant's geometric quotient.
    acc = 0
    for _ in range(e + 1):
        acc = acc*x+1
    return acc


def odd(x):
    return x // (x & -x)


def exact_state(rows, banned):
    assert len({p for p, _ in rows}) == len(rows)
    if sum(h % 2 for _, h in rows) > 1:
        return
    if any(h % 2 and (h % 4, p % 4) != (1, 1) for p, h in rows):
        return
    x = prod(p**h for p, h in rows)
    s = prod(sig(p, h) for p, h in rows)
    y = odd(s)
    m = lcm(x, y)
    if m <= B and s <= 2*x and gcd(m, prod(banned)) == 1 and gcd(m//x,x) == 1:
        return x,y,m


def split(rows, banned, q):
    x,y,_ = exact_state(rows,banned)
    assert x % q and y % q == 0 and q not in banned
    n = y
    while n % q == 0:
        n //= q
    paid = lcm(x,n)
    lo = 1
    while n*q**(lo-1) < y:
        lo += 1
    lo -= 1
    tail=lo
    while paid*q**tail <= B:
        tail += 1
    return {h: rows+[(q,h)] for h in range(lo,tail) if exact_state(rows+[(q,h)],banned)},tail


def scope(rows,bans):
    t = sig(Q,12)//13
    if rows[:-1] == [(7,438), (R438,10)]:
        assert bans == {19} and rows[-1][0] == 67
        return '438'
    if rows[:-1] == [(7,12), (Q,12), (t,2)]:
        assert bans == {19,5,11} and rows[-1][0] == 3453283
        assert sig(7,12) == Q and sig(Q,12) == 13*t and sig(t,2) % (3*3453283) == 0
        assert sig(3,2) == 13
        # Under 5 presence, use 5^1 regardless of Euler. Under 11 presence,
        # separate exponent of compelled 3: 2 or >=4. If 3^2 exactly, its
        # 13 inflow adds a unit to sigma(Q^12), forcing v_13(N)>=2.
        for hypothetical in ([(7,12),(3,2),(5,1)],
                             [(7,12),(3,4),(11,2),(13,1)],
                             [(7,12),(3,2),(11,2),(13,2)]):
            assert prod(sig(p,h) for p,h in hypothetical) > 2*prod(p**h for p,h in hypothetical)
        return '12L'
    if rows[:-1] == [(7,48), (6106505825833677713,4)]:
        assert bans == {19} and rows[-1][0] == 5913168485260377611579965807967983090512568398832018674784831
        live,tail = split(rows[:-1],bans,rows[-1][0]); assert set(live) == set(range(2,19,2)) and tail == 37
        return '48f4'
    assert rows[:-1] == [(7,12),(Q,42)] and rows[-1][0] == 173 and bans == {19}
    return '12R'


def replay_basics(name, expected_hash, expected):
    raw = (HERE / name).read_bytes()
    assert sha256(raw).hexdigest() == expected_hash
    packet = json.loads(gzip.decompress(raw))
    splits = []
    leaves = 0
    labels = set()
    seen = set()
    def examine(rows,bans,node):
        nonlocal leaves
        _,_,m = exact_state(rows,bans)
        labels.update(p for p,h in rows)
        if node['type'] == 'split':
            pivot = node['q']
            branches,tail = split(rows,bans,pivot)
            assert set(branches) == set(map(int,node['cases']))
            labels.add(pivot)
            splits.append((len(branches),tail))
            for h,child in branches.items():
                examine(child,bans,node['cases'][str(h)])
            return
        assert node['type'] == 'forest' and 1 <= node['head'] <= 1024
        roots, nodes = set(node['roots']), dict(node['owners'])
        assert len(roots)==len(node['roots']) and len(nodes)==len(node['owners'])
        vertices = roots | nodes.keys()
        assert not roots & nodes.keys() and not vertices & (bans|dict(rows).keys())
        assert all(m % p == 0 for p in roots) and all(m % p for p in nodes)
        for p in nodes:
            visited = set()
            while p not in roots:
                assert p in nodes and p not in visited
                visited.add(p)
                p = nodes[p]
        labels.update(vertices)
        leaves += 1
    for record in packet['records']:
        assert not record['unresolved']
        rows, bans = [tuple(pair) for pair in record['P']], set(record['bad'])
        item = scope(rows,bans), rows[-1][1]
        assert item not in seen
        seen.add(item)
        for i in range(1,len(rows)):
            children,_ = split(rows[:i],bans,rows[i][0])
            assert rows[i][1] in children
        examine(rows,bans,record['tree'])
    assert seen == expected
    assert {str(p) for p in labels if p>=2**64} == packet['ecpp'].keys()
    print('PASS independent domains, pinned bytes, forest support/ownership and exact rows:',
          name, len(seen), 'conditions;', leaves, 'forest leaves; splits (live,tail)', splits,
          'ECPP labels', len(packet['ecpp']))


if __name__ == '__main__':
    assert __debug__
    replay_basics('Forest438a.json.gz', 'ed862b6cc0f6a3a13fd4b7740825d3bed0f41861eb88a88353aae1d12a3f5b6d',
                  {('438', h) for h in range(130,159,2) if h != 148})
    replay_basics('Forest438b.json.gz', '84283ffbe0884a019647faa7ddb0746a1623e50a200b5d625ddfbd1e1dc40777',
                  {('438', h) for h in (36,38,42,50,52,54,58,64,66,68,70,72,74,76,78,84,86,88,90,92,94,96,98,100,102,104,106,108,110,112,114,116,118,120,122,126,128)})
    replay_basics('Forest438c.json.gz', 'd7ac09f97d59087aa08e9ae5dff07ae158108552d79606b63e159af9a6b429f3',
                  {('438', h) for h in (12,16,22,28,30,34)})
    replay_basics('Forest48a.json.gz', '65361a2a06a7aabecfbe2e6d54bea1468554b5a10c61bc3fd40f9c9a9ec4c44e',
                  {('48f4', h) for h in (8,10,12,14,16,18)})
    replay_basics('Forest12b.json.gz', '1b235c54fd29601e6ce1945df11d1a6c114602ed84faf00d21909d784158b91e',
                  {('12R', h) for h in (64,66,68,70,72,74,76,84,86,88,90,92,94,98,100,102,104,108,110,112,114,116,118,122,128,132,134,140,142,144,146,152,154)})
    replay_basics('Forest12a.json.gz', '393ed361ee148eb28cd618271ba3adb7ff21833c4704818fbd3eda375bbfe675',
                  {('12L', h) for h in (10,16,22)} |
                  {('12R', h) for h in (160,162,164,168,170,174,178,186,188,194)})
