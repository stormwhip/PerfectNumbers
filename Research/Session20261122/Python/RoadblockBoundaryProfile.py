"""Find a certified roadblock boundary for a fixed rational multiplier."""

from bisect import bisect_right
from collections import defaultdict
from fractions import Fraction
from heapq import heappop, heappush

from RoadblockDual import log_bounds, odd_primes


class FactorTable:
    def __init__(self, limit):
        self.limit = limit
        self.primes = tuple(odd_primes(limit))
        self.even_factors = {q: [] for q in self.primes}
        self.special_factors = {q: [] for q in self.primes}
        self.logs = {q: (log_bounds(q)[0], log_bounds(q, q - 1)[1])
                     for q in (*self.primes, limit + 1)}

        def mark(table, r, residue):
            for p in range(residue, limit + 1, r):
                factors = table.get(p)
                if factors is not None:
                    factors.append(r)

        # An odd prime r divides (q + 1)/2 exactly when q = -1 mod r.
        for r in self.primes:
            mark(self.special_factors, r, r - 1)
            if r == 3:
                mark(self.even_factors, r, 1)
            elif r % 3 == 1:
                exp = (r - 1) // 3
                for a in range(2, r):
                    root = pow(a, exp, r)
                    if root != 1:
                        mark(self.even_factors, r, root)
                        mark(self.even_factors, r, root * root % r)
                        break


class BoundaryProfile:
    def __init__(self, table, gap, mu, forbidden=(), expanded=(), special_used=False):
        self.limit = table.limit
        mu = Fraction(mu)
        num, den = mu.numerator, mu.denominator
        tail_log, tail_ab = table.logs[self.limit + 1]
        if gap < 0 or mu < 0 or num * tail_ab > 2 * den * tail_log:
            raise ValueError("invalid abundance gap or tail multiplier")
        tail_gain = 0 if special_used else max(0, num * tail_ab - den * tail_log)
        forbidden, expanded = set(forbidden), set(expanded)
        remote_forbidden = [r for r in forbidden if r > self.limit]
        even_events = defaultdict(int)
        special_events = defaultdict(list)

        def first_forbidden(factors):
            if any(r in forbidden for r in factors):
                return 3
            return next((r + 1 for r in factors if r not in expanded), self.limit + 1)

        for q in table.primes:
            if q in forbidden or q in expanded:
                continue
            loglo, abund = table.logs[q]
            cost, target = den * loglo, num * abund
            if cost >= target:
                break
            switch = first_forbidden(table.even_factors[q])
            if any((q*q + q + 1) % r == 0 for r in remote_forbidden):
                switch = 3
            remove = q + 1
            switch = min(switch, remove)
            for lo, hi, e in ((3, switch, 2), (switch, remove, 4)):
                if lo >= hi:
                    continue
                even = min(0, e * cost - target)
                even_events[lo] += even
                even_events[hi] -= even
                if not special_used and q % 4 == 1:
                    hi = min(hi, first_forbidden(table.special_factors[q]))
                    gain = even - cost + target
                    if lo < hi and gain > 0:
                        special_events[lo].append((-gain, hi))
                        special_events.setdefault(hi, [])  # Wake the sweep on expiration.

        cuts, bounds = [], []
        active = []
        value = num * gap
        for b in sorted({3, *even_events, *special_events}):
            if b > self.limit:
                break
            value += even_events[b]
            for option in special_events[b]:
                heappush(active, option)
            while active and active[0][1] <= b:
                heappop(active)
            gamma = max(tail_gain, -active[0][0] if active else 0)
            cuts.append(b)
            bounds.append((value - gamma) // den)
        self.cuts, self.bounds = cuts, bounds

    def at(self, boundary):
        if not 3 <= boundary <= self.limit:
            raise ValueError("boundary outside the table")
        return self.bounds[bisect_right(self.cuts, boundary) - 1]

    def first_above(self, budget):
        """Smallest integer boundary with a certified bound above the budget."""
        i = bisect_right(self.bounds, budget)
        return self.cuts[i] if i < len(self.cuts) else None
