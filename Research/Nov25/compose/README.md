# Low-index composition pilot, 25 Nov 2026

**Zero complete exponent exclusions; zero shards.** The packets in this directory are conditional, not additions to the frontier. The positive-support cells below eliminate genuine subcases. The separate all-absent masks omit 3, 5, 7 and already lie inside the baseline three-prime hitting result; those packets are independent calibration only.

## Main result: an index-transferable support rule

Suppose `N` is an odd perfect number, `19,7,11,31 ∤ N`, and `13^E ∥ N` for an even `E` with `11 | E+1`. If `3·5 | N`, then **`v₅(N)=1`, `v₃(N)=2`, and `17 ∤ N`**. This is not an assertion that either 3 or 5 is individually absent. The rule doesn't require `N ≤ 10^2400`.

The seed factorization is `σ(13^10)=23·419·859·18041`. Every factor transfers by `σ(13^10) | σ(13^E)` and `I(13^E) ≥ I(13^10)`. Under the same prior absent primes, lower-bound `I(N)` by the product of minimally admissible abundancies for the forced support, taking the minimum over a single Euler position (or exterior Euler). The three exact minima are strictly above 2, with floors in parts per million:

| Hypothesis | `floor(10^6 × lower I(N))` | Consequence |
|---|---:|---|
| `3,5,17` all present | 2,092,943 | `17` absent when `3,5` present |
| `3,5` present, `v₅(N) ≥ 2` | 2,052,296 | `5` is the Euler prime with exponent 1 |
| `3,5` present, `v₅(N)=1`, `v₃(N)≥3` | 2,045,072 | `v₃(N)=2` |

At the fixed baseline, the rule applies to `(13,10)`, `(13,54)`, and `(13,76)`; `(13,76)` was separately excluded in the current results. Run `python -I -S -B Research/Nov25/compose/SupportRules.py 10 54 76`.

## Positive-support conditional cells

Besides the exact root component and the prior-root absence, assume `3·5 | N` for the following root-13 cells. The [transferable rule](<SupportRules.py>) supplies `v₅=1`, `v₃=2`, `17 ∤ N`. These five packets exclude the following indicated **exact** exponent of `18041`; they do not exclude `(13,10)` itself:

| Packet / `v₁₈₀₄₁(N)` | Exact cutoff |
|---|---:|
| [6](<branches/F13x10-m3-5x1-3x2-18041x6.json.gz>) | Log floor 2444 |
| [12](<branches/F13x10-m3-5x1-3x2-18041x12.json.gz>) | Log floor 2427 |
| [16](<branches/F13x10-m3-5x1-3x2-18041x16.json.gz>) | Log floor 2441 |
| [24](<branches/F13x10-m3-5x1-3x2-18041x24.json.gz>) | `v₅(S)=2 > v₅(N)=1` |
| [42](<branches/F13x10-m3-5x1-3x2-18041x42.json.gz>) | Log floor 2609 |

At root `(31,10)`, assuming `5 | N` and `3,13,17 ∤ N` additionally to the usual `19,7,11` absence, the following forest leaves exclude exact exponents of `150332843`:

| Packet / `v₁₅₀₃₃₂₈₄₃(N)` | Integer floor of lower `log₁₀ N` |
|---|---:|
| [2](<branches/F31x10-m2-150332843x2.json.gz>) | 2409 |
| [4](<branches/F31x10-m2-150332843x4.json.gz>) | 2511 |
| [6](<branches/F31x10-m2-150332843x6.json.gz>) | 2448 |
| [12](<branches/F31x10-m2-150332843x12.json.gz>) | 2611 |
| [14](<branches/F31x10-m2-150332843x14.json.gz>) | 2836 |
| [16](<branches/F31x10-m2-150332843x16.json.gz>) | 2811 |
| [18](<branches/F31x10-m2-150332843x18.json.gz>) | 2851 |
| [20](<branches/F31x10-m2-150332843x20.json.gz>) | 3421 |

These are all admissible exact exponents through 20 in that mask. The admissible tail `v₁₅₀₃₃₂₈₄₃(N) ≥ 22` was not closed (constructed floor 2246).

For a forest leaf, erase the exact assigned support from `S`, charge its remaining part once, and promote only primes already forced by that part or by presence assumptions. Every other label has one owner, which alone may cause it to be charged as a component. Residual sigma stripped of all fixed and trackable support can still be charged multiplicatively across distinct emitters. Two arithmetic recurrences compare the resulting integer bound against `10^2400` without factoring any unresolved residual. Standalone replays use `Replay.py --conditional` and `IndependentForest.py`, with the chosen packet path as the final argument.

## Conditional calibration packets

All rows assume an odd perfect `N ≤ 10^2400` with the stated **exact** root exponent and the corresponding prior-root absence. In addition to the explicit absence below, prior-root absence is `(19,7,11,31)` for root 13 and `(19,7,11)` for root 31. No positive support assumptions are used in these terminal packets.

