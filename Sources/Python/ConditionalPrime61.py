"""Conditional on the first eight primes being excluded, partition 61 exponents.

With 31 excluded, 61 cannot have an odd exponent because 61 ≡ -1 (mod 31)
and 31 | sigma(61^odd). Exponents 2, 4, 8 are excluded by sigma factors
in {3,5,13,19}; hence the remaining cases are 6 and >=10 (even).

This script performs separate primal/interval-dual solves for both cases;
it does not itself establish the preceding eight root eliminations.
"""
from IntervalCertificate61 import solve_and_certify

S8 = {3, 5, 7, 11, 13, 17, 19, 31}
TARGET = 2400.0
for mode in (None, "exact6", "atleast10"):
    primal, certified = solve_and_certify(
        S8, P_max=4000, a_cut=16, certify=True, force61_mode=mode
    )
    print(f"CONDITIONAL_61 mode={mode or 'none'} float={primal:.12f} "
          f"dualLower={certified:.12f} "
          f"exceeds2400={certified > TARGET}", flush=True)

print("COVERAGE odd e impossible via 31; e=2,4,8 impossible via sigma; "
      "remaining e=6 or even e>=10", flush=True)
