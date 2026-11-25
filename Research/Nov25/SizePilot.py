"""Pilot: exact size/primality cap with a single Euler discount. No heuristic can close a row."""
from functools import cache
from math import gcd, isqrt, prod
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
R = HERE.parent
sys.path.insert(0, str(R / 'EveningTree'))
import IndependentTree as I

# Acquaah--Konyagin: P^3 < 3N, for the largest prime of an actual OPN.
# For a known factor q this gives q^3 < 3N; do NOT multiply q^3/3 by an
# unrelated divisor, since the statement is a lower bound on the same N.
B = 10**2400


@cache
def coprime_parts(blocks):
    """Split overlapping divisors into pairwise coprime supports, without factoring.

    Input may contain independent contributions to the valuation of the same
    recipient. Return chunks whose product is exactly the input product.
    """
    cells = [n for n in blocks if n > 1]
    while True:
        for j, x in enumerate(cells):
            for k in range(j):
                y = cells[k]
                g = gcd(x, y)
                if g > 1:
                    if x == y:
                        new = [x * y]
                    elif g == x:
                        # Pull all prime factors already present in x out of y.
                        t = y
                        while (d := gcd(x, t)) > 1:
                            t //= d
                        new = [x * (y // t), t]
                    elif g == y:
                        t = x
                        while (d := gcd(y, t)) > 1:
                            t //= d
                        new = [y * (x // t), t]
                    else:
                        t = x
                        while (d := gcd(g, t)) > 1:
                            t //= d
                        u = y
                        while (d := gcd(g, u)) > 1:
                            u //= d
                        new = [(x // t) * (y // u), t, u]
                    cells = [a for i, a in enumerate(cells) if i not in (j, k)]
                    cells.extend(a for a in new if a > 1)
                    break
            else:
                continue
            break
        else:
            return tuple(sorted(cells))


@cache
def weak_square_multiplier(n, minimum, cap):
    """Lower bound for the multiplier to an even valuation at every prime."""
    if isqrt(n)**2 == n:
        return 1
    # If n*t is square, the least t is sf(n), an odd divisor of n.
    for d in range(minimum | 1, cap + 1, 2):
        if n % d == 0 and isqrt(n // d)**2 == n // d:
            return d
    return max(minimum, (cap + 1) | 1)


def residual_blocks(U, parts):
    # Collect v_r(U) copies from the individual exact source sums. U is
    # coprime to assigned primes, so r-adic cancellations have not occurred.
    left = U
    blocks = []
    for z, f in parts:
        g = gcd(left, I.sigma(z, f))
        if g > 1:
            blocks.append(g)
            left //= g
    if left != 1:
        raise ValueError('residual source block product mismatch')
    return coprime_parts(tuple(blocks))


class Tree(I.Proof):
    def __init__(self, p, e, fs, depth, nodes, cap, valuation):
        super().__init__(p, e, fs, False, valuation)
        self.depth = depth
        self.nodes = nodes
        self.cap = cap
        self.first = None

    def visit(self, parts, X, S, ban):
        self.stats['nodes'] += 1
        if self.stats['nodes'] > self.nodes:
            return False
        used = any(f % 2 for _, f in parts)
        U = S // gcd(S, 2*X)
        if gcd(U, X*2*prod(ban)) > 1 or X*U > B or S > 2*X:
            self.stats['standard'] += 1
            return True
        blocks = {}
        for z in self.pr:
            if U == 1:
                break
            if U % z:
                continue
            c = I.vp(U, z)
            U //= z**c
            bad = I.forbidden_indices(z, ban)
            m = I.least(z, c, bad, False)
            a = None if used else I.least(z, c, bad, True)
            blocks[z] = c, m, a, bad
        if any(q**3 >= 3*B for q in blocks) or any(q**3 >= 3*B for q, _ in parts):
            self.stats['prime-cap'] += 1
            return True
        base = X*U*prod(z**m for z, (_, m, _, _) in blocks.items())
        saves = {z: z**max(0, m-a) for z, (_, m, a, _) in blocks.items() if a is not None}
        maxsave = max((1, *saves.values()))
        if base > B*maxsave:
            self.stats['standard'] += 1
            return True
        if self.valuation and self.valuation_close(X, S, U, base, blocks, used):
            self.stats['valuation'] += 1
            return True
        if self.cap is not None:
            # SMALL includes all odd primes below 5000. All unpaid U support
            # is therefore >=5001. No claim that any rough chunk is prime.
            extras = [(C, weak_square_multiplier(C, 5001, self.cap))
                      for C in residual_blocks(U, parts)]
            all_square = prod(t for _, t in extras)
            # Only one coupon: if U contains Euler q, at most its own block
            # loses the square multiplier. A block 3 mod 4 cannot lose the
            # whole multiplier since any eligible q is 1 mod 4.
            roughsave = max((1, *(t if C % 4 == 1 else max(1, t // 5001)
                                  for C, t in extras))) if not used else 1
            # For 3 mod 4, rigorously cap the *loss of the claimed multiplier*,
            # not the unknown true kernel. Round conservatively by checking
            # each one-coupon placement directly instead of dividing integers.
            possible = [base*all_square <= B*maxsave]
            if not used:
                possible.extend(base*(all_square // t)*(5001 if C % 4 == 3 and t > 1 else 1) <= B
                                for C, t in extras)
            if not any(possible):
                self.stats['rough-parity'] += 1
                return True
        if len(parts) > self.depth or not blocks:
            if self.first is None:
                self.first = dict(depth=len(parts), pivots=[(len(str(z)), f) for z, f in parts],
                                  rough_digits=len(str(U)), base_room_digits=len(str(B*maxsave//base)))
            return False
        z = max(blocks, key=lambda r: (r**blocks[r][1], r))
        _, m, a, bad = blocks[z]
        other = base // z**m
        opt = [(m, 2, max((1, *(s for r, s in saves.items() if r != z))))]
        if a is not None:
            opt.append((a, 4, 1))
        for f, step, saving in opt:
            power = z**f
            while other*power <= B*saving:
                if I.permissible(f, bad) and not self.visit(parts+((z, f),), X*power, S*I.sigma(z, f), ban):
                    return False
                f += step
                power *= z**step
        return True


if __name__ == '__main__':
    raise SystemExit('Use the separate pilot driver or a checked certificate adapter.')
