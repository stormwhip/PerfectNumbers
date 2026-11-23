# Forbidden-Sigma Exponent DP: 15 More Certified Root Contradictions

**Research date:** 2026-11-23. **Target:** exclude odd perfect numbers `N<=10^2400` in selected canonical exponent shards. **Status:** exact-integer mathematical certificates and independent verifier implementation committed; fresh repository CI and full direct-root audit remain to be executed.

This strengthens [CyclotomicEulerPrimorial2400.md](CyclotomicEulerPrimorial2400.md) by preserving the forbidden-root constraints on every *candidate quotient prime's exponent*.

## 1. Setup and mathematical necessity

Let `m=d+1` be odd prime with `m>p`, `A=Phi_m(p)=sigma(p^d)`, `P=p^d A<=B=10^2400`, and `R=floor(B/P)`. A non-exact canonical shard represents `m|(e+1)` with actual root exponent `e>=d`. Therefore `N=P Q` for an odd positive `Q<=R`.

All prime divisors of `A` lie in the congruence class `1 (mod 2m)`; in particular `A` has no prime factor below `L=2m+1`. For each prime `q<L` other than `p` and earlier forbidden roots `F`, the exponent `v_q(Q)` equals the *actual exact* exponent `v_q(N)`.

Because `sigma(q^{v_q(N)})|sigma(N)=2N`, a necessary condition for such a prime is

```
f does not divide sigma(q^e), for every earlier forbidden root f in F.
```

This condition is evaluated exactly, without factoring `sigma(q^e)`:

```
if q mod f == 1:  f | sigma(q^e) iff (e+1) mod f == 0
otherwise:        f | sigma(q^e) iff q^(e+1) mod f == 1.
```

By Euler's theorem, all such small-prime exponents are even except possibly one exponent congruent to `1 (mod 4)`, at a prime `q=1 (mod 4)`.

For each small `q`, define a *conservative minimum* ordinary exponent `a_q` by scanning even exponents `2,4,...,200` for the first one satisfying the forbidden-factor tests. If all fail, take `a_q=202`; every possible admissible exponent must indeed be at least 202. Likewise define a candidate Euler-special minimum `b_q` among `1,5,...,201` for `q=1 (mod 4)`, or take `b_q=205` if none passes. The fallback values are lower bounds only, not assertions that those exponent classes are possible.

## 2. Exact integer DP for the smallest quotient

List the allowed primes below `L` in increasing order. Define

- `D0[k]`: the minimum product of `k` distinct small-prime powers with all ordinary even exponents;
- `D1[k]`: the minimum product of `k` distinct small-prime powers with exactly one possible Euler-special odd exponent.

Initially `D0[0]=1` and all other values are infinity. For each small prime `q`, allow skipping the prime or the following transitions:

```
D0[k+1] <- min(D0[k+1], D0[k]*q^a_q)
D1[k+1] <- min(D1[k+1], D1[k]*q^a_q)
D1[k+1] <- min(D1[k+1], D0[k]*q^b_q)   [q=1 (mod 4)]
```

Implement updates in decreasing `k` so every prime is used at most once. Cap values exceeding `R` at `R+1`. Then

```
M_k = min(D0[k], D1[k])
```

is a rigorous lower bound on the size of the small-prime component of any admissible `Q` containing exactly `k` distinct small primes.

For an independent finite bound `K` on possible `k`, continue to use `(r_1...r_K)^2/r_K<=R` from Euler's one-special-prime theorem. No other `k` can occur.

## 3. Abundance upper bound and integer certificate

Let `r_1<...<r_k` denote the `k` smallest primes below `L` not in `F union {p}`. Any `k` distinct small prime factors, regardless of which are selected, contribute at most

```
U_k = product_(i=1)^k r_i/(r_i-1)
```

to abundance. All other quotient primes except `p` are at least `L`. Their number is at most

```
v_k=floor(log_L(floor(R/M_k))),
```

which is computed by repeated *integer division*. They contribute at most `(L/(L-1))^v_k`.

