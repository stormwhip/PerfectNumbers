# Review handoff — canonical roots 11 and 13

**Frozen reference** `495c59f55456a70994ce7848487e0c4e262c1984`. The [coverage rebuild](Coverage.py) verifies all **11 exact keys in 9 shards (7 singleton shards)** and nine forced-pivot domains. The other two keys `(13,612)` and `(13,618)` use an anonymous cyclotomic block. None of these keys or shards closes in the results here.

| Exact key | Completely excluded first-pivot exponents | Initial exact domain | Live remainder |
|---|---:|---:|---:|
| `(11,4)` | 42 | 211 | 169 |
| `(11,6)` | 21 | 98 | 77 |
| `(11,16)` | 29 | 47 | 18 |
| `(11,18)` | 16 | 37 | 21 |
| `(11,48)` | 9 | 19 | 10 |
| `(13,2)` | 51 | 297 | 246 |
| `(13,4)` | 28 | 122 | 94 |
| `(13,6)` | 15 | 50 | 35 |
| `(13,8)` | 13 | 89 | 76 |

**Total: 224 distinct complete conditional fibers**, namely [212 original forests](ForestCoverage.json), [11 recursive full first fibers](Nested.md) and the [one separate Euler/valuation/lattice fiber](Price48.md) `(11,48)` with `v_t=36`. The nested sets all lie in the original remaining lists, and their `(p,e,f)` identifiers are disjoint. The 212 forests, 8 original recursive fibers, f25 recursive mixed fiber, f13 recursive fiber and f36 valuation/lattice fiber have separate audit receipts. The latest f10 recursive fiber at `(11,16)` also passed [independent review](../Audit/Root11First10.md). Do not assign shard credit even if all 223 are accepted. The exact residual at `(11,48)` is `[2,4,8,10,12,16,18,22,28,30]` and at `(11,16)` is `[1,2,4,6,8,12,16,18,22,24,28,30,36,40,42,46,52,60]`.

**Anonymous keys.** [HighLinear](HighLinear.md) excludes all `v_13(q+1)=537..612` and `537..618`, respectively (76+82 exact supply windows) with no factorization or squarefreeness assumption. The [first endpoint supplement](Thin618.md) excludes `s=535,536` at `(13,618)` by full progression and a monotone signed tail. The [cyclic-subgroup supplement](ThinGeneral.md) also excludes `(13,618)` `s=533,534` and `(13,612)` `s=536`. Together the [independently verified bounds](../Audit/Root13GeneralWindowReceipt.md) are `s≤535` at `(13,612)` and `s≤532` at `(13,618)`. A separate [large exact replay](NativeLarge.md) now also excludes `(13,612)` `s=535` in both exact FLINT and GCC/GMP runs, giving the stronger `s≤534` there, pending independent integration. These are necessary conditions, not evidence of realizability. See the [independent anonymous receipt](../Audit/Root13HighLinearReceipt.md). The lower Euler supply windows and other species are not solved by this proof.

**Hensel guard.** [AllLifts](AllLifts.py) cold-passes 180 independent brute-force comparisons and two demonstrations of discarded nonleast prime lifts at weight 6. The accepted atom prices avoid the retracted methodological gap by checking `weight≤order−1`, so the least lift is complete in the restricted strict deficit interval. The anonymous proof instead handles full integer progressions, with no Hensel relaxations. The [PR #11 result](https://github.com/stormwhip/PerfectNumbers/pull/11) remains withdrawn.

**Main obstacles.** The narrowly surviving `(11,16)` first fiber 24 has one hard `v_z=2` substate at `z=1730263451729489729947159213315224702803351`. Certifying an additional 69-digit factor of `σ(z²)` exposes a `q^4` substate and additional factorization gaps; the exploration did not prove all its branches. At `(11,48)`, most smaller `σ(t^f)` blocks are genuinely anonymous, not treated as primes; more factor evidence or a stronger targeted valuation argument is still needed. The generic dual/forest/sizing models did not close the hard low fibers. No incomplete exploratory search is counted.

**Offline replay.** `python -I -S -B Research/AstraFinalAfternoon2400/ElevenThirteen/QuickReplay.py --local-arithmetic` passed the full 224-fiber local partition and arithmetic replay. The separate anonymous commands are in [HighLinear](HighLinear.md), [Thin618](Thin618.md), [ThinGeneral](ThinGeneral.md) and [NativeLarge](NativeLarge.md). The pinned [original forest](Forests.json.gz) hash is `141fa902e99953ad720e34360ed7e456a83c90133be31b092fcbfec4029f978f`; the pinned [f36 lattice packet](Price48Depth.json.gz) is `0e1a0db906c12ec4100ea6866193f5bb12cf34ac8915943f2655ff199f7d6f12`. The WSL factor bank, public factor hints and FLINT were discovery aids; verification uses only exact integer arithmetic and proof-grade primality chains.
