"""Finite exhaustive endpoint and slot-count regressions for V17."""
import itertools
from EulerDualBounds import prime_option_group_bounds, coupled_gain_lower

def exhaustive(groups, special_used=False):
    bounds = [prime_option_group_bounds(ordinary, special)
              for ordinary, special in groups]
    reported = coupled_gain_lower(bounds, special_used)
    options = [ordinary + special for ordinary, special in groups]
    endpoint_cases = [list(itertools.product(*[(lo, hi) for lo, hi in opts]))
                      for opts in options]
    actual_min = float("inf")
    for assignments in itertools.product(*endpoint_cases):
        baseline = sum(min(0.0, r) for opts in assignments for r in opts)
        allowed = []
        for (ordinary, special), vals in zip(groups, assignments):
            count = len(ordinary)
            allowed.append([(v, False) for v in vals[:count]] +
                           [(v, True) for v in vals[count:]])
        for choices in itertools.product(*allowed):
            slots = sum(int(kind) for _, kind in choices)
            if slots > (0 if special_used else 1):
                continue
            actual_min = min(actual_min, sum(v for v, _ in choices) - baseline)
    assert reported <= actual_min + 1e-12, (reported, actual_min, groups)
    return reported

both = [([(1.0,1.0)], [(-2.0,-2.0)]), ([(1.0,1.0)], [(-2.0,-2.0)])]
assert 2.999999 < exhaustive(both) <= 3.0
assert 5.999999 < exhaustive(both, special_used=True) <= 6.0
assert coupled_gain_lower([]) == 0.0
for a in (-2.0, 0.0, 2.0):
    for b in (-1.0, 1.0):
        for c in (-2.0, 1.0):
            for d in (-1.0, 2.0):
                groups = [([(a, a+0.125)], [(b, b+0.125)]),
                          ([(c, c+0.125)], [(d, d+0.125)])]
                exhaustive(groups)
                exhaustive(groups, special_used=True)
                exhaustive([(groups[0][0], []), groups[1]])
print("EulerDualTests: OK")
