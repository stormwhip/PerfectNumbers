# V22 research — exact sigma-divisibility size cuts

Date: 2026-11-22. Base commit: `90100f4447f9196835951fdb7e9dcdd3ab23723f`.
Research branch: `research/exact-sigma-size-v22`. Production V21, the WSL 72-hour runner, and all input files remain unchanged.

## Proven invariant

Let `N` be an odd perfect number, and consider a factor-chain branch specifying the minimal exponent `a` of an odd prime `p`. An exact branch means `p^a || N`. An inexact branch represents an exponent `e>=a` with `a+1 | e+1`. The latter implies

\[
\sigma(p^a)=\frac{p^{a+1}-1}{p-1}\ \Bigm|\ \sigma(p^e)\ \Bigm|\ 2N.
\]

Since `N` is odd, the odd part `s(p,a)=sigma(p^a)/2^{nu_2(sigma(p^a))}` divides `N`, and `p^a | N`. Accordingly

\[
A_k=\prod_{i=1}^{k}p_i^{a_i},\qquad
B_k=\prod_{i=1}^{k}s(p_i,a_i),\qquad
D_k=\operatorname{lcm}(A_k,B_k).
\]
The products range over *distinct* branched primes. Because \(\sigma(N)=\prod_i\sigma(p_i^{e_i})=2N\), we have both \(A_k\mid N\) and \(B_k\mid N\), including repeated prime factors across different sigma terms. Consequently \(D_k\mid N\). The branch closes if `D_k > 10^B` for a target `N<=10^B`.

This cut needs no factorization, primality inference, approximate logarithm, or Ochem database entry. In V22, only the decision `D_k > 10^B` closes a branch; this is exact GMP integer comparison. Summing multiplicities in the product `B_k` is stronger than taking the LCM over individual sigma terms.

## Cheap even-power screen

For even `a`, `sigma(p^a)` is odd and coprime with `p`. Therefore

\[
N \ge p^a\sigma(p^a)>p^{2a}.
\]

For `B=2400`, the exact condition `p^a > 10^{1200}` closes that branch *before* sigma factorization. For a general integer target `B`, the experimental code conservatively compares against `10^{ceil(B/2)}`.

A floating-log condition decides whether the exact computation is worth trying; only the exact GMP comparison determines whether a branch closes. No floating-point error can cause an unsafe cut.

## Enumerated root-option screening

For the eight root primes in V21 order, Python exact-integer enumeration of their 2400 exponent lists gives:

| prime | V21 top-level options | options not rejected by even-power test | directly rejected |
| --- | ---: | ---: | ---: |
| 19 | 287 | 158 | 129 |
| 7 | 412 | 223 | 189 |
| 11 | 341 | 190 | 151 |
| 31 | 253 | 138 | 115 |
| 13 | 325 | 180 | 145 |
| 3 | 676 | 370 | 306 |
| 5 | 481 | 267 | 214 |
| 17 | 297 | 164 | 133 |
| **total** | **3072** | **1690** | **1382 (44.99%)** |

V22 keeps the original `get_exponents` branch list and rejects impossible branches during processing. This avoids changing the existing exponent-covering lemma and allows direct ablation against V21.

**Performance scope:** most of the 123 one-second-timeout root-19 shards from census `45005912683` are low exponents, below this particular threshold. The 44.99% is an option-count reduction, *not* a measured 44.99% runtime reduction. The cumulative LCM cut is intended to test deeper states.

## Experimental integration

- `Sources/Cpp/ExactSigmaDivisor.hpp`: isolated two exact-integer rules.
- `Sources/Cpp/ProofTreeV22.cpp`: opt-in ablation with the same LP, root-order and factor-chain logic as V21.
- `Sources/Cpp/ProofCoreTestsV22.cpp`: inherited regressions and exact-integer cut tests.
- `OPN_EXACT_DIVISOR_MODE=0`: V21-equivalent code path.
- `OPN_EXACT_DIVISOR_MODE=1`: add exact even-power check.
- `OPN_EXACT_DIVISOR_MODE=2`: add cumulative sigma-divisor LCM cut (default in V22).
- `OPN_EXACT_DIVISOR_MODE=3`: defer product-LCM computation until baseline size/abundance checks have passed and a cheap log(A*B) prefilter predicts that an exact contradiction may be possible. Reconstruct both products from branched prime powers only on demand.

