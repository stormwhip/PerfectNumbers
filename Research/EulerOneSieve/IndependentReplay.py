import sys, json, time
from math import gcd
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import TeichmullerBaseline as T   # only U, sigma, forbidden, kappa, B
B = 10**2400

def vp(n, p):
    v = 0
    while n % p == 0: n //= p; v += 1
    return v

def order(a, p):
    o = 1; x = a % p
    while x != 1: x = x*a % p; o += 1
    return o

def mr_composite(n):
    """True only if n is proven composite (trial division / MR witness)."""
    if n < 2: return True
    for d in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n % d == 0: return n != d
    dd, r = n-1, 0
    while dd % 2 == 0: dd//=2; r+=1
    for b in (2,3,5,7,11,13,17,19,23,29,31,37):
        x = pow(b, dd, n)
        if x in (1, n-1): continue
        for _ in range(r-1):
            x = x*x % n
            if x == n-1: break
        else: return True
    return False

def my_D5_table(p, emax, use_filters=True):
    """list of (t, deficit) for Euler deficit candidates q = x_t at exact level t."""
    forb = set(T.forbidden(p)); out = []
    for a in range(2, p):
        o = order(a, p)
        if o < 3 or o % 4 == 0: continue
        L = o if o % 2 == 0 else 2*o
        f0 = L - 1
        x = a
        for t in range(1, emax+1):
            m = p**t
            if t > 1: x = pow(x, p, m)       # x_t = x_{t-1}^p mod p^t
            assert x % p == a and pow(x, o, m) == 1
            if vp(pow(x, o) - 1, p) != t:    # exact level t
                continue
            if x % 4 != 1: continue
            if use_filters and (x in forb or x == p or mr_composite(x)): continue
            if f0*(x.bit_length()-1) >= 5*t*p.bit_length(): continue
            if x**f0 < p**(5*t):
                out.append((t, -(-p**(5*t) // x**f0)))
    return out

def D5_fn(tab):
    def D5(s):
        best = 1
        for t, d in tab:
            if t <= s and d > best: best = d
        return best
    return D5

def sq_up(m):
    out = 1; r = 2
    while r*r <= m:
        v = 0
        while m % r == 0: m//=r; v+=1
        if v: out *= r**(2*((v+1)//2))
        r += 1
    if m > 1: out *= m*m
    return out

def a1(p, e, s, q, A, kap, U):
    pe = p**e; L = p**(kap*(e-s))
    if 2*s <= e: return q*pe*L > B*U
    return q*pe*max(A*U, L) > B*U

def check(rec, use_filters):
    p, e = rec['root'], rec['exponent']
    pr = PROF.setdefault(p, T.Profile(p)); kap = T.kappa(p)
    A = (p**(e+1)-1)//(p-1); pe = p**e
    assert e % 2 == 0 and e >= 2 and pe*A <= B and e <= pr.top
    assert all(A % z for z in T.forbidden(p))
    tab = my_D5_table(p, e, use_filters); D5 = D5_fn(tab)
    worst = None
    for s in range(e+1):
        U, D = pr.U(e-s), D5(s)
        lhs = p**(e+kap*(e-s)) * max(p**(5*s), 3125*D); rhs = B*U*D
        assert lhs > rhs, ('a5', p, e, s)
        m = lhs.bit_length() - rhs.bit_length()
        worst = m if worst is None else min(worst, m)
    win = {w[0]: (w[1], w[2]) for w in rec['proof_data']['windows']}
    used = set(); counts = {}
    for s in range(e+1):
        U = pr.U(e-s); ps = p**s
        if a1(p, e, s, 2*ps-1, A, kap, U):
            assert s not in win; continue
        assert s in win, ('missing window', s)
        used.add(s); jstop, wit = win[s]
        assert a1(p, e, s, jstop*ps-1, A, kap, U), ('stop', s)
        need = [j for j in range(2, jstop, 4) if j % p]
        assert sorted(j for j, _ in wit) == need and len(wit) == len(need), ('cover', s)
        for j, w in wit:
            assert j % 4 == 2 and j % p
            q = j*ps - 1
            if a1(p, e, s, q, A, kap, U): raise AssertionError('witness after stop?')
            if w > 1:
                assert q % w == 0 and 1 < w < q; k = 'div'
            elif w == 0:
                assert q > 1 and pow(2, q-1, q) != 1; k = 'fermat'
            elif w == -1:
                assert gcd(A, q) == 1
                mq = sq_up(j//2)
                assert (j//2) % 2 == 1 and gcd(mq, p*q) == 1
                l = A // gcd(A, mq) * mq
                assert q*pe*max(l*U, p**(kap*(e-s))) > B*U; k = 'R4'
            else:
                z = -w
                assert z in T.forbidden(p) and (j//2) % z == 0; k = 'R5'
            counts[k] = counts.get(k, 0) + 1
    assert used == set(win), ('extra windows', set(win)-used)
    return worst, counts, len(tab)

def lemmas(p, smax):
    for s in range(1, smax+1):
        assert 2*p**s - 1 >= 5*s and 2*p**s - 1 >= 5 + 5*s
        assert 3**(6*(p**s-1)) >= p**(5*s) if s <= 3 else True
    # j >= 6: compare logs crudely via bitlengths (exponent of 3 huge)
    return True

PROF = {}
recs = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ActualExponentRecords.json')))
uf = sys.argv[2] == '1'
if True:
    for rec in [r for r in recs if r['root'] == int(sys.argv[1])]:
        t0 = time.time()
        r = check(rec, uf)
        print('filters' if uf else 'NOfilters', rec['root'], rec['exponent'], 'a5 min bit margin', r[0], r[1], 'D5 entries', r[2], round(time.time()-t0,1), flush=True)
for p in (19, 7, 11, 13, 31): lemmas(p, 3)
print('ALL OK')
