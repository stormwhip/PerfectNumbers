"""Independent fixed-point oracle for the two-multiplier roadblock bound."""

from bisect import bisect_left
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import accumulate

SCALE = 1 << 80
TERMS = 32
MULTIPLIER_SCALE = 1 << 32


def ceil_div(n, d):
    return -(-n // d)


def unit_log_bounds(n, d):
    """Bounds for SCALE * ln(n/d), with 1 <= n/d <= 2."""
    z_lo = SCALE * (n - d) // (n + d)
    z_hi = ceil_div(SCALE * (n - d), n + d)
    power_lo, power_hi = z_lo, z_hi
    lo = hi = 0
    for k in range(TERMS):
        odd = 2 * k + 1
        lo += power_lo // odd
        hi += ceil_div(power_hi, odd)
        power_lo = power_lo * z_lo**2 // SCALE**2
        power_hi = ceil_div(power_hi * z_hi**2, SCALE**2)
    # The omitted series, including its factor two, is bounded by 3*z**65.
    return 2 * lo, 2 * hi + 3 * power_hi


LOG2 = unit_log_bounds(2, 1)


@lru_cache(maxsize=None)
def log_bounds(n, d=1):
    """Bounds for SCALE * ln(n/d), with n >= d > 0."""
    if n < d or d <= 0:
        raise ValueError("expected n >= d > 0")
    shift = n.bit_length() - d.bit_length()
    if n < d << shift:
        shift -= 1
    lo, hi = unit_log_bounds(n, d << shift)
    return lo + shift * LOG2[0], hi + shift * LOG2[1]


def odd_primes(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    for p in range(2, limit + 1):
        if sieve[p]:
            if p * p <= limit:
                sieve[p * p :: p] = bytes((limit - p * p) // p + 1)
            if p != 2:
                yield p


@dataclass(frozen=True)
class Option:
    log_lower: int
    abund_upper: int
    special: bool


@dataclass(frozen=True)
class Stream:
    exponent: int
    options: tuple
    special_options: tuple
    log_prefix: tuple
    abund_prefix: tuple

    @classmethod
    def build(cls, exponent, options):
        return cls(exponent, tuple(options), tuple(o for o in options if o.special),
                   tuple(accumulate((o.log_lower for o in options), initial=0)),
                   tuple(accumulate((o.abund_upper for o in options), initial=0)))

    @staticmethod
    def crossing(options, exponent, num, den):
        """First index with a nonnegative even reduced cost."""
        lo, hi = 0, len(options)
        while lo < hi:
            mid = (lo + hi) // 2
            option = options[mid]
            if exponent * option.log_lower * den < num * option.abund_upper:
                lo = mid + 1
            else:
                hi = mid
        return lo


class RoadblockDual:
    def __init__(self, boundary, table_limit, forbidden=(), expanded=(),
                 special_used=False):
        if boundary < 3 or table_limit < boundary:
            raise ValueError("expected 3 <= boundary <= table_limit")
        forbidden = set(forbidden)
        expanded = set(expanded)
        primes = tuple(odd_primes(table_limit))
        effective_forbidden = forbidden | (set(primes[:bisect_left(primes, boundary)]) - expanded)
        groups = {2: [], 4: []}
        for p in primes[bisect_left(primes, boundary):]:
            if p in forbidden or p in expanded:
                continue
            exponent = 4 if any((p * p + p + 1) % r == 0 for r in effective_forbidden) else 2
            special = (not special_used and p % 4 == 1 and
                       all(((p + 1) // 2) % r != 0 for r in effective_forbidden))
            groups[exponent].append(Option(log_bounds(p)[0], log_bounds(p, p - 1)[1], special))
        self.streams = tuple(Stream.build(e, rows) for e, rows in groups.items())
        tail = table_limit + 1
        self.tail = Option(log_bounds(tail)[0], log_bounds(tail, tail - 1)[1],
                           not special_used)
        self.tail_cap = Fraction(2 * self.tail.log_lower, self.tail.abund_upper)

    def evaluate(self, gap_lower, mu):
        """Check a rational witness and return (scaled bound rounded down, scaled gamma)."""
        mu = Fraction(mu)
        if gap_lower < 0 or not 0 <= mu <= self.tail_cap:
            raise ValueError("expected nonnegative gap and multiplier within the tail cap")
        num, den = mu.numerator, mu.denominator
        value = num * gap_lower
        gamma = (max(0, num * self.tail.abund_upper - den * self.tail.log_lower)
                 if self.tail.special else 0)
        for stream in self.streams:
            e = stream.exponent
            k = stream.crossing(stream.options, e, num, den)
            value += e * den * stream.log_prefix[k] - num * stream.abund_prefix[k]
            # Below the crossing, gain rises with log(q); above it, the gain falls.
            j = stream.crossing(stream.special_options, e, num, den)
            for option in stream.special_options[max(0, j - 1):j + 1]:
                gain = min((e - 1) * option.log_lower * den,
                           num * option.abund_upper - option.log_lower * den)
                gamma = max(gamma, gain)
        return (value - gamma) // den, ceil_div(gamma, den)

    def propose(self, gap_lower):
        """Find a witness. Every result is independently checkable by evaluate()."""
        # The unrounded bound is concave in mu. Integer rounding can flatten
        # comparisons; include endpoints and the best evaluated interior points.
        lo, hi = Fraction(0), self.tail_cap
        best = (0, lo)
        for _ in range(80):
            left, right = (2 * lo + hi) / 3, (lo + 2 * hi) / 3
            left_bound = self.evaluate(gap_lower, left)[0]
            right_bound = self.evaluate(gap_lower, right)[0]
            best = max(best, (left_bound, left), (right_bound, right))
            if left_bound < right_bound:
                lo = left
            else:
                hi = right
        _, mu = max(best, (self.evaluate(gap_lower, self.tail_cap)[0], self.tail_cap))
        # A short dyadic witness is sufficient. Rounding down preserves the cap.
        mu = Fraction(mu.numerator * MULTIPLIER_SCALE // mu.denominator,
                      MULTIPLIER_SCALE)
        return self.evaluate(gap_lower, mu)[0], mu