Local primitive test passed (GMP/C++17; `3^2` forces `117`, adding `7^2` forces `108927`). A new regression uses `3^2` and `61^2`: their sigma values share factor 13, and multiplying sigma contributions yields a mandatory divisor `548985177`, exactly 13 times the naive individual-LCM result `42229629`. Full V22 regression runs through `QualityChecks.yml` on this research branch.

## Remaining performance experiment

Use the same pinned factor database, 256-prefix LP tables, cutoff product, hardware, thread count, root order and selected difficult shards for all three modes. Record completed shards, total branches, CPU time, peak resident memory, and `EXACT_DIVISOR_STATS` counters. Prefer completed 10–30-second shards over partial node-rate comparisons. A claimed wall-time gain requires a completed matched test.

Do not replace the V21 72-hour scheduler until this matched test passes. Mathematical release still requires independent validation of the original LP and all other tree cuts.

## Initial bounded matched benchmark (completed)

Run: https://github.com/stormwhip/PerfectNumbers/actions/runs/45011182741. Four root-19 exponent shards, 2 threads, 12-second cap per test, same checksum-pinned inputs and LP tables.

| Shard | V21 baseline | V22 mode 1 even-power | V22 mode 2 eager product-LCM |
| --- | --- | --- | --- |
| 35 | PROVEN, 45,987 branches, 1.44718s | PROVEN, 45,987 branches, 1.48195s | PROVEN, 45,713 branches, 2.06066s |
| 130 | PROVEN, 2,230 branches, 0.06153s | PROVEN, 2,230 branches, 0.06205s | PROVEN, 2,230 branches, 0.08546s |
| 0 | TIMEOUT 12s | TIMEOUT 12s | TIMEOUT 12s |
| 100 | TIMEOUT 12s | TIMEOUT 12s | TIMEOUT 12s |

At shard 100's 10-second progress mark, V21 had visited 376,475 branches while eager mode 2 had visited 245,666, with 138,987 cumulative LCM cuts. Shard 35 had 25,722 eager LCM cuts and removed only 274 visited branches overall. Thus **eager mode 2 does not show an end-to-end performance gain**; it is about 42% slower in the first completed shard. Partial visited-node counts are not speed measurements.

The exact arithmetic lemma remains valid. Mode 3 tests whether postponing GMP product/LCM work until a branch survives cheap contradictions and passes an optional `log(A*B)` screening gate is a better implementation. Screening may miss a valid optional cut but cannot make a false cut, since final pruning uses GMP exact comparison.

## Deferred mode-3 matched result (completed)

Run: https://github.com/stormwhip/PerfectNumbers/actions/runs/45011614919. Same four root-19 shards, 2 threads, pinned database and LP tables, 12-second cap per test.

| Shard | V21 baseline | V22 eager mode 2 | V22 deferred mode 3 |
| --- | --- | --- | --- |
| 35 | PROVEN 45,987 branches / 2.01519s | PROVEN 45,713 / 2.72243s | PROVEN 45,713 / 2.92290s |
| 130 | PROVEN 2,230 / 0.08636s | PROVEN 2,230 / 0.11653s | PROVEN 2,230 / 0.11917s |
| 0 | TIMEOUT 12s | TIMEOUT 12s | TIMEOUT 12s |
| 100 | TIMEOUT 12s | TIMEOUT 12s | TIMEOUT 12s |

Deferred mode 3 rebuilt exact products 7,171 times for shard 35 and 18,096 times by the 10-second progress mark for shard 100. For shard 35 the total number of nodes only decreased by 274, while runtime grew by ~45%. Rebuilding exact products late in the tree remains more expensive than the work it saves.

**Decision:** the exact divisor theorem and regression coverage are retained; both product-LCM runtime variants are experimental and must not be merged into the production V21 72-hour runner. Further priority is diagnostic profiling of V21 hard-root DFS, followed by earlier structural/conditional LP cuts rather than additional late arithmetic cuts.
