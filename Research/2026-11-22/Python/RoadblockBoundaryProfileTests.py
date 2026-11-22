"""Check all event boundaries against independently rebuilt reference streams."""

from fractions import Fraction
from random import Random
from time import perf_counter

from RoadblockBoundaryProfile import BoundaryProfile, FactorTable
from RoadblockDual import RoadblockDual, SCALE, log_bounds


def main():
    rng = Random(20261122)
    for _ in range(80):
        limit = rng.randint(13, 90)
        table = FactorTable(limit)
        extended = (*table.primes, 109, 127, 151, 229)
        forbidden = set(rng.sample(extended, rng.randrange(5)))
        expanded = set(rng.sample(sorted(set(extended) - forbidden), rng.randrange(5)))
        special_used = rng.choice((True, False))
        gap = rng.randrange(101) * SCALE // 100
        cap = RoadblockDual(3, limit, forbidden, expanded, special_used).tail_cap
        mu = cap * (Fraction(1) if rng.randrange(5) == 0 else Fraction(rng.randrange(101), 100))
        profile = BoundaryProfile(table, gap, mu, forbidden, expanded, special_used)
        expected = [RoadblockDual(b, limit, forbidden, expanded, special_used).evaluate(gap, mu)[0]
                    for b in range(3, limit + 1)]
        assert expected == sorted(expected)
        assert expected == [profile.at(b) for b in range(3, limit + 1)]
        for budget in (expected[0] - 1, rng.choice(expected), expected[-1]):
            index = next((i + 3 for i, value in enumerate(expected) if value > budget), None)
            assert index == profile.first_above(budget)

    # An explicit forbidden prime above the cutoff can block a finite even option.
    table = FactorTable(29)
    oracle = RoadblockDual(29, 29, {67})
    profile = BoundaryProfile(table, SCALE // 50, oracle.tail_cap, {67})
    assert profile.at(29) == oracle.evaluate(SCALE // 50, oracle.tail_cap)[0]
    print("80 randomized profiles: all boundaries and strict thresholds agree")

    start = perf_counter()
    table = FactorTable(300000)
    table_seconds = perf_counter() - start
    expanded = {3, 5, 11, 13, 17, 19, 23}
    gap = log_bounds(38, 37)[0]
    for p in (29, 31, 41, 43, 47, 59, 61):
        gap += log_bounds(p*p + p + 1, p*p)[0]
    oracle = RoadblockDual(29, 300000, {7}, expanded)
    bound, multiplier = oracle.propose(gap)
    start = perf_counter()
    profile = BoundaryProfile(table, gap, multiplier, {7}, expanded)
    profile_seconds = perf_counter() - start
    assert profile.at(29) == bound
    print(f"synthetic bound={bound / SCALE:.9f}; precompute={table_seconds:.3f}s; "
          f"one witness profile={profile_seconds * 1000:.3f}ms; events={len(profile.cuts)}")


if __name__ == "__main__":
    main()
