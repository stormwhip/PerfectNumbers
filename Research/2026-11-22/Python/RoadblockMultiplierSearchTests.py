"""Differential tests for exact roadblock multiplier selection."""

from fractions import Fraction
from random import Random
from time import perf_counter

from RoadblockBoundaryProfile import BoundaryProfile, FactorTable
from RoadblockDual import RoadblockDual, SCALE, log_bounds
from RoadblockMultiplierSearch import BoundaryDual, first_certified_boundary


def checks():
    rng = Random(3954)
    count = 0
    for _ in range(80):
        limit = rng.randint(5, 27)
        table = FactorTable(limit)
        pool = (*table.primes, 67, 79, 151)
        forbidden = set(rng.sample(pool, rng.randrange(3)))
        expanded = set(rng.sample(sorted(set(pool) - forbidden), rng.randrange(3)))
        special_used = rng.choice((False, True))
        gap = rng.randint(1, 99) * SCALE // 100
        den = rng.randint(1, 3)
        values = []
        for boundary in range(3, limit + 1):
            direct = RoadblockDual(boundary, limit, forbidden, expanded, special_used)
            dual = BoundaryDual(table, boundary, forbidden, expanded, special_used)
            cap = int(direct.tail_cap * den)
            vals = [dual.numerator_and_slope(gap, num, den) for num in range(cap + 1)]
            assert all(x[0] // den == direct.evaluate(gap, Fraction(i, den))[0]
                       for i, x in enumerate(vals))
            maximum, _ = dual.maximize(gap, den, 0, cap)
            assert maximum == max(v for v, _ in vals)
            # A tangent produced at an endpoint, even activation, or tied
            # special option must majorize the function on both sides.
            for i, (value, slope) in enumerate(vals):
                for j in (0, max(0, i - 1), min(cap, i + 1), cap):
                    assert vals[j][0] <= value + slope * (j - i)
            values.append(maximum // den)
            count += len(vals)
        for budget in {0, values[0], values[-1], rng.choice(values), max(0, values[-1] - 1)}:
            match = next((b for b, value in enumerate(values, 3) if value > budget), None)
            cert = first_certified_boundary(table, gap, budget, forbidden, expanded, special_used, den)
            assert (cert.boundary if cert else None) == match
            if cert:
                assert BoundaryProfile(table, gap, cert.multiplier, forbidden, expanded,
                                       special_used).at(cert.boundary) == cert.bound
    print(f"80 randomized states, {count} exact lattice evaluations agree with reference")


def synthetic():
    table = FactorTable(300_000)
    forbidden = {7}
    expanded = {3, 5, 11, 13, 17, 19, 23}
    gap = log_bounds(38, 37)[0] + sum(
        log_bounds(p*p+p+1, p*p)[0] for p in (29, 31, 41, 43, 47, 59, 61))
    for budget, expected_boundary in ((55, 3), (56, 30)):
        start = perf_counter()
        cert = first_certified_boundary(table, gap, budget*SCALE, forbidden, expanded)
        elapsed = perf_counter() - start
        assert cert is not None and cert.boundary == expected_boundary
        direct = RoadblockDual(cert.boundary, table.limit, forbidden, expanded)
        assert direct.evaluate(gap, cert.multiplier)[0] == cert.bound
        assert BoundaryProfile(table, gap, cert.multiplier, forbidden, expanded
                               ).first_above(budget*SCALE) == cert.boundary
        print(f"synthetic budget={budget}: first boundary={cert.boundary}, "
              f"multiplier={float(cert.multiplier):.10f}, lower bound={cert.bound/SCALE:.10f}; "
              f"search={elapsed:.3f}s (shared table excluded)")


if __name__ == "__main__":
    checks()
    synthetic()
