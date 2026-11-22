"""Exact dyadic multiplier and boundary search for experimental roadblocks."""

from bisect import bisect_left
from dataclasses import dataclass
from fractions import Fraction

from RoadblockDual import MULTIPLIER_SCALE, Option, Stream


class BoundaryDual:
    """Compiled two-stream dual at a single boundary, using a shared factor table."""

    def __init__(self, table, boundary, forbidden, expanded, special_used):
        if not 3 <= boundary <= table.limit:
            raise ValueError("boundary outside the prime table")
        forbidden, expanded = set(forbidden), set(expanded)
        remote = tuple(r for r in forbidden if r > table.limit)

        def blocked(factors):
            return any(r in forbidden or (r < boundary and r not in expanded) for r in factors)

        groups = {2: [], 4: []}
        for i in range(bisect_left(table.primes, boundary), len(table.primes)):
            q = table.primes[i]
            if q in forbidden or q in expanded:
                continue
            even = 4 if (blocked(table.even_factors[q]) or
                         any((q * q + q + 1) % r == 0 for r in remote)) else 2
            special = (not special_used and q % 4 == 1 and
                       not blocked(table.special_factors[q]))
            groups[even].append(Option(*table.logs[q], special))
        self.streams = tuple(Stream.build(e, options) for e, options in groups.items())
        self.tail = Option(*table.logs[table.limit + 1], not special_used)

    def numerator_and_slope(self, gap, num, den):
        """Return den times the unrounded bound and one exact supergradient."""
        value, slope = num * gap, gap
        gamma, gamma_slope = 0, 0
        if self.tail.special:
            gain = num * self.tail.abund_upper - den * self.tail.log_lower
            if gain > 0:
                gamma, gamma_slope = gain, self.tail.abund_upper
        for stream in self.streams:
            e = stream.exponent
            index = stream.crossing(stream.options, e, num, den)
            abundance = stream.abund_prefix[index]
            value += e * den * stream.log_prefix[index] - num * abundance
            slope -= abundance
            index = stream.crossing(stream.special_options, e, num, den)
            for option in stream.special_options[max(0, index - 1):index + 1]:
                cost = den * option.log_lower
                special_gain = num * option.abund_upper - cost
                gain = min((e - 1) * cost, special_gain)
                if gain > gamma:
                    gamma = gain
                    # At equality the even option was excluded by crossing().
                    gamma_slope = option.abund_upper if special_gain == gain else 0
        return value - gamma, slope - gamma_slope

    def maximize(self, gap, den, lower_num, upper_num):
        """Return the exact lattice maximum in [lower_num, upper_num]."""
        best = None
        while lower_num <= upper_num:
            num = (lower_num + upper_num) // 2
            value, slope = self.numerator_and_slope(gap, num, den)
            if best is None or value > best[0]:
                best = value, num
            if slope > 0:
                lower_num = num + 1
            elif slope < 0:
                upper_num = num - 1
            else:
                break
        return best


@dataclass(frozen=True)
class Certificate:
    boundary: int
    multiplier: Fraction
    bound: int


def first_certified_boundary(table, gap, budget, forbidden=(), expanded=(),
                             special_used=False, denominator=MULTIPLIER_SCALE):
    """Find the smallest certified boundary on the specified multiplier lattice.

    Returns None when a nonnegative budget cannot be exceeded on this lattice.
    Callers should handle a negative size budget as a direct size contradiction.
    """
    if denominator <= 0 or budget < 0 or table.limit < 3:
        raise ValueError("expected a positive denominator and nonnegative budget")
    if gap <= 0:
        return None
    tail_log, tail_abundance = table.logs[table.limit + 1]
    first_num = ((budget + 1) * denominator + gap - 1) // gap
    last_num = 2 * tail_log * denominator // tail_abundance
    if first_num > last_num:
        return None

    forbidden, expanded = tuple(forbidden), tuple(expanded)
    lo, hi = 3, table.limit
    best = None
    while lo <= hi:
        boundary = (lo + hi) // 2
        dual = BoundaryDual(table, boundary, forbidden, expanded, special_used)
        value, num = dual.maximize(gap, denominator, first_num, last_num)
        bound = value // denominator
        if bound > budget:
            best = Certificate(boundary, Fraction(num, denominator), bound)
            hi = boundary - 1
        else:
            lo = boundary + 1
    return best
