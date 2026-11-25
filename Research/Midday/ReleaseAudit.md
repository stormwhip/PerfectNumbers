# Reproducing the canonical union

The ledger counts distinct `(root, actual exponent)` pairs first and then closes a canonical shard only if **all** its remaining actuals have been removed. Shards overlap: neither packet counts nor group-local shard totals are additive. The comparison point is commit `6732a1a894817457a1bc1b88b7d214ac4d6c9872` (406 open shards, 511 distinct actuals, 582 shard/actual incidences). The release does not prove the full bound.

From a clean checkout at the release commit, use a standard Python 3.11 interpreter with assertions enabled:

```sh
python -I -S -B -X int_max_str_digits=0 Research/Midday/CheckLedger.py --workers 4 --check Research/Midday/Delta.json
python -I -S -B -X int_max_str_digits=0 Research/Midday/LedgerTests.py
```

The [registry](Registry.json) pins the SHA-256 of the compressed bytes. The first command evaluates ordinary seed forests, including their permitted odd-index-divisibility lifts. It also checks exact prefix, pivot, nested and root-five certificates **without** applying such a lift. The [independent projection](LedgerTests.py) decodes each registered certificate to check its claimed root and exponent, then recomputes the many-to-many projection against [the previous frontier](../Nov25/Delta.json). A pair may occur in multiple accepted proofs but is counted once. SHA-256 match alone is not a mathematical check. The aggregate remains explicitly incomplete.

## Rolling checkpoints

| Research commit | Distinct newly excluded actuals | Newly closed shards | Shards still open | Verification |
|---|---:|---:|---:|---|
| `a5cf4a61` | 117 | 86 | 320 | Second aggregate checkout and independent projection |
| `5d3dec47` | 184 | 137 | 269 | Third complete ledger and independent projection; includes all 14 root-five actuals and 13 root-five shards |
| `97c2ff21` | 207 | 157 | 249 | Third plus 19 new ordinary forests, one exact prefix tree, and three exact root-three certificates; isolated replay of the difference and independent projection of the entire union |

## Disjoint credit

* [Root three](../MiddayThree/README.md) and [root five](../MiddayFive/README.md) are complete certificates **for their stated canonical actuals**. See the additional [root-five audit](../MiddaySupply/FiveAudit.md).
* [Graph trees](../MiddayGraph/ReleaseNotes.md) consume their complete exact cases. [Forest controls](../MiddayForest/README.md) independently check arithmetic and overlap.
* [Terminal hitting-set reductions](../MiddayTerminal/FiveSets.md) and [support restrictions](../MiddaySupport/README.md) are useful necessary conditions, **not** additional complete exponents or shards. They are not registered as forest seeds.

## Runtime

Rolling isolated tests used CPython 3.11.9 (64-bit), Windows build 26200, Intel Core i9-14900HX (32 logical processors), `-I -S -B`, no numerical packages or discovery caches. Run from a release checkout rather than an active discovery tree. Full offline replay may take substantially longer than verifying a single packet. Researchers reusing an earlier completed sub-run must bind both the packet and the verifier plus all data dependencies to the earlier snapshot.
