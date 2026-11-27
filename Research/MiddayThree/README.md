# Midday root-three work (fixed Nov25 frontier)

Only root 3, whose canonical mask excludes 7,11,13,19,31, is considered. The 44 shards / 62 distinct open exact exponents are from `../Nov25/Delta.json`. **New complete exact exponents certified in this directory: (3,178), (3,190), (3,342).** The first two each close the singleton `P3_I00042`, `P3_I00044`; 342 removes one actual from `P3_I00005` (nine other actuals remain), without standalone shard credit. The independently pursued root-three 336 graph is tracked separately by the merge lead.

## Verified scope and fixed registry

Relative to Nov25, the 16 ordinary packets in `Registry.json` close 16 distinct actuals and seven whole shards, with repeated certificates counted once. The shared full-order graphs for 150,156,166,180,186,208,216,220,246,286,298,336,360 were received from the lead and independently certified here; those are not separate discoveries to add to a global graph tally. Use `python -I -S -B Research/MiddayThree/Registry.py --replay` for both exact verifiers and the coverage map.

**One additional complete conditional-portfolio case:** `(3,138)` closes the singleton `P3_I00035`. The unique 57-digit pivot `115215201111546538317696820901417129607616709798043944747` divides σ(3^138). Modulo forbidden primes and Euler parity, only f=10,12,16,18 below 19 survive. Different private forests for these four exact cells and f≥19 give integer log10 floors 2408,2441,2424,2626,2747 respectively; the f=16 graph passed after targeted ECM on weak exact emitters. `Pivot138.json.gz` SHA-256 `db90ac4ff43d67b7b5595e78783eb9c09cada11d1a7529e6f887062c996aa104`. `Portfolio.py` and `IndependentPivot.py` both accept. A second portfolio, `Pivot126.json.gz` (SHA-256 `3fe6a2d9e068e6349f186a4c8a1a4d72ae28435ec3892b3c77a352aaa1cf146e`), closes `(3,126)` / `P3_I00032`. The exact pivot cases f=6,10,12,16,18 and tail f≥19 yield floors 3384,2440,2408,2424,2578,2516; again both verifiers pass. The ordinary registry plus these two portfolios therefore supply **18 distinct actuals / nine complete shards**, before deduplication with other teams. Never count an individual pivot case as an extra exact.

Two further portfolios close `(3,106)` (19 finite/tail leaves on two distinct compulsory pivots, 13 reusable forest graphs; integer floor 2405, SHA-256 `251bfa84f9dcede0a4b7668f308c89a809ff70d59a860c87ee0e69a93f54e002`) and `(3,108)` (13 finite/tail leaves, integer floor 2422, SHA-256 `e3da2e0b865f8bd839f0acc7086214aad7c715417f1e55e3ee47e67ffbff1ed5`). A graph discovered for one exponent of the forced pivot may verify a different cell **only** after recomputation at that cell, not by assuming its original emissions. `NestedReplay.py` checks each branch against both integer solvers; `PivotTests.py` checks duplicate owners and a mutated ECPP chain after warming the cache. The live combined authority is `Release.json`: **20 distinct roots/exponents, 11 complete shards; 42 of the initial 62 actuals remain.** From repository root run `python -I -S -B Research/MiddayThree/Release.py --replay`; `--check` tests object/manifest hashes and the fixed-frontier mapping only.

