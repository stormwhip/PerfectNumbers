# Reproducing the canonical union

The ledger counts distinct `(root, actual exponent)` pairs first and then closes a canonical shard only if **all** its remaining actuals have been removed. Shards overlap: neither packet counts nor group-local shard totals are additive. The comparison point is commit `6732a1a894817457a1bc1b88b7d214ac4d6c9872` (406 open shards, 511 distinct actuals, 582 shard/actual incidences). The release does not prove the full bound.

From a clean checkout at the release commit, use a standard Python 3.11 interpreter with assertions enabled:

```sh
python -I -S -B -X int_max_str_digits=0 Research/Midday/CheckLedger.py --workers 4 --check Research/Midday/Delta.json
python -I -S -B -X int_max_str_digits=0 Research/Midday/LedgerTests.py
```

The [registry](Registry.json) pins SHA-256 over the original compressed bytes, or over LF-normalized UTF-8 bytes for the single plain JSON Supply-domain descriptor. The latter is a scope declaration, not a proof on its own: the verifier recomputes every window. The first command evaluates ordinary seed forests, including their permitted odd-index-divisibility lifts. It also checks exact prefix, pivot, nested and root-five certificates **without** applying such a lift. The [independent projection](LedgerTests.py) decodes each registered certificate to check its claimed root and exponent, then recomputes the many-to-many projection against [the previous frontier](../Nov25/Delta.json). A pair may occur in multiple accepted proofs but is counted once. SHA-256 match alone is not a mathematical check. The aggregate remains explicitly incomplete.

## Rolling checkpoints

| Research commit | Distinct newly excluded actuals | Newly closed shards | Shards still open | Verification |
|---|---:|---:|---:|---|
| `a5cf4a61` | 117 | 86 | 320 | Second aggregate checkout and independent projection |
| `5d3dec47` | 184 | 137 | 269 | Third complete ledger and independent projection; includes all 14 root-five actuals and 13 root-five shards |
| `97c2ff21` | 207 | 157 | 249 | Third plus 19 new ordinary forests, one exact prefix tree, and three exact root-three certificates; isolated replay of the difference and independent projection of the entire union |
| `417ef66e` | 230 | 176 | 230 | 23 additional ordinary forests from three producers; isolated difference replay at `076e4c86`, 12:15:53–12:16:55 UTC+08:00; entire union independently projected |
| `e1a656b4` | 238 | 181 | 225 | Added six ordinary seeds and two exact Euler-location partitions |
| `832a3f06` | 246 | 186 | 220 | Five directed seeds, one more Euler cover and two exhaustive binary supports |
| `70650ba4` | 250 | 190 | 216 | Two further graph exact trees, the joined `(7,1018)` binary support and a nested Three tree |
| `c2986e29` | 259 | 196 | 210 | More frozen forests, exact binary supports and complete Three join |
| `28ccde92` | 262 | 197 | 209 | Directed lifts reconciled without double counting, plus complete Three 88 |
| `16b17796` | 265 | 200 | 206 | Intake control: final group of 14 Forest packets and Three's 24 complete actuals |
| `21cf568d` | 266 | 201 | 205 | Complete support partition for `(31,10)`, including the final 204 leaves |
| **`6ab50f57`** | **267** | **202** | **204** | Strict full-domain `(11,718)` adds its singleton; final independent projection, 2,868/3,072 closed, 244 distinct open actuals and 181 singleton shards |

The final registry contains **255** packets: 231 ordinary seeds, five exact prefix trees and nineteen special entries. All baseline proof-code directories remained unchanged. No unconditional credit was given to sampling, a conditional subcell, or a second proof of the same key.

## Disjoint credit

* [Root three](../MiddayThree/README.md) and [root five](../MiddayFive/README.md) are complete certificates **for their stated canonical actuals**. See the additional [root-five audit](../MiddaySupply/FiveAudit.md).
* [Graph trees](../MiddayGraph/ReleaseNotes.md) consume their complete exact cases. [Forest controls](../MiddayForest/README.md) independently check arithmetic and overlap.
* [Terminal hitting-set reductions](../MiddayTerminal/FiveSets.md) and individual [support restrictions](../MiddaySupport/README.md) do **not** add complete exponents or shards on their own. A union covering every support cell may admit one exact pair if its closed-world verifier succeeds. It cannot be registered as a liftable forest seed.

