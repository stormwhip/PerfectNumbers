"""Independent exact integer lower bound when the forced forest root is ordinary."""
from functools import cache
from fractions import Fraction
from math import gcd, prod

BAD = (3, 7, 11, 13, 19, 31)
B = 10**2400


def lower(row):
    # Label primality and forest topology are separately verified before calling.
    q, = row['roots']
    parent = dict(row['owners'])
    kids = {p: [] for p in set(parent) | {q}}
    for v, u in parent.items():
        kids[u].append(v)
    support = 5*q*prod(parent)

    def v_p(n, p):
        k = 0
        while n % p == 0:
            k += 1
            n //= p
        return k

    def strip(n):
        while (g := gcd(n, support)) > 1:
            n //= g
        return n

    @cache
    def visit(p, c, odd):
        if odd and (p%4 != 1 or any((p+1)%l == 0 for l in BAD)):
            return None
        f = c + ((1-c)%4 if odd else (-c)%2)
        step = 4 if odd else 2
        full = flex = B+1
        for _ in range(row['head']):
            if p**f >= max(full, flex):
                break
            while any(pow(p, f+1, l*(p-1)) == 1 for l in BAD):
                f += step
            s = (p**(f+1)-1)//(p-1)//(2 if odd else 1)
            cost = p**f * strip(s)
            refund = Fraction(1)
            for r in kids[p]:
                h = v_p(s, r)
                if h:
                    a, b = visit(r, h, False)
                    special = visit(r, h, True)
                    if special is not None:
                        b = min(b, special[0])
                    cost *= a
                    refund = max(refund, Fraction(a, b))
            full = min(full, cost)
            flex = min(flex, cost//refund)
            f += step
        # Every legal omitted exponent is >= f, so retain a pure-power tail.
        return min(full, p**f), min(flex, p**f)

    return 5**row['e'] * visit(q, 1, False)[1]
