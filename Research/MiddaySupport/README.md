# Support cells and dyadic residual prices

Baseline `6732a1a`. All results below are necessary conditions on a hypothetical odd perfect `N <= 10^2400`; none of the conditional exclusions is an additional complete actual exponent in the global ledger.

## Root 31, exact exponent 10

Assume `19,7,11` are absent (canonical prior roots) and `31^10 || N`. Exactly one of 3 and 5 divides N. If it is 5, at least one of 13 and 17 divides N. These conclusions rely on the baseline three-root hitting theorem (not a new proof that 3 or 5 must be present). The outstanding cases are: 3 present and 5 absent; or 3 absent, 5 present and at least one of 13,17 present.

* [Full31](Full31.json.gz) rules out 5 present and `3,13,17` all absent. The prime `q=150332843` divides `sigma(31^10)=23*397*617*q`. There are 40 admissible actual exponents at q through 100, followed by a lower-exponent tail. The minimum exact integer log floor is 2407, tail floor 2872. The old Nov25 result stopped at 20.
* [Both31](Both31.json.gz) rules out 3 and 5 both present. First [Transfer](Transfer.py) proves (without the size bound) that 13,17,29,37 are absent and `5^1 || N`. For each excluded prime or higher exponent, minimize the forced-support abundancy over every possible Euler position and compare strict rational products with 2. Having fixed 5, all other primes have even exponents. The bound for all candidate `q` exponents but 40 comes from 39 finite cells and one tail (floor 3103). At 40 another 21 exact choices of `v3(N)` plus a tail (floor 2402) cover the remaining possibilities. All 62 leaves exceed `10^2400` **strictly**, including the leaf whose floor is exactly 2400.
* The exclusion of primes and fixing 5 in the preceding step applies to every even exponent E with `11 | E+1`; all this step uses is `sigma(31^10) | sigma(31^E)` and monotonic abundancy. The full conditional forest uses the exact exponent 10. In the analogous root-13 class (prior 19,7,11,31 absent), the same transfer proves that 3 and 5 together force `3² || N`, `5 || N`, and absence of 17,29,37,41,43,47,53,59,61. Do not transfer an exact exponent's outgoing sigma directly to a larger arbitrary exponent.

Reproduce from repo root (stdlib only, no online hints):

```
python -I -S -B -X int_max_str_digits=0 Research/MiddaySupport/VerifyTransferForest.py
python -I -S -B -X int_max_str_digits=0 Research/MiddaySupport/Independent31.py
python -I -S -B -X int_max_str_digits=0 Research/MiddaySupport/Independent31.py --both
```

The latter two commands independently enumerate exact cells and compare integers using a separate ordinary/flexible-subtree product recurrence, sharing only ECPP arithmetic. The root sigma fixes initial demand. Only the excess threshold of the tail is changed; no new sigma factor is asserted for that tail. At every other level an exact component may activate its sigma. The disjoint-owner and multiplicity arguments are as in the [baseline composition](../Nov25/Compose/README.md).

## Omission of two of 3, 5, 7

[PairDual](PairDual.py) rechecks the original and replacement factor archives, recomputes a fixed integer dual and reproduces the older exponent list *before* strengthening it. All nominated factors are tested for divisibility and deterministic primality (64-bit or Pocklington/ECPP); no factoring cache is a replay dependency. The small helper input for 3 and 5 came from prior unregistered numerical research and has no authority before these arithmetic checks. The canonical previous published two-root support partition for 7 had 291 exceptions, largest 924. The improved 7 condition has 253 exceptions, largest 826. Analogous fully checked conditions for root 3 and 5 have 1188/701 even exponents, largest 2394/1422 respectively. In the case of root 5 and absent 3, no odd exponent can occur since `3 | sigma(5^f)` for every odd f. Budget exhaustion and all remaining exponents are UNKNOWN. Three- and five-root results do not improve the largest known overall canonical frontier bounds: they describe **different, less restricted support classes**.

1. Split the forced root sigma into explicit prime powers, certified new primes, and residual cyclotomic layers. For potentially overlapping layers, move all their common prime support into a single disjoint block. In a remaining layer `Phi_h(p)` coprime to `h`, a prime factor r has exact multiplicative order h; r is therefore 1 modulo 2h (h odd). Elementary proof: over characteristic r not dividing h, `X^h-1` has simple roots, so the `Phi_d` factors for `d|h` cannot share a root. Any root of `Phi_h` has exact order h. This increases the minimum prime admitted by each block and reduces its allowed abundance.
2. A nonsquare disjoint block has at least one odd valuation. Charge its smallest possible prime once more for rounding to an even exponent, unless that odd valuation belongs to Euler. In a block equal to 3 modulo 4, at least one such prime is 3 modulo 4 and cannot be Euler. Other blocks and explicitly rounded outside primes share **at most one** Euler discount.
3. For a certified new prime q, replace bare rounding by pricing a finite list of actual exponents and a uniform exponent tail. An exact exponent pays its own excess over root demand and a rough part c of its sigma. Remove support of *every* modeled explicit prime, the entire root sigma and all pre-existing anonymous blocks. Increment log cost by `log c` and upper-credit any new abundance by the checked rough-block bound. The residual products can overlap across distinct sources: multiplicities in their product still divide `N`, while summing separate abundance credits can only overestimate available abundance. Ignoring a negative-priced block is legitimate: omit its size as well as its credit, and any remaining prime is represented by the generic tail. Existing exact/tail rows at forced explicit sources are likewise tightened by their actual exponent and optional emission. These prices never charge a relaxed-tail valuation as an exact sigma.
4. The old directed bounds and dyadic integer multipliers are retained; changing the exact root's upper abundance and restoring the new conditional lower terms is integer arithmetic. Do not interpret floors or numerical LP feasibility as sufficient: admission uses `z > 2400 * DYADIC * upper_log(10)`.

```
python -I -S -B Research/MiddaySupport/PairDual.py Research/NightUniform/TwoAvoidSevenB.json
python -I -S -B Research/MiddaySupport/PairDual.py Research/MiddaySupport/TwoTail3.json
python -I -S -B Research/MiddaySupport/PairDual.py Research/MiddaySupport/TwoTail5.json
python -I -S -B Research/MiddaySupport/SupportClosure.py --check
```

See [root 7 exceptions](PairResults.json), [root 3](PairResults3.json), [root 5](PairResults5.json) and the [positive-support scan](Positive35.json). Checks of the positive 3+5 cell span all 435 baseline actual exponents for which the cell is not excluded by the canonical prior, over 511 distinct actuals. Sieve decision *open* does not mean the branch or exponent is realizable. In the scans for (13,10), two nested exponent splits left holes; unverified partial cells were not packaged for admission. This pair has separately been closed by the MiddayForest route.
