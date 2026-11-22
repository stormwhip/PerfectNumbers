# V24: product-GCD composite residual accounting

Date: 2026-11-22. Research branch `research/exact-sigma-size-v22`. Source `Sources/Cpp/ProofTreeV24.cpp`, diff based on V23. Production V21 remains untouched.

## Exact equivalence lemma

The old `refresh_composite_size_bound` scans known branched prime factors `p`, unbranched prime factors `q`, and every previously accepted composite residual `d` for each candidate residual `c`. A residual is accepted if no `p|c`, no `q|c`, and each `gcd(c,d)=1`. Every `p,q` in a genuine proof-tree state is a prime. Therefore `c` is accepted if and only if

\[
\gcd\left(c,\left(\prod_{p\in B\cup U}p\right)\left(\prod_{d\in C_\mathrm{accepted}}d\right)\right)=1.
\]

V24 builds this product and tests one GMP gcd per candidate, multiplying the product by each accepted residual. It preserves the same accepted residual order and the same addition order for `log_size_comp`.

`ProofCoreTestsV24.cpp` includes the inherited V21/V23 regression tests and 4,000 deterministic randomized differential tests comparing the V24 computed `log_size_comp` against an independent copy of the original V21 logic; all passed in the workflow below.

## Pinned bounded matched experiment

https://github.com/stormwhip/PerfectNumbers/actions/runs/45012698021

Target 2400, root 19, indices 0,35,100,130, identical database hash and 256-prefix LP files; 2 OpenMP threads, 12-second cap per variant. Versions: V21 baseline, V23 cached-primality variant, V24 product-gcd variant. V23 and V24 use ten primality-test reps; V21 uses its original five reps (two calls for some residuals). Exact full PROVEN results:

| Shard | V21 | V23 | V24 |
| --- | --- | --- | --- |
| 35 | 45,987 branches / 2.14638s | 45,987 / 1.53477s | 45,987 / 1.75235s |
| 130 | 2,230 / 0.084345s | 2,230 / 0.063108s | 2,230 / 0.061948s |
| 0 | TIMEOUT | TIMEOUT | TIMEOUT |
| 100 | TIMEOUT | TIMEOUT | TIMEOUT |

At the 10-second mark, visited branches (not completed time) for shard 0 were V21 87,159, V23 123,524, V24 129,160. For shard 100 they were 284,349, 365,732, 374,448. V24 logs show 264,794 gcd candidate calls / 263,654 accepted on shard 35, and 12,853 calls / 12,849 accepted on shard 130. Its large acceptance rate suggests some new gcd checks add significant overhead even when nothing is rejected.

**Finding:** the product-gcd change is mathematically equivalent (under the prime-factor invariant) and passes all synthetic differential tests, but has no demonstrated *overall* improvement over V23: shard 35 became 14.2% slower than V23, shard 130 approximately 1.8% faster, and both difficult shards remained incomplete. Do not promote V24 into the production runner.

The next performance research should prioritize reducing V21/V23 sigma residual primality/factorization cost (V23 success) and stronger cuts applied before deep factorization. The 72-hour target still requires a complete root/task runtime census and proof-level independent arithmetic/LP auditing.
