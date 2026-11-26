# Exact closure of (7,28) in canonical root 7

This packet excludes an odd perfect `N ≤ 10^2400` with `19 ∤ N` and `7^28 ∥ N`. It does not assume anything about other support, nor does it exclude `7^28 | N` with a different exact valuation. In the frozen [FinalSprint ledger](../../FinalSprint/Delta.json#L889-L898), the canonical shard `P7_I00009` has only the exact exponent 28 left. This directory does not modify the ledger.

```powershell
python -I -S -B Research/Night2400/D2/Verify.py
```

The [cold checker](Verify.py) reads the new [packet](Seven28.json.gz) and the [historical packet](../../FinalSprint/Support/Root7x28.json.gz). New packet SHA-256: `0b416d8f3cca2ae2d4a275cbdfc24b4d87a91c33fcb0cff814d3bb455f0f256f`. It needs the repository's public Python sources and standard library only. It doesn't read trial graphs, PARI, the factor bank, or sparse ECPP files, and doesn't accept an earlier support verdict on trust.

## Domain and size proof

The canonical support order is `(19,7,11,31,13,3,5,17)`. Since 7 is present and 19 is absent, the 64 supports are exactly the masks congruent to 2 mod 4. The historical projection names 26 of these. Of those, the verifier reconstructs and replays 13 historical forest graphs and proves the other 13 (`34,38,42,50,58,70,86,150,162,170,178,198,214`) using new graphs. Of the 38 masks outside the projection, 14 use new graphs (`2,6,10,14,18,22,26,30,130,134,138,142,146,154`) and 24 are rejected by elementary fixed abundancy. This proves 64/64 directly, not by trusting projection completeness or a hitting-set theorem.

The exact divisor sum is `σ(7^28) = 59 × 127540261 × 71316922984999`, with the three factors prime. They enter each forest as mandatory roots. A forest may also use the present S8 primes as roots. A tracked non-root label can be charged only under its unique owner and only when the actual divisor sum forces it. Removing tracked and fixed bases from other emissions leaves residual products that can be charged without factoring. Each graph is checked by the [Compose integer recurrence](../../Nov25/Compose/Compose.py) and the [ForestMasks integer recurrence](../../FinalSprint/Support/ForestMasks.py). Both require a strict integer product `> 10^2400`. Unexplored exponents at each node are included by the monotone component-size tail, even when no factorization of that tail is known. Both recurrences allow at most one Euler vertex; an Euler prime elsewhere leaves every listed component even. The 24 abundance-only masks are checked with exact rational arithmetic, again taking the minimum over the all-even configuration and every permitted single Euler position on the listed primes.

No explicit pivot split is used in the final proof: the largest factor's full exponent domain is covered within the forest. For comparison, the [domain diagnostic](Domain.py) finds 28 live exponents after the prescribed-pivot parity, excess valuation and size checks: `4,6,10,12,16,18,22,24,28,30,34,36,40,42,46,48,52,54,58,60,64,66,70,72,76,78,82,84`. The raw monotone pivot tail starts at 171. The proof instead covers every such sibling and the entire tail at the root.

## Optional discovery recipe

For discovery only, run these from the original worktree. The external factor bank and optional `flint` are read-only. Search stores local graphs under `trials/`; do not add that directory to version control.

```powershell
$env:PYTHONPATH='E:/PerfectNumbers/Build/Night2400/Python'
python -B Research/Night2400/D2/Search.py --db E:/PerfectNumbers/Build/Night2400/FactorData --mask 42 58 170 178 34 50 162 --rounds 35 --smooth 25
python -B Research/Night2400/D2/Search.py --db E:/PerfectNumbers/Build/Night2400/FactorData --mask 70 86 150 198 214 38 --rounds 35 --smooth 25
python -B Research/Night2400/D2/Search.py --db E:/PerfectNumbers/Build/Night2400/FactorData --mask 22 6 134 146 154 130 138 142 2 10 14 18 26 30 --phase extra --rounds 35 --smooth 25
python -B Research/Night2400/D2/Pack.py
```

[Pack.py](Pack.py) tries the pinned local Git certificate blobs, generates missing chains with PARI via WSL, validates the new chains, and writes the proof packet. The cold verifier requires neither those discovery tools nor the raw trial graphs.
