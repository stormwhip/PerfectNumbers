# Final night: independently accepted progress

**Status: INCOMPLETE_FRONTIER.** Theorem sought: every odd perfect number exceeds 10^2400. This branch does not yet prove it. Baseline [1447d41b](https://github.com/stormwhip/PerfectNumbers/commit/1447d41b806f43ec5775e0cef7eaa7739ab67388), checked against remote main before work. The two original incidence maps are bound by Git object hashes in [Project](Project.py). New complete results are exact, not divisibility lifts.

|Measure|Baseline|Accepted overlay|
|---|---:|---:|
|Canonical shards closed|3004|3010|
|Shards open|68|62|
|Distinct exact keys open|78|72|
|Singleton shards open|60|54|

|Exact key|Singleton closed|Independent full-dependency replay|
|---|---|---|
|(19,58)|P19_I00015|[384.095 s](Audit/TenReceipt.md)|
|(31,310)|P31_I00062|[63.005 s](Audit/ThirtyOneReceipt.md)|
|(13,262)|P13_I00055|[220.073 s](Audit/ThirteenReceipt.md)|
|(13,310)|P13_I00063|[440.350 s](Audit/NextReceipt.md)|
|(31,16)|P31_I00005|[259.891 s](AuditNext/Full31Receipt.md)|
|(31,352)|P31_I00069|[240.628 s](Audit/MoreReceipt.md)|

The first key has no preceding root; the 31 keys assume 19,7,11 absent and the 13 keys assume 19,7,11,31 absent. The [independent frozen projection](Audit/BatchOne.md) checks disjoint incidence deletion for the first five; the sixth is checked against both maps in its own receipt. For all other domains see the [conditional ledger](Results.json): a higher-level closure can supersede older partial rows, which are not counted again.

## Known–to prove

Assume positive odd N≤10^2400, sigma(N)=2N. Exclude the first dividing prime in order (19,7,11,31,13,3,5,17) at each of the following exact exponents. Earlier roots are forbidden. Each row is a *projection*: the actual shard membership is in [OpenFrontier](OpenFrontier.json).

|Root|Open shards|Remaining exact exponents|
|---:|---:|---|
|19|22|2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 30, 32, 46, 48, 82, 222, 276, 280, 282, 292, 312, 330, 358, 372, 420, 432, 618|
|7|16|4, 6, 10, 12, 16, 18, 24, 34, 36, 48, 430, 438, 456, 486, 600, 738, 808, 882, 906|
|11|9|4, 6, 12, 16, 18, 48, 358, 396, 456, 462|
|31|6|2, 6, 240, 268, 456, 466|
|13|6|2, 4, 6, 8, 388, 612, 618|
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

The projection alone is **not** a proof. Key-specific cold runs listed above include their historical dependencies. The baseline five-command regression passed; the Night2400 run took 3807.369 s. No full-repository historical cold replay or 72-hour global benchmark is claimed. [Research log](ResearchLog.md) · [draft PR](https://github.com/stormwhip/PerfectNumbers/pull/10).
