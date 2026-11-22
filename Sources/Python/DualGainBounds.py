"""Outward-rounded lower bounds for dual reduced-cost gains."""
import math


def forced_prime_gain_lower(reduced_cost_intervals):
    """Lower-bound min(r_i) - sum(min(0, r_i)) from interval endpoints.

    Each input pair is (lower_i, upper_i), enclosing a reduced cost r_i.
    The forced minimum uses the smallest lower endpoint. The baseline penalty
    uses the sum of negative upper endpoints, an upper bound before subtraction.
    Every float conversion and accumulation is rounded outward.
    """
    intervals = list(reduced_cost_intervals)
    if not intervals:
        return 0.0

    lower_values = [
        math.nextafter(float(lower), -math.inf)
        for lower, _ in intervals
    ]
    upper_values = [
        math.nextafter(float(upper), math.inf)
        for _, upper in intervals
    ]

    baseline_upper = 0.0
    for upper in upper_values:
        baseline_upper = math.nextafter(
            baseline_upper + min(0.0, upper),
            math.inf,
        )

    return math.nextafter(min(lower_values) - baseline_upper, -math.inf)
