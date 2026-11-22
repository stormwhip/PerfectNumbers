# Sigma pilot and persistent frontier

> **进度标注（2026-11-22）**：本文记录对应阶段的数学推导、实验数据和当时的搜索状态。最新研究进度、独立验证器 V2、可恢复前沿及全量未闭合项目，统一见 [CurrentStatus2400.md](../../../Documentation/CurrentStatus2400.md)。本文历史计时和程序 `PROVEN` 均不作为 `10^2400` 完整证明。


## Implemented experiments

The [sigma pilot branch](https://github.com/stormwhip/PerfectNumbers/commit/e56e76911a9427ec9e4785e23044878620756d8d) compares four modes of the same compiled V21. G0 preserves the two-test path. G1 reuses the probable-prime result unless the remainder changes during trial division. G2 performs a before-factorization v2 test and an exact-branch valuation quota test when the required modulus fits an unsigned long. G3 combines G1 and G2. All modes use the same original root order, data and legacy roadblock policy. Small-prime trial division was not reordered. Database prechecking, shared caching and state-LP early pruning are separate experiments.

For a branch at source prime \(p\), write \(m=d+1\). If \(p\equiv1\bmod q\) for an odd prime \(q\), then \(v_q(\sigma(p^d))=v_q(m)\). If \(p\not\equiv0,1\bmod q\), divisibility by \(q^k\) is equivalent to \(p^m\equiv1\bmod q^k\). If \(q\mid p\), the valuation is zero. A standard branch still guarantees \(\sigma(p^d)\mid\sigma(p^e)\), so the new source contribution can be added to already recorded contributions from distinct source primes. An upper-quota prune requires an exact exponent of the target prime \(q\). The implementation skips an out-of-range modulus. The portable C++ test checked 9,680 exact divisibility cases against explicit integer geometric sums.

The v2 formula is exact for odd \(p\), but ordinary V21 options use even \(d\), or exact \(d=1\) with \(p\equiv1\bmod4\). The v2 rule is mainly a consistency check for those options.

Treating residual size and abundance as external to a conditional LP requires a fresh proof that every actual completion maps to a feasible point of the remaining model. In particular, a base LP row cannot keep requiring an explicit variable that no longer represents an external residual factor. Merely checking disjointness of the currently listed primes does not verify every implication row.

## Matched pilot results

[GitHub Actions run and raw logs](https://github.com/stormwhip/PerfectNumbers/actions/runs/45031791682). Same Linux runner and two OpenMP threads, nine targeted prefix tables from the original root order. The searchable target was 2400. One run per cell.

| Shard | G0 wall (s) | G1 wall (s) | G2 wall (s) | G3 wall (s) |
| --- | ---: | ---: | ---: | ---: |
| 35 | 2.345 | 1.575 | 2.140 | 1.631 |
| 130 | 0.145 | 0.125 | 0.139 | 0.122 |

Both controls finished with the program's PROVEN status, zero failed roadblocks and identical branch counts across modes (45,987 and 2,230).

| Shard | G0 nodes at ~10 s | G1 | G2 | G3 |
| --- | ---: | ---: | ---: | ---: |
| 0 | 86,111 | 122,687 | 85,210 | 118,909 |
| 100 | 285,634 | 366,794 | 279,075 | 364,957 |

All eight hard-shard runs timed out at 20 s. On shard 0, G0 and G1 had 3,714 and 4,286 probable-prime calls at ~10 s, but the G1 ratio per cache miss was 1.31 versus 1.85 and it visited more nodes. On shard 100 the same-time counts were 47,427 versus 35,379. The precheck hit neither v2 nor quota contradictions in the logged snapshots of the measured cases. The timeout logs do not exhaust the search. These measurements support prioritizing G1 for subsequent experiments, while leaving the optional early precheck off by default. They do not estimate a completed hard-shard runtime.

## Frontier prototype

[FrontierLedger.py](../Python/FrontierLedger.py) records a path-based task identity, lease attempt token and expiry, ordered child states as part of the durable split, and a digest for a candidate result. The split state and every inserted child are committed together. A stale worker's attempt cannot renew, split or finish a reclaimed task. Reopening after a split recovers its children. The test also checks rollback of an attempted split that fails after its first child insertion.

The ledger does not verify a caller-supplied child list or an attached proof. `RESULT` is an opaque candidate, separate from independently accepted evidence. V21 task export/import and an independent closure verifier are required before scheduling real trees. A fast resume format must retain the order of residuals or record their stronger-bound evidence per residual. V21 currently indexes a certified prefix by position, and its greedy residual-size selection is order-dependent. Sorting residuals while retaining this prefix count can misassign a stronger abundance bound. The V21 circular child order tries the fixed circular order first, then other primes in ascending order; a resumed edge must carry the exact prior exclusions for its chosen ordering.

## 72-hour scheduling bound

With independent jobs all ready at time zero, measured durations on identical slots, and a work-conserving list schedule, any last finishing job \(k\) starts no later than \((W-t_k)/J\), because all \(J\) slots were busy before it started. Thus \(\max(\max_i t_i,W/J)\) is a lower bound and \(W/J+(1-1/J)\max_i t_i\) is an upper bound under those assumptions. A split that becomes available later or shares variable resources needs a separate schedule model. A censored task duration or bootstrap estimate supplies no deterministic completion guarantee.