| Packet | Additional absent primes | Integer floor of lower `log₁₀ N` |
|---|---|---:|
| [Terminal 13×10](<branches/T13x10-mask0-f0.json.gz>) | 3, 5, 17 | 2988 |
| [Terminal 13×22](<branches/T13x22-mask0-f0.json.gz>) | 3, 5 | 2436 |
| [Terminal 31×6](<branches/T31x6-mask0-f0.json.gz>) | 3, 5, 13 | 2797 |
| [Terminal 31×10](<branches/T31x10-mask0-f0.json.gz>) | 3, 5, 13 | 2759 |
| [Weighted forest 31×10](<branches/W31x10-s3-5-13-17-m0-f0-mu4000.json.gz>) | 3, 5, 13, 17 | 2658 (primary replay) |

Two cold replay implementations rebuild the four terminal bounds from their packets, without historical trees, factorizations, solver or primality caches. The weighted-forest calibration uses the primary replay only. Both use the repository's projective ECPP verifier; numerical comparisons are independent (fixed-point atanh enclosure versus directed Decimal). The primary CLI rejects a calibration packet if submitted without `--conditional`.

```text
python -I -S -B Research/Nov25/compose/Replay.py --conditional Research/Nov25/compose/branches/T13x10-mask0-f0.json.gz
python -I -S -B Research/Nov25/compose/IndependentTerminal.py Research/Nov25/compose/branches/T13x10-mask0-f0.json.gz
python -I -S -B Research/Nov25/compose/Tests.py
```

Substitute any other terminal packet from the table for the two replay commands.

### Terminal accounting

1. For each exact assigned prime power, multiply the odd part of its divisor sum into `S`. These are distinct sources, so the **product** divides `N`. Check exact valuations at assigned bases. Their actual powers make up `X`. Strip their support, and all further explicitly represented prime bases, from `S` to obtain the residual `D₀` (a composite is fine). Thus the constant charge is `log(X·D₀)`.
2. Every explicit prime outside the fixed states has ordinary even options and, when admissible, Euler options `f ≡ 1 mod 4`. Below its cap, a selected option represents **one exact component**, and may charge the full odd `σ` residual after stripping all fixed and explicit bases. Those residual factors can overlap each other and `D₀`; multiplicity is still valid by `σ(N)=2N`. A selected tail represents a lower exponent bound but emits nothing. Forbidden-prime tests are evaluated exactly.
3. At any receiver named in the input, count only exact emissions and their checked valuations; ignoring unlisted edges is a relaxation. At a fixed exact receiver, the sum cannot exceed its unused exponent capacity. At an explicit receiver, total exponent must cover initial and selected source valuations. Euler placement is globally at most one.
4. Actual prime support is partitioned for the abundance upper estimate. Fixed components and explicit components are separate. For remaining primes, count a prime at most once, attributing any one covered occurrence to a charged block or `D₀`. Overcounting via `floor(log₅₀₀₁(block))` for **each** block is allowed here only because it upper-bounds available abundance. Any prime not covered by any charged block contributes entirely from the generic tail. The single generic Euler option can waive the ordinary cost-amplitude ratio for one such prime, never one per block. Rounding always weakens necessary constraints and lower bounds.
5. Solve on a larger real-valued feasible region only for discovery. Cold replay evaluates the exported dyadic nonnegative multipliers against outward-coefficient row inequalities, group minima, and a nonnegative unbounded-tail reduced cost. Admission uses a strict exact comparison to `2400 log(10)`.

## Discovery findings and limits

- For `(13,10)`, making the terminal bound apply without 17 absent lowered it from 2988 to 2172 in the cheap trial. Allowing 3 or 5 was much worse: representative exact terminal scores 319 (3 present), 854 (5 present), 261 (both); under the forced `3²·5` core the terminal score remained 310.
- Exact splitting on `18041` can help the sparse private-source forest where linear relaxation fails. In the `3²·5` exact core it closed some cells, e.g. `f=6,12,16,42`; a 25-round read-only cached run on `f=4` reached only 2296. The high-exponent gap includes `f=96` and a representative tail after 100, so no complete 3+5 branch was emitted.
- `(31,6)` has a useful certified anchor `917087137 = σ(31^6)` (ordinary, since `11 | 917087137+1` makes every Euler exponent inadmissible). Its historical 108 cells include 25 arithmetic proposals below 2400. Sparse composition improved neither representative low cells `f=2,4,10,36,52,72` nor `f=96,106` enough. The all-absent LP closes only an already-excluded mask, not the whole anchor split.
- The low `(19,16),(19,22)` and `(13,12)` ordinary graph candidates were well short of the target. No complete exponent was proven for any of the six requested pairs. The 31×10 present-five mask without fixing the 150332843 exponent peaked at only 2298 in the weighted trial.

The exact-source branch and outgoing accounting are adaptations of the established factor-chain method. See [Brent–Cohen–te Riele (1991)](https://maths-people.anu.edu.au/~brent/pub/pub116.html) and [Ochem–Rao (2012)](https://doi.org/10.1090/S0025-5718-2012-02563-4). In particular, an actual source component is required; `r^f | N` alone never activates `σ(r^f)`.
