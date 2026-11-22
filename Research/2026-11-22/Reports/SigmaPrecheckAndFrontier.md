# Sigma pilot and persistent frontier

## Implemented experiments

The [sigma pilot branch](https://github.com/stormwhip/PerfectNumbers/commit/e56e76911a9427ec9e4785e23044878620756d8d) compares four modes of the same compiled V21. G0 preserves the two-test path. G1 reuses the probable-prime result unless the remainder changes during trial division. G2 performs a before-factorization v2 test and an exact-branch valuation quota test when the required modulus fits an unsigned long. G3 combines G1 and G2. All modes use the same original root order, data and legacy roadblock policy. Small-prime trial division was not reordered. Database prechecking, shared caching and state-LP early pruning are separate experiments.

For a branch at source prime \(p\), write \(m=d+1\). If \(p\equiv1\bmod q\) for an odd prime \(q\), then \(v_q(\sigma(p^d))=v_q(m)\). If \(p\not\equiv0,1\bmod q\), divisibility by \(q^k\) is equivalent to \(p^m\equiv1\bmod q^k\). If \(q\mid p\), the valuation is zero. A standard branch still guarantees \(\sigma(p^d)\mid\sigma(p^e)\), so the new source contribution can be added to already recorded contributions from distinct source primes. An upper-quota prune requires an exact exponent of the target prime \(q\). The implementation skips an out-of-range modulus. The portable C++ test checked 9,680 exact divisibility cases against explicit integer geometric sums.

The v2 formula is exact for odd \(p\), but ordinary V21 options use even \(d\), or exact \(d=1\) with \(p\equiv1\bmod4\). The v2 rule is mainly a consistency check for those options.

Treating residual size and abundance as external to a conditional LP requires a fresh proof that every actual completion maps to a feasible point of the remaining model. In particular, a base LP row cannot keep requiring an explicit variable that no longer represents an external residual factor. Merely checking disjointness of the currently listed primes does not verify every implication row.

## Frontier prototype

[FrontierLedger.py](../Python/FrontierLedger.py) records a path-based task identity, lease attempt token and expiry, ordered child states as part of the durable split, and a digest for a candidate result. The split state and every inserted child are committed together. A stale worker's attempt cannot renew, split or finish a reclaimed task. Reopening after a split recovers its children. The test also checks rollback of an attempted split that fails after its first child insertion.

The ledger does not verify a caller-supplied child list or an attached proof. \`RESULT\` is an opaque candidate, separate from independently accepted evidence. V21 task export/import and an independent closure verifier are required before scheduling real trees. A fast resume format must retain the order of residuals or record their stronger-bound evidence per residual. V21 currently indexes a certified prefix by position, and its greedy residual-size selection is order-dependent. Sorting residuals while retaining this prefix count can misassign a stronger abundance bound. The V21 circular child order tries the fixed circular order first, then other primes in ascending order; a resumed edge must carry the exact prior exclusions for its chosen ordering.

## 72-hour scheduling bound

With independent jobs all ready at time zero, measured durations on identical slots, and a work-conserving list schedule, any last finishing job \(k\) starts no later than \((W-t_k)/J\), because all \(J\) slots were busy before it started. Thus \(\max(\max_i t_i,W/J)\) is a lower bound and \(W/J+(1-1/J)\max_i t_i\) is an upper bound under those assumptions. A split that becomes available later or shares variable resources needs a separate schedule model. A censored task duration or bootstrap estimate supplies no deterministic completion guarantee.
