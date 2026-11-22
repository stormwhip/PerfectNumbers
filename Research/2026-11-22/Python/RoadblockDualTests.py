"""Reproduce the synthetic counterexample and check the fixed-point oracle."""

from fractions import Fraction
from itertools import product
from random import Random
import sys
from time import perf_counter

from RoadblockDual import RoadblockDual, SCALE, ceil_div, log_bounds


def direct(oracle, gap, mu):
    num, den = mu.numerator, mu.denominator
    value = num * gap
    gamma = (max(0, num * oracle.tail.abund_upper - den * oracle.tail.log_lower)
             if oracle.tail.special else 0)
    for stream in oracle.streams:
        for option in stream.options:
            r_even = den * stream.exponent * option.log_lower - num * option.abund_upper
            r_special = den * option.log_lower - num * option.abund_upper
            value += min(0, r_even)
            if option.special:
                gamma = max(gamma, min(0, r_even) - min(0, r_special))
    return (value - gamma) // den, ceil_div(gamma, den)


def exhaustive(oracle, gap):
    options = [(s.exponent, o) for s in oracle.streams for o in s.options]
    choices = [(0, e, 1) if o.special else (0, e) for e, o in options]
    best = None
    for exponents in product(*choices):
        if exponents.count(1) > 1:
            continue
        abund = sum(o.abund_upper for e, (_, o) in zip(exponents, options) if e)
        cost = sum(e * o.log_lower for e, (_, o) in zip(exponents, options))
        remaining = max(0, gap - abund)
        tail_even = Fraction(cost) + oracle.tail_cap * remaining
        candidate = tail_even
        if oracle.tail.special and 1 not in exponents:
            tail_special = Fraction(cost) + oracle.tail.log_lower
            tail_special += oracle.tail_cap * max(0, remaining - oracle.tail.abund_upper)
            candidate = min(candidate, tail_special)
        best = candidate if best is None else min(best, candidate)
    return best


def solve_lp(oracle, gap):
    from scipy.optimize import linprog

    cost, abund, special = [], [], []
    pairs = []
    for stream in oracle.streams:
        for option in stream.options:
            even_idx = len(cost)
            cost.append(stream.exponent * option.log_lower / SCALE)
            abund.append(option.abund_upper / SCALE)
            special.append(0)
            if option.special:
                pairs.append((even_idx, len(cost)))
                cost.append(option.log_lower / SCALE)
                abund.append(option.abund_upper / SCALE)
                special.append(1)
    bounds = [(0, 1)] * len(cost)
    cost.append(float(oracle.tail_cap))
    abund.append(1)
    special.append(0)
    bounds.append((0, None))
    if oracle.tail.special:
        cost.append(oracle.tail.log_lower / SCALE)
        abund.append(oracle.tail.abund_upper / SCALE)
        special.append(1)
        bounds.append((0, 1))

    rows = [[-x for x in abund], special]
    rhs = [-gap / SCALE, 1]
    for i, j in pairs:
        row = [0] * len(cost)
        row[i] = row[j] = 1
        rows.append(row)
        rhs.append(1)
    result = linprog(cost, A_ub=rows, b_ub=rhs, bounds=bounds, method="highs")
    if not result.success:
        raise RuntimeError(result.message)
    return result.fun


def regression():
    even = (29, 31, 41, 43, 47, 59, 61)
    gap = log_bounds(38, 37)[0]
    for p in even:
        gap += log_bounds(p * p + p + 1, p * p)[0]
    cost_upper = log_bounds(37)[1] + sum(2 * log_bounds(p)[1] for p in even)
    start = perf_counter()
    oracle = RoadblockDual(29, 300000, forbidden={7}, expanded={3, 5, 11, 13, 17, 19, 23})
    setup = perf_counter() - start
    start = perf_counter()
    bound, mu = oracle.propose(gap)
    elapsed = perf_counter() - start
    assert bound == oracle.evaluate(gap, mu)[0]
    assert bound <= cost_upper
    assert 55 * SCALE < bound < 57 * SCALE
    print(f"synthetic b=29: bound={bound / SCALE:.9f}, "
          f"witness cost={cost_upper / SCALE:.9f}, mu={float(mu):.6f}")
    print(f"300000 table: setup={setup:.3f}s, multiplier proposal={elapsed:.4f}s")
    relaxed_gap = sum(log_bounds(p, p - 1)[0] for p in (*even, 37))
    relaxed_bound, _ = oracle.propose(relaxed_gap)
    print(f"infinite-power gap: lower bound={relaxed_bound / SCALE:.9f}")


def checks(compare_lp=False):
    rng = Random(2400)
    max_gap = 0.0
    for p in (3, 5, 17, 23, 29, 61, 1021, 299993):
        lo, hi = log_bounds(p)
        ab_lo, ab_hi = log_bounds(p, p - 1)
        assert lo <= hi and 0 < ab_lo <= ab_hi
        assert hi - lo < 10_000 and ab_hi - ab_lo < 1_000
    for _ in range(200):
        boundary = rng.randint(3, 19)
        limit = rng.randint(boundary, 37)
        forbidden = rng.sample((3, 5, 7, 11, 13, 17), rng.randrange(4))
        expanded = rng.sample([p for p in (3, 5, 7, 11, 13, 17) if p not in forbidden], 2)
        oracle = RoadblockDual(boundary, limit, forbidden, expanded, rng.choice((True, False)))
        gap = rng.randrange(100) * SCALE // 200
        for mu in (Fraction(0), oracle.tail_cap, oracle.tail_cap * rng.randrange(101) / 100):
            assert oracle.evaluate(gap, mu) == direct(oracle, gap, mu)
        bound, mu = oracle.propose(gap)
        assert oracle.evaluate(gap, mu) == direct(oracle, gap, mu)
        assert 0 <= bound <= exhaustive(oracle, gap)
        if compare_lp:
            lp_gap = solve_lp(oracle, gap) - bound / SCALE
            assert -1e-7 < lp_gap < 1e-7, lp_gap
            max_gap = max(max_gap, abs(lp_gap))
    if compare_lp:
        print(f"passed 200 HiGHS comparisons; max absolute difference={max_gap:.3g}")
    print("passed 200 exhaustive instances and 800 direct exact evaluations")


if __name__ == "__main__":
    checks(compare_lp='--compare-lp' in sys.argv[1:])
    regression()
