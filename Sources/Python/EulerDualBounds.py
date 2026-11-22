"""Outward-rounded reduced-cost groups for at-most-one Euler-special slot."""
import math

def lower(v):
    return math.nextafter(float(v), -math.inf)

def upper(v):
    return math.nextafter(float(v), math.inf)

def prime_option_group_bounds(ordinary_intervals, special_intervals):
    """Return (ordinary_min_lower, special_min_lower or None, baseline_upper)."""
    if not ordinary_intervals:
        raise ValueError("Every explicitly modeled odd prime needs an ordinary tail option")
    ordinary = min(lower(lo) for lo, _ in ordinary_intervals)
    special = min((lower(lo) for lo, _ in special_intervals), default=None)
    baseline_upper = 0.0
    for _, hi in list(ordinary_intervals) + list(special_intervals):
        baseline_upper = math.nextafter(
            baseline_upper + min(0.0, upper(hi)), math.inf
        )
    return ordinary, special, baseline_upper

def coupled_gain_lower(groups, special_used=False):
    """Extra dual lower bound when all groups occur and <=1 has special exponent.

    For each forced group q the chosen reduced cost is ordinary o_q or
    special s_q. The minimum with at most one special is
    sum(o_q) - max(0, max(o_q - s_q)).
    Subtract the upper bound on the old sum of negative reduced costs,
    using outward rounding in every floating arithmetic operation.
    """
    if not groups:
        return 0.0
    ordinary_sum = baseline_upper = best_saving_upper = 0.0
    for ordinary, special, baseline in groups:
        ordinary_sum = math.nextafter(ordinary_sum + ordinary, -math.inf)
        baseline_upper = math.nextafter(baseline_upper + baseline, math.inf)
        if not special_used and special is not None:
            saving_upper = math.nextafter(ordinary - special, math.inf)
            best_saving_upper = max(best_saving_upper, saving_upper)
    joint_lower = math.nextafter(ordinary_sum - best_saving_upper, -math.inf)
    gain_lower = math.nextafter(joint_lower - baseline_upper, -math.inf)
    return max(0.0, gain_lower)
