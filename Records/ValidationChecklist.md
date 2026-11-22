# Proof Validation Checklist

A run printing `PROVEN` is experimental evidence until its mathematical and computational assumptions have been checked.

- [x] Verify the exponent-covering combinatorial lemma on the V6 branch list for selected root primes and exponents through 2048 (automated test); independent formal proof review remains open.
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


## V6 audit changes (2026-11-22)

- V6 replaces finite-table exhaustion in the roadblock fractional knapsack with an explicit infinite even-prime tail, using an upper bound on abundance per unit log-size for all primes beyond the table. It optimistically grants a possible tail special prime's full maximum abundance for free. This produces a conservative relaxation.
- V6 recomputes composite size contributions from pairwise coprime residuals that are also coprime to known prime divisors; every residual gets an optimistic abundance allowance even when it shares factors with another residual.
- A limited combinatorial check finds no missing exponent classes for the V6 branches on selected primes through exponent 2048. Coverage follows from divisibility \(d+1\mid a+1\) for inexact branches; a complete, independently reviewed proof remains a separate task.
- The ALPHA=10^8 residual factor assumption is inherited and must be checked against the database. No new unconditional lower bound is claimed from V6.

## Source validation record

- 2026-11-22: [GitHub Actions quality run 44990984163](https://github.com/stormwhip/PerfectNumbers/actions/runs/44990984163) succeeded for commit `9dc5cd6`. C++ compilation of the index builder and V1–V6, C++ core tests, and Python syntax checks all passed.
- Dataset-backed proof-tree regression and independent mathematical certification remain separate verification gates.
