# Proof Validation Checklist

A run printing `PROVEN` is experimental evidence until its mathematical and computational assumptions have been checked.

- [ ] Prove that the exponent branching covers every Euler-allowed prime-power exponent, including possible special-prime exponents congruent to 1 modulo 4.
- [ ] Check that every roadblock bound covers the infinite prime tail beyond the finite sieve, and confirm binary-search monotonicity.
- [ ] Replace all decision-critical floating-point inequalities with certified lower/upper enclosures or conservative directed rounding.
- [ ] Check primality and factorization certificates for all database entries used as primes; `mpz_probab_prime_p` is probabilistic.
- [ ] Audit composite-factor lower-bound assumptions (including ALPHA), overlapping factors, and multiplicities.
- [ ] Verify the LP relaxation includes a safe infinite tail, handles all special-prime options and uses a checkable dual certificate.
- [ ] Validate all 15 forbidden-prime roots in the intended exclusion order, and validate the complementary endgame.
- [ ] Record a pinned source commit, database hash, compiler versions, runtime arguments and complete results.
- [ ] Repeat critical targets with an independent checker or a second implementation.

## Initial audit findings (2026-11-22)

Review `Sources/Cpp/ProofTreeV5.cpp` before treating its output as a mathematical certificate:

1. `get_exponents` inserts the exact special-prime exponent `a=1` and generic even exponents; explicit coverage of `a=5,9,...` is not apparent. This is a proof-completeness risk.
2. `compute_roadblock_bound` currently returns success when it exhausts a finite prime table. An analytic enclosure of the omitted infinite tail is needed for soundness.
3. Floating-point cutoffs and probabilistic primality tests require proof-grade auditing.

These are open audit items, not claims that a mathematical theorem is false.
