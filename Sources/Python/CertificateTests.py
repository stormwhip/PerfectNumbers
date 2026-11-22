"""Standard-library regression tests for interval-safe forced-prime gains."""
from itertools import product

from DualGainBounds import forced_prime_gain_lower

def check(intervals):
    lower = forced_prime_gain_lower(intervals)
    for values in product(*[(lo, hi) for lo, hi in intervals]):
        actual = min(values) - sum(min(0.0, x) for x in values)
        assert lower <= actual + 1e-14, (lower, actual, values)
    return lower

gain = check([(-3.0, -2.9), (-1.0, -0.9)])
assert 0.79 < gain < 0.81, gain

gain = check([(-3.0, -2.9), (1.0, 2.0)])
assert gain <= 0.0, gain

gain = check([(-3.0, -3.0), (-1.0, -1.0)])
assert 0.999999999999 < gain <= 1.0, gain

gain = check([(-1.0, -0.5)])
assert gain <= 0.0, gain

assert forced_prime_gain_lower([]) == 0.0
print("CertificateTests: OK")
