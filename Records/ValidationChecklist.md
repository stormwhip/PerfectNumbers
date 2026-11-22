# Proof Validation Checklist

A run printing `PROVEN` is experimental evidence until its mathematical and computational assumptions have been checked.

- [x] Verify the exponent-covering combinatorial lemma on the V6 branch list for selected root primes and exponents through 2048 (automated test); independent formal proof review remains open.
- [ ] Check that every roadblock bound covers the infinite prime tail beyond the finite sieve, and confirm binary-search monotonicity.
- [ ] Replace all decision-critical floating-point inequalities with certified lower/upper enclosures or conservative directed rounding.
- [ ] Check primality and factorization certificates for all database entries used as primes; `mpz_probab_prime_p` is probabilistic.
- [ ] Audit composite-factor lower-bound assumptions (including ALPHA), overlapping factors, and multiplicities.
- [ ] Verify the LP relaxation includes a safe infinite tail, handles all special-prime options and uses a checkable dual certificate.
- [ ] Validate all eight root primes in the order `19,7,11,31,13,3,5,17` at exponent `2400` and the enhanced complementary LP.
- [ ] Record a pinned source commit, database hash, compiler versions, runtime arguments and complete results.
- [ ] Repeat critical targets with an independent checker or a second implementation.

## Initial audit findings (2026-11-22)

Historical V5 source is available in the [pre-cleanup snapshot](https://github.com/stormwhip/PerfectNumbers/tree/124ab21449d4afd9d017a32faa9bd27253943c70); the current proof engine is `Sources/Cpp/ProofTreeV16.cpp`. Re-audit the same questions for V16:

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

## 2400 proof-specific release gates (2026-11-22)

- [x] Independent exact multiplication and primality testing of the sigma(61^e) factorization data used to strengthen the LP, including e=10,12; see [45001172416](https://github.com/stormwhip/PerfectNumbers/actions/runs/45001172416).
- [x] Computer-generated interval-dual lower exponent >2400 for the **S8-coprime** case, with recorded result 2400.822998027028.
- [ ] Independent proof that the LP relaxation covers ordinary and Euler-special exponent families and the infinite tails conservatively.
- [ ] Export and validate a fully checkable dual witness, including all numerical coefficient enclosures and multiplier signs.
- [ ] Test complete 256-mask **enhanced** prefix-certificate production against V16's CSV loader; check terminal mask 255.
- [ ] Complete all eight root trees at exponent 2400 with no unresolved branches or roadblocks.
- [ ] Independently certify branch-critical float comparisons, prime certificates and ALPHA/composite bounds.
- [ ] Add reliable checkpoint/restart/task-aggregation with source SHA and database hash before multi-day calculations.
- [ ] Reproduce the assembled theorem with a separate verifier.

See [ProgressReport2400](../Documentation/ProgressReport2400.md) for the task plan.
