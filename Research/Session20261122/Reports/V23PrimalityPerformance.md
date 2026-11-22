# V23: eliminating duplicate primality tests in the 2400 proof tree

Date: 2026-11-22. The production V21 source remains unchanged. Research source: `Sources/Cpp/ProofTreeV23.cpp`, derived from main SHA `90100f4447f9196835951fdb7e9dcdd3ab23723f`.

## Profiled bottleneck

The instrumented, unmodified V21 trial ran on GitHub Actions (2 OpenMP threads, fixed pinned factors and the 256-prefix LP tables):

https://github.com/stormwhip/PerfectNumbers/actions/runs/45012070442

At the 10-second mark in root-19 shard 0, summed threaded CPU timer readings were `fact=15.7194s`, `prime=15.6449s`, `db=0.00507s`, `lp=0.0189s`, `composite=3.3592s`. The fact timer *includes* the prime timer, so these totals must not be added. There were 84,801 fact-cache calls, 82,789 cache hits, and 3,722 primality test calls. Shard 100's readings were `prime=10.2617s`, `composite=7.10972s`, `lp=0.0759s`, `db=0.0516s`.

## Semantic-preserving improvement

V21 calls `mpz_probab_prime_p(rem,5)` to decide whether to trial-divide `rem`, then calls it again for classification, even if `rem` was not changed in the intervening trial-divide loop. V23 saves the first classification; it re-tests the residual *only if trial division actually changed it*. The new source accepts `OPN_PRIME_REPS=5` and `10` for bounded comparisons, defaulting to 10 for a stronger screening pass. This modification does not change exponent branching, LP cuts, data lookups, circular partition logic, or proof-tree results for matched inputs.

## Completed matched performance experiment

https://github.com/stormwhip/PerfectNumbers/actions/runs/45012354324

2 OpenMP threads, matched GitHub Actions hardware class, database, 256-prefix LP tables, and target exponent 2400. Each shard had a 12-second cap; only full `PROVEN` results establish end-to-end timing.

| Root19 shard | V21 baseline | V23 reps=5 | V23 reps=10 |
| --- | --- | --- | --- |
| 35 | 45,987 branches / 1.82285s | 45,987 / 1.33147s | 45,987 / 1.27435s |
| 130 | 2,230 / 0.068694s | 2,230 / 0.050745s | 2,230 / 0.051555s |
| 0 | TIMEOUT (10s: 104,886 visited) | TIMEOUT (10s: 151,121 visited) | TIMEOUT (10s: 148,882 visited) |
| 100 | TIMEOUT (10s: 354,128 visited) | TIMEOUT (10s: 429,694 visited) | TIMEOUT (10s: 429,646 visited) |

For completed shard 35, the 10-repetition implementation saved 30.09% elapsed time; shard 130 saved 24.95%. Both returned `PROVEN` with identical branch counts and zero failed roadblocks. V23 was also tested by `ProofCoreTestsV23.cpp`, whose inherited V21 core suite passed.

**Interpretation:** successful preliminary runtime gain on two *completed* shards; the other two only support partial throughput comparisons. Trials are single runs, and the complete 8-root workload and 72-hour feasibility remain unmeasured. Retaining 10 primality-test repetitions is reasonable for the experimental branch, but all proof-critical prime assertions ultimately require deterministic primality certification and independent checker validation.

## Next bottleneck

`refresh_composite_size_bound()` is the next dominant timer, especially root19 shard100. The current implementation scans every known branched/unbranched prime and every previously accepted residual when checking each composite factor. Investigate mathematically equivalent product-gcd screening, count actual gcd operations, and use completed matched shards to assess wall-time benefits. Keep experiments on research branches until validation and measured gains are established.