The recorded release replay returned 20 excluded pairs, 11 closed shards and 42 remaining pairs. For exponent 106 it returned 19 leaves in 13 graphs, with minimum integer floor 2405. [Original replay output](https://github.com/stormwhip/PerfectNumbers/blob/b4b2a30601ef5e3f135c47c846c1e9801af57b3f/Research/MiddayThree/ReleaseReplay.log).

## Certified exact-source forest: 342

`Forest342.json.gz` (SHA-256 `acdb5208a7fe7ba994ff6ee8dd701dad44e4c2f7b740a1b7ad039694b686d328`) records 13 certified distinct factors of σ(3^342), 340 private children and 38 ECPP chains. Start with the roots and a legal prefix (16 values per exact exponent progression); attach children only to a minimizing exact exponent in the current tree, reselect minimizing cells, and iterate. Five directed rounds replaced a 1523-order static pilot with a full 2449-order integer floor over all Euler positions. Each trigger rechecks σ divisibility, removes all graph and root-σ support from geometric-sum products, grants at most one Euler globally, and retains the lowest possible prime-power cost for every untreated tail. No assumptions about Euler outside the forest or colored emissions. Both offline standard-library verifiers accept:

```
python -I -S -B Research/MiddayThree/Forest.py Research/MiddayThree/Forest342.json.gz
python -I -S -B Research/MiddayThree/IndependentForest.py Research/MiddayThree/Forest342.json.gz
```

The second traversal uses a different ECPP implementation and evaluates the Euler-optional root program independently. Integer lower bound >10^2449 in both.

Two further disjoint exact cases use the identical scheme:

| packet | roots | children | ECPP | integer floor | SHA-256 |
|---|--:|--:|--:|--:|---|
| `Forest178.json.gz` | 7 | 228 | 36 | 2431 | `416767f6f53f8c212887d7da4f171221268122b6cf931e4e0a34cfa579e78882` |
| `Forest190.json.gz` | 4 | 377 | 63 | 2413 | `11fb6f2b4ca41bfb8df3a91ec34d61f249c2d0c0eed331306c8b36870f10363f` |

The original survey graph was not near the threshold for either. The first adaptive graph exceeded 2400 in round 5 and the second in round 8. Both received full double replay.

## Incoming unit tariff and two-sided generalization

Assume an odd perfect `N<=10^2400`, `3^e || N`, external Euler prime `q || N` with `s=v3(q+1)>0`, `Y=3^s`, `q=2Yk-1`, and tag `k mod 3` (1 or 2, odd k). Let `A=(3^(e+1)-1)/2` and `P=3^(e+1)`. The previous root sieve leaves 928 s values, i.e. 1,856 tagged cells, in five prime-index blind blocks. We only assert exclusions under these exact assumptions. A q dividing A would have odd order of 3, hence (3/q)=1; with q=1 mod 4 this would force q=1 mod 3, impossible. Some ordinary r^f must therefore emit q. Call such a source *blue* if r=2 mod 3. Do not assume that a blue emitter exists.

Each ordinary supplier z=1 mod 3, providing j units by LTE, emits for every `1<=i<=j` the integer `w=(x²+x+1)/3`, `x=z^(3^(i-1))`. It has no factor 3. All of its prime factors l have order 3 for x, so `l=1 mod 3`. The product W of all these integers is a divisor of the product of sigma values of ordinary components, without any pairwise-coprimeness requirement. Consequently `A W | N` (odd and coprime to 3), and q does not divide W. The k'=e-s smallest feasible unit prices, allowing phantom units and a common conservative tail cap, give an integer lower bound for W. Inputs with known forbidden factors in the corresponding cyclotomic factors are skipped; missing factors never exclude a unit.

Two-sided variant: choose a marked finite set D of known red primes coprime to A. Work in N². Each prime in D can pay one exponent copy from actual holdings (z contributes z^(2*3^(i-1)) to each received 3 unit), and one from W. Other primes pay two copies from W. Thus each incoming w is priced by `w * rough_D(w)`; multiply additionally by the supplier increment if marked. The cap uses only w, which never exceeds the relaxed price. Compound by `3^(2e) A² q²`, using q also absent from D and W. All prices, every marker ground-prime check and every bound use exact integers. Lower bound on q tests the first 12 eligible odd k in each residue class: forbidden factors of k, q and a failed base-2 Fermat test only *exclude*, never certify.

A blue source r^f has no interaction with W or D, since r=2 mod 3. External to A it costs `r^f>4q/5` (r>=5). Internal to A, use the previously proved balanced source bound `r^(f-v_r(A))>qY/[max(P,q)(P/Y+4)]` from `../NightThree/Proof.md`. This additional actual holding is disjoint from all previously counted factors. In the squared ledger its cost is squared. A claimed blue-source cut merely excludes such sources, not all red sources. In particular failure to factor a blind block is never an exclusion.

Offline independent implementation: `python -I -S -B Research/MiddayThree/ConditionalReplay.py`. Rebuilds all prices from sieved primes, checks marker coprimality for the specific A, re-enumerates q minima and verifies **each claimed predicate**, agreeing with the separate producers `Emission.py` and `Weighted.py`. No discovery cache, ECPP, SciPy, SymPy or downloaded database needed. Columns count rejected `(s,tag)` cells for the respective condition; **not additive**:

|e|tested|all sources excluded|external blue excluded|internal blue excluded|
|--:|--:|--:|--:|--:|
|1162|216|0|128|106|
|1108|360|66|228|198|
|990|408|60|192|150|
|970|416|59|188|142|
|856|456|50|152|96|
|total|1856|235|888|692|

At e=1162 both blue source modes are eliminated for **both tags throughout s=1055..1107**. The earlier `../Nov25/Three/SourceUnit.json` had retained all internal possibilities and both source colors; its 34 exterior exclusions should not be counted again. Here a next proof must exclude the remaining **red** source(s), or use some other contradiction. The stronger squared tariff adds 4 external-blue and 4 internal-blue exclusions at e=1162; other four rows match the simpler incoming-only pilot.

## Other scouts (discovery only)

`ScoutForest.py` tested all 62 actuals with exact-cost root-three private forests, at most 500 child primes each. We generated 46 missing certified large root factors locally (`PrimesWanted.json`, `PrimeCache/`); candidate discovery additionally used historical read-only `NightCache` and NightThree ECPP. `ForestScout.json` is the survey, not a proof release. On these forests the best unconditional diagnostic floor is 1523 at e=342, followed by 1423 at e=138. Five blind roots have no certified seed, and this static strategy cannot presently close a new exponent. `WindowForest.py` tested eight medians with an external-Euler half-cost split; no original root-sieve windows eliminated. No history, running quota or probability of primality is used as proof.