As in the unweighted certificate, let `T=floor(log_L A)`, `C=1+ceil(log_2 T)`. For every possible `k`,

```
sigma(N)/N <
    [p/(p-1)] * [2m/(2m-C)]
    * [product_(i=1)^k r_i/(r_i-1)]
    * [L/(L-1)]^v_k.
```

For all cases with `M_k<=R`, a strict upper bound below 2 suffices.

### Stronger final implementation: exact cyclotomic and large-prime products

The checked code uses two strictly sharper rational expressions.

First, `A=Phi_m(p)` has at most `T` distinct prime divisors, and its abundance is bounded by the **full exact product**

```
A_upper = product_(i=1)^T (2mi+1)/(2mi).
```

Second, let `s_1<s_2<...` be the actual increasing sequence of prime numbers at least `L`. For `Q/M_k` size budget `R/M_k`, define `v_k` as the largest nonnegative integer satisfying

```
product_(j=1)^v_k s_j <= floor(R/M_k).
```

Any `v` distinct large prime factors have product at least the product of the first `v` such primes and abundance at most `product_(j=1)^v s_j/(s_j-1)`. Hence the final integer-certified exclusion compares

```
sigma(N)/N <
  [p/(p-1)] * A_upper
  * [product_(i=1)^k r_i/(r_i-1)]
  * [product_(j=1)^v_k s_j/(s_j-1)] < 2.
```

The program builds every numerator, denominator, and initial prime product with exact integers. Its deterministic sieve includes primes below 20,000 and explicitly returns an *inconclusive* result if these primes do not exhaust the size budget. Root-17 exponent `708` has an upper bound approximately `1.9997019240`; exponent `718` approximately `1.9906026916`. Both comparisons are strictly certified as integer inequalities. Each passing top-level shard is therefore impossible, with no factorization of `A`, floating-point comparison, or acceptance of solver flags.

## 4. New verified-integer candidate census

| Root | Newly excluded nonoverlapping exponents | Count |
| --- | --- | ---: |
| 5 | 1626, 1636 | 2 |
| 17 | 708, 718, 726, 732, 738, 742, 750, 756, 760, 768, 772, 786, 796 | 13 |
| **Total** | | **15** |

The simpler cyclotomic Euler primorial test already excludes 34 shards, one of which overlaps the earlier finite quotient census. The strengthened DP excludes 15 *additional* shards. Thus the current candidate top-level census is

```
14 forbidden factors
+ 1382 exact sigma-divisor-size contradictions
+ 3 fully exhausted finite quotients
+ 33 new simple cyclotomic-Euler bounds
+ 15 new forbidden-exponent DP bounds
= 1447 candidate integer proof leaves / 3072.

Open top-level shard count = 1625.
```

## 5. Repository integration and validation

- [Exact integer DP checker](../Python/CyclotomicExponentDPClosure2400.py)
- [Regression and tampering tests](../Python/CyclotomicExponentDPClosureTests.py)
- [Independent verifier](../Python/IndependentVerifierV2.py): new root-only leaf reason `CYCLOTOMIC_FORBIDDEN_EXPONENT_DP`.
- [Direct proof generator](../Python/DirectRootClosures2400.py): selects the 13 independently recomputed positive cases.
- [3,072-shard audit](../Python/AuditDirectRoot2400.py): expects 1,447 independently accepted leaves, 1,625 open, and global `INCOMPLETE_FRONTIER`.

Reproduce from the repository root:

```bash
python3 -S -O Research/Session20261122/Python/CyclotomicExponentDPClosureTests.py
python3 -S -O Research/Session20261122/Python/DirectRootClosuresTests.py
python3 -S -O Research/Session20261122/Python/AuditDirectRoot2400.py
```

The current implementation performs no paid external model calls. It uses deterministic primality trial division only for the small primes `p`, `m`, and quotient-sieve primes. The full 3,072-shard theorem, deeper proof DAGs, and fixed-hardware 72-hour runtime acceptance remain open.
