# Sprint result: current exact frontier

On the research branch, **2988/3,072** canonical shards are closed, **84** are open, with **94 distinct unresolved (root, exponent) pairs**. 76 open shards contain just one remaining exponent. The global theorem is not established.

Relative to [main at 2b53c830](https://github.com/stormwhip/PerfectNumbers/commit/2b53c830dd903b460a315df04fa3a4a410fb8357): 16 newly excluded actuals; 14 newly closed shards. [Full ledger, including every shard’s exact remaining membership](Delta.json).

| Canonical root | Closed / total | Open | New exact exclusions | Remaining exact exponents |
|---:|---:|---:|---|---|
|19|258 / 287|29|268, 348, 352, 448, 478|2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 30, 32, 46, 48, 58, 82, 162, 222, 232, 238, 270, 276, 280, 282, 292, 312, 316, 330, 358, 372, 420, 432, 502, 618|
|7|389 / 412|23|46, 70, 90, 168|4, 6, 10, 12, 16, 18, 24, 28, 34, 36, 48, 130, 420, 430, 438, 456, 486, 490, 586, 600, 682, 732, 738, 808, 882, 906|
|11|332 / 341|9|10, 42, 108|4, 6, 12, 16, 18, 48, 358, 396, 456, 462|
|31|244 / 253|9|348, 388|2, 6, 16, 240, 268, 310, 352, 456, 466|
|13|314 / 325|11|—|2, 4, 6, 8, 262, 310, 372, 388, 456, 508, 612, 618|
|3|673 / 676|3|970, 990|6, 12, 856|
|5|481 / 481|0|—|—|
|17|297 / 297|0|—|—|

**Newly closed IDs:** `P19_I00055`, `P19_I00068`, `P19_I00069`, `P19_I00085`, `P19_I00090`, `P7_I00014`, `P7_I00019`, `P11_I00003`, `P11_I00012`, `P11_I00027`, `P31_I00068`, `P31_I00075`, `P3_I00165`, `P3_I00168`.

The eight-root coprime terminal is separate; its independently replayed lower log is 4183.209493. Root 5 and root 17 were fully closed before this sprint. Conditional supports and fixed-pivot fibers do not enter the counts above.

**Verification scope.** New complete keys were verified per packet, using exact integer/rational arithmetic or outward-directed logarithm enclosures. Some speculative finite-head trees failed and were not used; only replacements passing both integer forest calculations were admitted. The historical 2,974 closures are inherited from the pinned base, not 2,974 fresh arithmetic reruns. The overlay verifier rechecks the new proofs then recomputes all shard memberships. No single full-history cold run is claimed. For 990 the new 64+98 subdomains and native range were separately replayed; historical no-five/valuation-cap results carry their original dependencies.

[Proof and verification instructions](Proof.md) · [Multi-prime pricing theorem](JointValuation.md) · [Complete 990 proof](Proof990.md) · [PR #7](https://github.com/stormwhip/PerfectNumbers/pull/7).

**Next target:** canonical root 3, exponent 12. Only a handful of exact first-pivot valuations at 797161 remain; split these before extending factor chains. The numerically smallest remaining root exponent is 2 (at several roots), not necessarily the cheapest proof. `P7_I00005` now needs only exponent 12 at root 7. For a new price leaf, close every sibling and the monotone exponent tail before registering its parent.
