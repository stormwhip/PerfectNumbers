# Cyclotomic–Euler Primorial Certificates for `10^2400`

**Research date:** 2026-11-23. **Production roots:** `(19,7,11,31,13,3,5,17)`.
**Global theorem:** `INCOMPLETE_FRONTIER`. This document proves one additional *top-level root-closure rule*; the full 3,072-task proof and 72-hour target remain incomplete.

## 1. Precise statement

Let `p` be an odd root prime, `d` an even non-exact exponent representative, and `m=d+1` an odd prime with `m>p`. Suppose an odd perfect number `N<=B=10^2400` belongs to the root class excluding the earlier roots `F` and has actual exponent `e>=d` with `m|(e+1)`.

Write

```
A = sigma(p^d) = Phi_m(p) = (p^m-1)/(p-1)  (odd)
P = p^d * A
R = floor(B/P)
N = P*Q,       1 <= Q <= R,  Q odd.
```

The identity `sigma(p^d)|sigma(p^e)|2N` and `gcd(p,A)=1` prove `P|N`. If `P>B`, the older `SIGMA_DIVISOR_SIZE` leaf already closes the task. Here `P<=B`.

For any prime `q|A`, the prime `q=m` is impossible because `m>p` and `Phi_m(p)=1 (mod m)`. Hence `ord_q(p)=m`, and every odd `q|A` satisfies `q=1 (mod 2m)`. For the distinct prime factors `q_1<...<q_t` of `A`, it follows that

```
q_i >= 2mi+1,
t <= T = floor(log_(2m+1)(A)).
```

All logarithmic-looking bounds are evaluated by *integer division*. Put `C=1+ceil(log_2 T)` for `T>=1`. A dyadic harmonic bound gives

```
sigma(A)/A < product_(i=1)^t [1+1/(2mi)]
             <= exp(H_T/(2m))
             <= exp(C/(2m))
             <= 2m/(2m-C),                  provided C<2m.
```

The final comparison is rational, so no floating point is needed.

## 2. Euler-restricted primorial and shared size budget

Let `L=2m+1`. Among the prime divisors of `Q` smaller than `L`, discard the root `p` and the prohibited primes `F`. List all remaining possible small primes as

```
r_1 < r_2 < ... < L,  with r_i not in F union {p}.
```

Every such prime is coprime to `pA`. Euler's theorem implies that at most one of these primes occurs to an odd exponent in `N`; each other small prime has exponent at least two. Thus, if exactly `k>=1` distinct small primes occur,

```
Q >= M_k = (r_1 r_2 ... r_k)^2/r_k.
```

Set `M_0=1`. The chosen small prime divisors contribute to `sigma(Q)/Q` at most `D_k=product_(i=1)^k r_i/(r_i-1)`, where `D_0=1`.

The remaining prime divisors of `Q` (except possible copies of the root `p`) are at least `L`. There are at most

```
v_k = floor(log_L(floor(R/M_k)))
```

distinct such primes. They contribute a multiplicative factor of at most `(L/(L-1))^v_k` to abundance.

A possible `p` factor in `Q` is absorbed into the exact `p`-adic component of `N`, whose abundance is always less than `p/(p-1)`.

Consequently every admissible `N` satisfies, for the actual number `k` of small distinct prime factors,

```
sigma(N)/N
  < [p/(p-1)] * [2m/(2m-C)] * D_k * [L/(L-1)]^v_k.
```

The checker examines **all** `k` with `M_k<=R` and checks the following *exact integer inequality*:

```
p*(2m)*(product_i r_i)*L^v_k
    < 2*(p-1)*(2m-C)*(product_i(r_i-1))*(L-1)^v_k.
```

If every inequality holds, then `sigma(N)/N<2`; the root shard is impossible. Notice that `M_k` and `v_k` jointly use the same quotient budget `R`. No factorization of `A`, heuristic prime test, LP approximation, or search completion label enters this rule.

## 3. Exact census on the unchanged root order

The exhaustive candidate scan and independent integer implementation found **34** non-size/non-forbidden top-level branches passing the criterion.

| Root | Exponent representatives | Count |
| --- | --- | ---: |
| 11 | 1152 | 1 |
| 5 | 1656, 1662, 1666, 1668, 1692, 1696, 1698, 1708 | 8 |
| 17 | 808, 810, 820, 822, 826, 828, 838, 852, 856, 858, 862, 876, 880, 882, 886, 906, 910, 918, 928, 936, 940, 946, 952, 966, 970 | 25 |
| **Total** | | **34** |

The `(11,1152)` task already has a `FINITE_QUOTIENT_CYCLOTOMIC` leaf in the previously integrated set of three. With priority `FORBIDDEN_FACTOR` > `SIGMA_DIVISOR_SIZE` > `FINITE_QUOTIENT_CYCLOTOMIC` > `CYCLOTOMIC_EULER_PRIMORIAL`, **33 new nonoverlapping proof leaves** are added.

```
14 forbidden factors + 1382 sigma-size + 3 finite quotients
+ 33 cyclotomic Euler primorial = 1432 candidate verified root leaves
Remaining top-level root shards: 3072-1432 = 1640.
```

The new one-node LEAF rule `CYCLOTOMIC_EULER_PRIMORIAL` is computed anew from the externally fixed root state in `IndependentVerifierV2.py`. Tampered source exponents are rejected. The authoritative complete audit is still pending a fresh run on the revised repository source.

## 4. Reproduction and integration

- [Bound and deterministic certificate checker](../Python/CyclotomicPrimorialClosure2400.py)
- [Regression and forged-witness checks](../Python/CyclotomicPrimorialClosureTests.py)
- [Independent leaf verification](../Python/IndependentVerifierV2.py)
- [Canonical direct-root generator](../Python/DirectRootClosures2400.py)
- [3,072-shard top-level audit](../Python/AuditDirectRoot2400.py)

From repository root:

```bash
python3 -S -O Research/Session20261122/Python/CyclotomicPrimorialClosureTests.py
python3 -S -O Research/Session20261122/Python/DirectRootClosuresTests.py
python3 -S -O Research/Session20261122/Python/AuditDirectRoot2400.py
```

These certificates remove some extreme high-exponent root tasks. They do not yet establish total search runtime, completeness of deeper V21 proof DAGs, or the unconditional `10^2400` theorem.
