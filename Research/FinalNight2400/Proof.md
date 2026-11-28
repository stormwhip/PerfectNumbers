# Final night: independently accepted progress

**Status: INCOMPLETE_FRONTIER.** Theorem sought: every odd perfect number exceeds 10^2400. This branch does not yet prove it. Baseline [1447d41b](https://github.com/stormwhip/PerfectNumbers/commit/1447d41b806f43ec5775e0cef7eaa7739ab67388), checked against remote main before work. The two original incidence maps are bound by Git object hashes in [Project](Project.py). New complete results are exact, not divisibility lifts.

|Measure|Baseline|Accepted overlay|
|---|---:|---:|
|Canonical shards closed|3004|3029|
|Shards open|68|43|
|Distinct exact keys open|78|53|
|Singleton shards open|60|35|

|Exact key|Singleton closed|Independent full-dependency replay|
|---|---|---|
|(11,396)|P11_I00076|[1920.787 s](TenNext/Full396Review.md)|
|(11,456)|P11_I00086|[779.101 s](ShortSeven/Review456.md)|
|(11,12)|P11_I00004|[2262.747 s](LowSeven/ReviewSmallEleven.md)|
|(11,358)|P11_I00070|[252.947 s](AuditNext/Full358.md)|
|(11,462)|P11_I00088|[254.255 s](AuditNext/Full462.md)|
|(19,312)|P19_I00063|[144.258 s](AuditNext/Full312.md)|
|(7,882)|P7_I00152|[816.964 s](ShortSeven/Review882.md)|
|(7,36)|P7_I00011|[2034.900 s](AuditNext/Full36.md)|
|(7,430)|P7_I00082|[1415.677 s](AuditNext/Full430.md)|
|(19,372)|P19_I00072|[8.309 s](AuditNext/Full372.md)|
|(19,420)|P19_I00080|[1570.141 s](AuditNext/Full420.md)|
|(19,618)|P19_I00112|[2458.340 s](AuditNext/Full618.md)|
|(19,330)|P19_I00065|[307.111 s](AuditNext/Full330.md)|
|(19,280)|P19_I00058|[4569.877 s](AuditNext/Full280.md)|
|(19,82)|P19_I00021|[357.584 s](AuditNext/Full82.md)|
|(19,282)|P19_I00059|[3327.483 s](AuditNext/Full282.md)|
|(19,292)|P19_I00060|[1368.139 s](Ten276/Review292.md)|
|(19,58)|P19_I00015|[384.095 s](Audit/TenReceipt.md)|
|(31,310)|P31_I00062|[63.005 s](Audit/ThirtyOneReceipt.md)|
|(13,262)|P13_I00055|[220.073 s](Audit/ThirteenReceipt.md)|
|(13,388)|P13_I00076|[307.375 s](AuditNext/Full388.md)|
|(13,310)|P13_I00063|[440.350 s](Audit/NextReceipt.md)|
|(31,240)|P31_I00051|[1349.598 s](AuditNext/Full240.md)|
|(31,16)|P31_I00005|[259.891 s](AuditNext/Full31Receipt.md)|
|(31,352)|P31_I00069|[240.628 s](Audit/MoreReceipt.md)|

The 19 key has no preceding root; the 11 keys assume 19 and 7 absent; the 31 keys assume 19,7,11 absent and the 13 keys assume 19,7,11,31 absent. The [independent frozen projection](Audit/BatchOne.md) checks disjoint incidence deletion for the first five; all later additions are checked against both maps in their own receipts. For all other domains see the [conditional ledger](Results.json): a higher-level closure can supersede older partial rows, which are not counted again.

## Known–to prove

Assume positive odd N≤10^2400, sigma(N)=2N. Exclude the first dividing prime in order (19,7,11,31,13,3,5,17) at each of the following exact exponents. Earlier roots are forbidden. Each row is a *projection*: the actual shard membership is in [OpenFrontier](OpenFrontier.json).

|Root|Open shards|Remaining exact exponents|
|---:|---:|---|
|19|13|2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 30, 32, 46, 48, 222, 276, 358, 432|
|7|13|4, 6, 10, 12, 16, 18, 24, 34, 48, 438, 456, 486, 600, 738, 808, 906|
|11|4|4, 6, 16, 18, 48|
|31|5|2, 6, 268, 456, 466|
|13|5|2, 4, 6, 8, 612, 618|
|3|3|6, 12, 856|
|5|0|—|
|17|0|—|

Roots 5,17 and the no-root case remain closed on historical evidence. For historical detailed conditional regions consult [Night2400](../Night2400/README.md) and [GeminiFrontier](../GeminiFrontier/Review.md); apply verified new cuts from the ledger to their stated assumptions only. Decision criterion: for each old shard subtract only VERIFIED_FULL keys and test whether its remainder is empty.

## What changed mathematically

* The [square-base Euler identity and cubic pricing](Root7Joint/Proof.md) treats any exponent 4k+1, retaining q+1 separately and using the odd-length geometric sum in q², not sigma of a fictitious prime. Joint orders, LTE increments and all candidate representatives are independently checkable. [Coprime effective lengths](Dual/Proof.md) permit asymmetric prices when two targets can share a source.
* The [hard 3^12 path](Three/ProofHard66.md) cancels an unknown incoming supply between two inequalities for the same external Euler emitter. The strict bound is on **N²**, so there is no duplicated mass lower bound on N. Analogous cancellation, combined with complete critical cubic losses and a gcd-based budget, closes the [last (13,262) fiber](Others/Proof13.md).
* [Four support cuts](Support/Proof.md) do not assume any root exponent: if 3,5,19,31 are absent then 53 or 59 occurs, and absence of 53 forces at least two of 41,73,137. [Two compulsory pivots at (19,358)](Triple/Proof.md) force all residual t-supply through the linear Euler factor, without factoring the anonymous root block.

## Replay

Run the five [historical entries and receipts](Audit/Baseline.md), then from a canonical-byte checkout with stock Python assertions enabled:

~~~sh
python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Verify.py
python -I -S -B Research/FinalNight2400/Project.py
~~~

The projection alone is **not** a proof. Key-specific cold runs listed above include their historical dependencies. The baseline five-command regression passed; the Night2400 run took 3807.369 s. No full-repository historical cold replay or 72-hour global benchmark is claimed. [Validation status, including partial replays](Validation.md) · [Chinese final report](Report.md) · [Research log](ResearchLog.md) · [draft PR](https://github.com/stormwhip/PerfectNumbers/pull/10).
