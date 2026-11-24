"""Read-only independent certificate: unit-price thresholds and official shard delta.
Run with Python 3.10+. No imports from the candidate or baseline verifiers.
"""
import csv
import json
from collections import Counter
from math import gcd, lcm, prod
from pathlib import Path

R = Path(__file__).resolve().parents[1]
B, T = 10**2400, 100000
TARGETS = (1296, 1300, 1302, 1308, 1312, 1330)
BAN = (19, 7, 11, 31, 13)

def load(path):
    return json.loads((R/path).read_text(encoding='utf8'))

# Trial division sieve independent of certificate generator.
ps = [2]
for i in range(3, T+1, 2):
    for q in ps:
        if q*q>i:
            ps.append(i)
            break
        if i%q==0: break

def floorlog(n,b):
    j = 0
    while n >= b:
        n //= b
        j += 1
    return j

def units(e):
    A = (3**(e+1)-1)//2
    phi, small, G = {}, Counter(), 0
    residuals = []
    for h in range(1,e+2):
        if (e+1)%h: continue
        phi[h] = (3**h-1)//prod(v for d,v in phi.items() if h%d==0)
        if h == 1: continue
        u = phi[h]
        for r in ps:
            while u%r == 0:
                small[r] += 1
                u //= r
        assert all(gcd(u,other)==1 for other in residuals)
        residuals.append(u)
        # An unknown prime subsidizing a whole unit has r^2 | u.
        # Its order mod r is h (r>T>h); r=1 mod 3 and r odd.
        stride = lcm(2*h,3)
        r = 1 + ((T-1)//stride+1)*stride
        for _ in range(100000):
            if u%(r*r)==0: break
            r += stride
        G += floorlog(u,r*r)
    assert prod(residuals)*prod(r**f for r,f in small.items()) == A
    # Only non-suppliers get a parity premium; discard largest for emitter.
    extras = sorted(r for r,f in small.items() if r%3!=1 and f%2)
    premium = prod(extras[:-1])
    # A more elementary bound than a list of sorted marginal prices: for
    # each power-of-two barrier 2^i count units costing strictly less.
    # Then at least max(0,k-count_i) chosen units pay this bit of cost.
    cheap = [0]*16
    for r in ps:
        if r%3!=1 or r in BAN: continue
        exp, paid = 2,small[r]
        while True:
            if any((pow(r,exp+1,z*(r-1))-1)%(z*(r-1))==0 for z in BAN): break
            price = r**max(0,exp-paid)
            if price >= 2**len(cheap): break
            for b in range(1,len(cheap)+1): cheap[b-1] += price < 2**b
            paid = max(paid,exp)
            exp = 3*(exp+1)-1
    def cost(k):
        return 1 << sum(max(0,k-G-c) for c in cheap)
    return A,G,premium,cost

def verify(e):
    A,G,prem,cost = units(e)
    # Old direct and high-Euler bounds. For a contributing r, LTE forces
    # f>=3^j-1; each incremental unit costs (r^(3^(j-1)))^2.
    bases = []
    for r in ps:
        if r%3!=1 or r in BAN: continue
        while r<=T:
            bases.append(r)
            r = r**3
    ordinary = [1]
    for b in sorted(bases)[:e]: ordinary.append(ordinary[-1]*b*b)
    assert len(ordinary)==e+1
    pe = 3**e; P = 3*pe
    misses = []; gaps = []; high = []
    for s in range(e+1):
        Y = 3**s; Q = max(5,2*Y-1); k = e-s
        size = pe*ordinary[k]
        if size*max(3125,3**max(0,5*s-5))<=B: high.append(s)
        if size*Q>B: continue
        nonsupplier = s>0 and pe*8*Q**4>=27*B
        if nonsupplier and 2*size*Q**2>=3*B: continue
        gaps.append(s)
        if not nonsupplier or pe*A*Q*Q*Y*prem*cost(k)<B*max(P,Q)*(P//Y+4): misses.append(s)
    print(e,'free',G,'premium',prem,'gap', (min(gaps),max(gaps)) if gaps else None,
          'misses',misses,'high',high)
    return not (misses or high)

def shard_delta(exponents):
    supplier = load('SupplierBatch/BatchAudit2400.json'); indicator = load('IndicatorCapacity/Audit2400.json')
    teich = load('TeichmullerValuation/Audit2400.json'); gem = load('TeichmullerValuation/GeminiBatchAudit2400.json')
    ids = {row['id'] for row in gem['additions']}
    official = [row for row in teich['open_manifest'] if row['id'] not in ids]
    assert len(official)==gem['open']==1045
    prior = {(row['root'],row['exponent']) for a in (supplier,indicator) for row in a['exact_exponents']}
    prior.update(map(tuple,gem['verified_exponents']))
    prior.update((row['root'],step['exponent']) for row in teich['additions'] for step in row['proof'])
    with (R/'FermatRootValuation/Exponents.csv').open() as f:
        pending = {int(row['actual_e']) for row in csv.DictReader(f) if row['p']=='3' and row['result']=='OPEN' and (3,int(row['actual_e'])) not in prior}
    delta=[]
    for row in official:
        if row['root']!=3: continue
        d = row['exponent']; es = {e for e in pending if (e==d if row['exact'] else (e+1)%(d+1)==0)}
        if es and es<=exponents: delta.append((row['id'],d,sorted(es)))
    print('new official shards',delta,'remaining',len(official)-len(delta))
    return delta

if __name__=='__main__':
    if not __debug__: raise SystemExit('Run without -O')
    proved={e for e in TARGETS if verify(e)}
    if proved!=set(TARGETS): raise SystemExit('Not all target exponents verified')
    print('independently closed', sorted(proved))
    delta = shard_delta(proved)
    if delta != [('P3_I00212',1296,[1296]), ('P3_I00213',1300,[1300]),
                 ('P3_I00214',1302,[1302])]: raise SystemExit('Unexpected shard delta')