## Rechecked block and conditional chain

At clean commit `076e4c86`, all 217 non-five packets in the fifth checkpoint (210 ordinary forests, 3 prefix trees, 4 root-three exact covers) passed together between 12:16:47 and 12:26:49 UTC+08:00 on November 25, 2026. The resulting 216 distinct keys and 163 shards reconcile with the 14 actuals / 13 shards of the frozen five audit. That earlier successful 14-line run ended at 11:51:22 UTC+08:00 (log SHA-256 `2be0944e0fc05807dc25941d09b2a9ee9b7d8c0497d320669add66570766479e`). No root-five verifier or input changed relative to `16e1682b`. The archived [root-five receipt](../MiddaySupply/FiveReceipt.json) reports the exit status and exact floors.

The [three-prime hitting theorem](../MiddayTerminal/Triple.md) is a global support restriction, **not** an additional canonical actual or shard. The initial chain including the historical `{3,5,7}` witness, its pair refinements, all three alternate cases, and the final triple each passed from isolated clean commits. The alternate exact Graph certificate for `(19,62)` also passed; this key is already registered through its ordinary forest and was not counted twice.

The exact pair `(31,10)` was admitted only after the separate [closed-world verifier](../MiddaySupport/Complete31.py) rechecked the `{3,5,7}` hitting prerequisite, four support partitions and the zero-exception final 204-leaf partition (13:02:54 UTC+08:00, 1,948.11 s). The independent final-tree replay passed in 950.25 s, floor 2401. For `(11,718)` the central isolated independent source replay covered 0 through 718 and required zero open windows; it passed at 13:05:56 in 2,548.41 s. The [Supply group's four separate receipts](../MiddaySupply/FullReceipt.json) cover both primary and independent implementations for `(11,718)` and `(7,1018)`. The latter exact pair was admitted through a separately verified binary support partition, not counted again as a Supply proof. The duplicate central Supply run for seven was stopped after those passes and is not reported as successful. At `6ab50f57` the entire final ledger and all 255 packet digests were reconciled from the isolated release tree at 13:06:53.

See [timed clean-run receipts](ReleaseReceipts.json) for UTC offsets, commit IDs, commands, exit codes, log digests, and the lack of uncommitted files before and after each reported run. These metadata aid reproducibility; the certificate replay itself remains authoritative.

## Final clean block reconciliation

The final union was reconstructed again from **four disjoint packet sets**, not by summing claims. The largest block (`16b17796`, 252 packets: 231 forests, 5 prefixes, 16 specials) finished on 2026-11-25 at 13:12:04 UTC+08:00 after 715.05 s; it produced 251 actuals and 187 new shards. The other three packets were the unchanged root-five unit (14/13), full `(31,10)` (1/1), and full `(11,718)` (1/1). All four individual projections passed; the independently recombined ledger matched the published `6ab50f57` delta **byte for byte** (LF SHA-256 `0da39e5f1346ac62f897d1ec6d6fce04466c914a79f453a31d6392ef57b2d39b`). Corresponding Registry LF SHA-256: `f3c4e0a46d83c5fb09bd6162397b5993d88407ff2d6ea5e93f455cfe3a74026f`. This is a cold block replay with explicitly reused immutable evidence, not a claim that all historical 3,072 proofs were rerun. Separately, the lead's full `ReleaseTriple.py --baseline` chain at clean `24766599` exited 0 at 13:08:37 UTC+08:00, log SHA-256 `8568400b4369172ed72dacdd2ead5826c764cdd9a022c8716175909aa0709b49`, final floor 2511. The latter does not change the numerical ledger.

## Runtime

Rolling isolated tests used CPython 3.11.9 (64-bit), Windows build 26200, Intel Core i9-14900HX (32 logical processors), `-I -S -B`, no numerical packages or discovery caches. Run from a release checkout rather than an active discovery tree. Full offline replay may take substantially longer than verifying a single packet. Researchers reusing an earlier completed sub-run must bind both the packet and the verifier plus all data dependencies to the earlier snapshot.
