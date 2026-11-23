"""Replay the root-valuation certificates using Python 3.10+ standard library."""
from bisect import bisect_right
from fractions import Fraction
from functools import lru_cache
from math import gcd, isqrt, lcm, prod
import csv
import sys

B = 10**2400
ORDER = (19, 7, 11, 31, 13, 3, 5, 17)
LIMIT = 30000


def primes(bound):
    flags = bytearray([1]) * (bound + 1)
    flags[:2] = b'\x00\x00'
    for r in range(2, isqrt(bound) + 1):
        if flags[r]:
            flags[r*r::r] = bytes((bound-r*r)//r+1)
    return [r for r in range(2, bound+1) if flags[r]]


PRIMES = primes(LIMIT)


def ilog(x, b):
    lo, hi = 0, 1
    while b**hi <= x:
        hi *= 2
    while hi-lo > 1:
        mid = (hi+lo)//2
        if b**mid <= x:
            lo = mid
        else:
            hi = mid
    return lo


def tasks(p):
    cap = ilog(B, p)
    data = [(1, True)] if p % 4 == 1 else []
    if p == 3:
        data.extend([(2, True), (4, True), (8, False), (14, False), (24, False)])
        first = 7
    elif p == 7:
        data.extend([(2, True), (8, False)])
        first = 5
    else:
        first = 3
    data.extend((m-1, False) for m in PRIMES if first <= m <= cap+1)
    return data


def sigma(p, e):
    return (p**(e+1)-1)//(p-1)


def odd(n):
    return n//(n & -n)


def cube_root(n):
    lo, hi = 0, 1 << ((n.bit_length()+2)//3)
    while hi-lo > 1:
        mid = (hi+lo)//2
        if mid**3 <= n:
            lo = mid
        else:
            hi = mid
    return lo


def forbids(p):
    return ORDER[:ORDER.index(p)]


@lru_cache(None)
def incoming_costs(p):
    # Each additional valuation unit at r costs at least a marginal power.
    units = []
    for r in PRIMES:
        if r in forbids(p) or r % p != 1:
            continue
        x = r
        while x <= LIMIT:
            units.append(x)
            x = x**p
    total = 1
    costs = [1]
    for x in sorted(units):
        total *= x**(p-1)
        costs.append(total)
        if total > B:
            return costs
    raise ValueError("Increase prime sieve cutoff")


def exterior_count(p, m, a, qmin):
    # A-primes: their distinct sorted values are >= 1+2mi.
    t = ilog(a, 2*m+1)
    upper = Fraction(p, p-1) * Fraction(qmin, qmin-1)
    for i in range(1, t+1):
        upper *= Fraction(2*m*i+1, 2*m*i)
    n = 0
    size = Fraction(1)
    for r in PRIMES:
        if upper >= 2:
            return n, size
        if r == 2 or r == p or r in forbids(p):
            continue
        upper *= Fraction(r, r-1)
        size *= Fraction(r*r, 3 if p == 3 else 1)
        n += 1
    raise ValueError("Increase exterior prime cutoff")


SCALE = 10**8


@lru_cache(None)
def benefit(r):
    # Upper bound on SCALE * log(r/(r-1)).
    z = Fraction(1, 2*r-1)
    u = 2*SCALE*(z + z**3/3 + z**5/(5*(1-z*z)))
    return -(-u.numerator//u.denominator)


def log2_lower():
    z = Fraction(1, 3)
    return int(2*SCALE*sum(z**(2*i+1)/(2*i+1) for i in range(10)))


def exterior_bits(p, r):
    def bits(n, d):
        return (n//d).bit_length()-1
    # The increasing lower bound r**e/(e+1) covers the infinite exponent tail.
    candidates = [bits(r**32, 33)]
    for e in range(2, 32, 2):
        if any(pow(r, e+1, f*(r-1)) == 1 for f in forbids(p)):
            continue
        t, penalty = e+1, 1
        if r % p == 1:
            while t % p == 0:
                t //= p
                penalty *= p
        candidates.append(bits(r**e, penalty))
    return min(candidates)


@lru_cache(None)
def fractional_items(p):
    items = [(Fraction(exterior_bits(p, r), benefit(r)), benefit(r))
             for r in PRIMES if 2 < r <= 1000 and r != p and r not in forbids(p)]
    # For r>1000, residual charge >= r^2/3 and upper benefit <= SCALE/1000.
    tail = Fraction((1000**2//3).bit_length()-1, SCALE//1000)
    return sorted((price, h) for price, h in items if price < tail), tail


def residual_bits(p, demand):
    items, tail = fractional_items(p)
    cost = Fraction(0)
    for price, h in items:
        take = min(max(0, demand), h)
        cost += price*take
        demand -= take
        if demand <= 0:
            break
    return int(cost + tail*max(demand, 0))


def valuation(p, d, a):
    m = d+1
    if p not in (3, 5) or m <= p or m not in PRIME_SET:
        return "OPEN", ()
    k = bisect_right(incoming_costs(p), B//p**d)-1
    j = ilog(ilog(B, 3)+1, p)
    s = d-k-j
    if s <= 0:
        return "OPEN", ()
    y = p**s
    qmin = 2*y-1
    if qmin <= a and qmin*(y+1) <= p**m-1:
        return "OPEN", ()
    # Search a bounded prefix for possible shared valuation credit.
    # Composites passing the test only weaken the result.
    step = 2*m*p
    for i in range(1, 129):
        r = 1+step*i
        if pow(p, m, r**(p-1)) == 1:
            break
    else:
        r = 1+129*step
    gift = ilog(a, r**(p-1))
    n, count_cost = exterior_count(p, m, a, qmin)
    demand = log2_lower()-benefit(p)-((SCALE+qmin-2)//(qmin-1))
    for i in range(1, ilog(a, 2*m+1)+1):
        demand -= (SCALE+2*m*i-1)//(2*m*i)
    bits = residual_bits(p, demand)
    cost = max(count_cost, Fraction(2**bits))
    numerator = p**(2*d)*a*cost.numerator
    denominator = p**gift*cost.denominator
    if numerator > B*denominator:
        return "VALUATION", (k, j, s, r, gift, n, bits, ilog(numerator//denominator, 10))
    return "OPEN", ()


PRIME_SET = set(PRIMES)


def regression():
    p, d, q = 3, 2476, 980893
    assert all(q % t for t in range(2, isqrt(q)+1))
    a = sigma(p, d)
    assert a % q == 0 and a % (q*q)
    bound = B//(p**d*a)
    exponents = [e for e in range(1, 2+ilog(bound, q)) if e % 2 == 0 or e % 4 == 1]
    assert exponents == [1, 2, 4, 5, 6]
    for e in exponents:
        b = odd(sigma(q, e))
        assert gcd(b, prod(forbids(p))) > 1 or lcm(p**d*a, q**e, a*b) > B
    # Small input checks include both parities of the Euler exponent.
    for p in (3, 5):
        for r in PRIMES[1:45]:
            if r == p:
                continue
            for e in range(1, 30):
                if e % 2 and (e % 4 != 1 or r % 4 != 1):
                    continue
                v = 0
                x = sigma(r, e)
                while x % p == 0:
                    x //= p
                    v += 1
                t = e+1 if r % p == 1 else 1
                if r % p == p-1 and e % 2:
                    t = (r+1)*(e+1)
                w = 0
                while t % p == 0:
                    t //= p
                    w += 1
                assert v == w
    # Without restrictions on p-1 the valuation identity fails.
    assert sigma(2, 2) % 7 == 0 and 2 % 7 not in (1, 6)
    assert valuation(3, 2, 13)[0] == "OPEN"
    assert tasks(3)[368] == (2476, False)


ACTUAL_HEADER = ("p", "actual_e", "result", "support")


def supplier(p, e, a, s, gift, shared_min, demand):
    first = next(r for r in PRIMES if r % p == 1 and r not in forbids(p))
    unit = min(first**(p-1), shared_min)
    while True:
        y = p**s
        qmin = 2*y-1
        cap = B//(p**e*a*qmin)
        if cap == 0:
            return "LIFT_SIZE", f"{s}/{gift}/{unit}"
        j = ilog(2+ilog(cap, qmin), p)
        k = gift+ilog(cap, unit)
        new_s = e-j-k
        if new_s <= s:
            break
        s = new_s
    def too_small(t, r):
        return ((p-1)*a*t*r < y*qmin and
                3*(p-1)*a*t+2*qmin*t*r < 2*qmin*y)
    first_exterior = next(r for r in PRIMES if r > 2 and r != p and r not in forbids(p))
    all_bits = residual_bits(p, demand)
    other_bits = residual_bits(p, demand-benefit(first_exterior))
    outside_impossible = 3*(cap >> other_bits) < 2*qmin
    inside_cap = cap >> all_bits
    # The gap f-v is zero, one, or at least two. At gap one, v is odd.
    t = inside_cap
    if t >= 2:
        root3 = min(t, cube_root(a))
        square_source = (p == 3 or t*t+t+1 < qmin or too_small(t, t))
        gap_one = square_source and too_small(root3, root3)
        gap_many = too_small(t, isqrt(t))
    else:
        gap_one = gap_many = True
    inside_impossible = t == 0 or (too_small(1, isqrt(a)) and gap_one and gap_many)
    if outside_impossible and inside_impossible:
        return "SUPPLIER", f"{s}/{gift}/{unit}/{all_bits}/{other_bits}"
    return "OPEN", ""


def exact_exponent(p, e):
    a = odd(sigma(p, e))
    if p**e*a > B:
        return "SIZE", ""
    if gcd(a, prod(forbids(p))) > 1:
        return "FORBIDDEN", ""
    k = bisect_right(incoming_costs(p), B//p**e)-1
    if e % 2:
        return ("EULER_SLOT", k) if e > k else ("OPEN", "")
    s = e-k-ilog(ilog(B, 3)+1, p)
    if s <= 0:
        return "OPEN", ""
    y = p**s
    qmin = 2*y-1
    if qmin <= a and qmin*(y+1) <= p**(e+1)-1:
        return "OPEN", ""
    residue = a
    gift = 0
    shared_min = 1001
    demand = log2_lower()-benefit(p)-((SCALE+qmin-2)//(qmin-1))
    for r in PRIMES:
        if r > 1000:
            break
        if residue % r:
            continue
        v = 0
        while residue % r == 0:
            residue //= r
            v += 1
        if r % p == 1:
            gift += ilog(v+1, p)
            shared_min = min(shared_min, r)
        demand -= benefit(r)
    gift += ilog(residue, 1001**(p-1))
    for i in range(ilog(residue, 1001)):
        denom = 1000 + 2*i
        demand -= (SCALE+denom-1)//denom
    bits = residual_bits(p, demand)
    if (p**(2*e)*a << bits) > B*p**gift:
        return "EXACT_VALUATION", f"{k}/{s}/{gift}/{bits}"
    m = e+1
    if m in PRIME_SET and m > p:
        sparse_demand = log2_lower()-benefit(p)-((SCALE+qmin-2)//(qmin-1))
        for i in range(1, ilog(a, 2*m+1)+1):
            sparse_demand -= (SCALE+2*m*i-1)//(2*m*i)
        demand = max(demand, sparse_demand)
        step = 2*m*p
        base = 1+step
        while base < 1+129*step and a % (base**(p-1)):
            base += step
        gift = min(gift, ilog(a, base**(p-1)))
        base = 1+step
        while base < 1+129*step and a % base:
            base += step
        shared_min = max(shared_min, base)
    return supplier(p, e, a, s, gift, shared_min, demand)


def covers(e, d, exact):
    return e == d if exact else (e+1) % (d+1) == 0


def tables():
    top, actuals = [], []
    for p in ORDER:
        options = tasks(p)
        possible = [e for e in range(1, ilog(B, p)+1)
                    if e % 2 == 0 or e % 4 == p % 4 == 1]
        for e in possible:
            assert any(covers(e, d, exact) for d, exact in options)
        direct = []
        for i, (d, exact) in enumerate(options):
            a = odd(sigma(p, d))
            info = ()
            if p**d*a > B:
                tag = "BASE_SIZE"
            elif gcd(a, prod(forbids(p))) > 1:
                tag = "BASE_FORBIDDEN"
            else:
                tag, info = valuation(p, d, a)
            direct.append([f"P{p}_I{i:05d}", p, d, "exact" if exact else "divisor",
                           tag, *info, *([""]*(8-len(info)))])
        if p in (3, 5):
            known = [(row[0], row[2], row[3]=="exact") for row in direct if row[4] != "OPEN"]
            unresolved = []
            for e in possible:
                support = next((key for key, d, exact in known if covers(e, d, exact)), "")
                tag, support = ("DIRECT_SHARD", support) if support else exact_exponent(p, e)
                if tag == "OPEN":
                    unresolved.append(e)
                actuals.append((p, e, tag, support))
            for row in direct:
                if row[4] == "OPEN" and not any(covers(e, row[2], row[3]=="exact") for e in unresolved):
                    row[4] = "ALL_EXPONENTS"
        top.extend(direct)
    return top, actuals


HEADER = ("shard", "p", "d", "mode", "result", "K", "J", "S", "R0", "G", "n", "bits", "floor_log10_bound")


def check_tables(paths):
    if not __debug__:
        raise RuntimeError("Run without -O.")
    regression()
    result, actual = tables()
    if len(result) != 3072:
        raise ValueError("Expected 3072 canonical shards")
    for path, header, data in zip(paths, (HEADER, ACTUAL_HEADER), (result, actual), strict=True):
        with open(path, newline="", encoding="utf-8") as f:
            if list(csv.reader(f)) != [list(header)] + [list(map(str, row)) for row in data]:
                raise ValueError(f"Certificate mismatch in {path}")
    return result, actual


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O.")
    if len(sys.argv) == 4 and sys.argv[1] == "--check":
        result, actual = check_tables(sys.argv[2:])
        print("--check", len(result), "shards and", len(actual), "actual exponents")
        sys.exit(0)
    regression()
    result, actual = tables()
    assert len(result) == 3072
    if len(sys.argv) == 4 and sys.argv[1] == "--write":
        for path, header, data in zip(sys.argv[2:], (HEADER, ACTUAL_HEADER), (result, actual)):
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, lineterminator="\n")
                writer.writerow(header)
                writer.writerows(data)
        print(sys.argv[1], len(result), "shards and", len(actual), "actual exponents")
    elif len(sys.argv) == 1:
        writer = csv.writer(sys.stdout, lineterminator="\n")
        writer.writerow(HEADER)
        writer.writerows(result)
    else:
        raise SystemExit("Usage: python Verify.py [--check|--write Results.csv Exponents.csv]")
