"""Regression tests for interval-certified LP gain arithmetic."""
from itertools import product
from mpmath import iv

from IntervalCertificate import forced_prime_gain_lower

iv.dps = 40

def check(intervals):
    endpoints = [(x.a, x.b) for x in intervals]
    lower = forced_prime_gain_lower(endpoints)
    for values in product(*[(float(x.a), float(x.b)) for x in intervals]):
        actual = min(values) - sum(min(0.0, x) for x in values)
        assert lower <= actual + 1e-14, (lower, actual, values)
    return lower

gain = check([iv.mpf([-3, -2.9]), iv.mpf([-1, -0.9])])
assert 0.79 < gain < 0.81, gain

gain = check([iv.mpf([-3, -2.9]), iv.mpf([1, 2])])
assert gain <= 0.0, gain

gain = check([iv.mpf([-3, -3]), iv.mpf([-1, -1])])
assert 0.999999999999999 < gain <= 1.0, gain

gain = check([iv.mpf([-1, -0.5])])
assert gain <= 0.0, gain

print("CertificateTests: OK")
