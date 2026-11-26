# Remaining primitive cyclotomic outputs

`AtomAudit.py` is a factor-free replay of a necessary condition on each of four remaining anonymous outputs. For an odd prime factor `s` of `Φ_d(r)`, we have `s != d`, `s ∤ r(r-1)` and therefore `ord_s(r)=d` (where `d` is an odd prime). Thus `s ≡ 1 (mod 2d)`. These hypotheses are checked directly at every atom. Exact trial division through 20,000,000 tests every integer in that class, not just probable primes. None divides. A nonzero Fermat remainder and exact integer square root certify compositeness and nonsquareness, with **no** assumption of complete factorization or squarefreeness. This is not an exclusion of any of the corresponding exact fibers.

| Primary valuation `v797161` | Extra exact components | Output | Decimal digits | Trial count |
|---:|---|---|---:|---:|
| 1 | `398581^102` | `Φ103(398581)` | 572 | 97087 |
| 1 | `398581^108` | `Φ109(398581)` | 605 | 91743 |
| 96 | none | `Φ97(797161)` | 567 | 103092 |
| 66 | `5897^6,42059143035592870990447^2,589657170962820100934139512775879733212083419^12` | `Φ13(589657170962820100934139512775879733212083419)` | 538 | 769230 |

```sh
python -I -S -B Research/Night2400/B/AtomAudit.py
```

Optional discovery reproduction (GMP-ECM 7.0.6, GMP 6.3.0; `ECM` may point to its absolute path) for two fully completed primary-96 tiers:

```sh
bash Research/Night2400/B/ReplaySearch.sh 797161 97 250000 60000000 1001 1300
bash Research/Night2400/B/ReplaySearch.sh 797161 97 1000000 300000000 50001 50220
```

Neither tier found a proper divisor. These are only negative discovery receipts, not lower bounds on the prime factors; `AtomAudit.py` is the certified trial bound. The initial P−1 and P+1 search also had no hit, and is not a proof prerequisite.

In the fourth row, fixed factors are forced by `5897 | Φ67(797161)`, `Φ7(5897)=42059143035592870990447`, and `Φ3(42059143035592870990447)=3*589657170962820100934139512775879733212083419`. The specified exponents condition that path, not the entire primary fiber.

The stock square-price checker does not close any of these four anonymous outputs. For the 1-fiber atoms and the 96-fiber atom, its initial size-valuations lower bound fails even before an extra Euler-one window (Euler is already fixed in the 1 fiber). For the 66 hard path, targets 797161 and the 45-digit fixed component have residual counts `(65, 11)`; the square price is sufficient for Euler exponent at least five. Of the exponent-one Euler supply vectors, 184 survive simultaneous comparison of the basic joint price and the disjoint fixed-divisor-plus-Euler bound. Tests of each separate fixed sum's cofactor progression put those 184 in the exterior Euler case. The net source inequalities can also be replayed independently with `python -I -S -B Research/Night2400/B/EulerRoute.py`. Since the Euler prime `e` is exterior to the fixed outputs and occurs to exponent one, a distinct unassigned ordinary component `r^h` must emit it. Its mass exceeds `2e/3` because `σ(r^h)<(3/2)r^h`. Writing `a=2m-1<=e`, the integer source floor is `ceil(2a/3)`. If `r` divides neither anonymous block, its full component multiplies `XD*e`; this strictly contradicts the size limit in all 184 surviving windows. If `r` divides a block, dividing the source floor by that whole block (rounding up) is a conservative net lower bound. This additionally excludes the 386-digit block as a source in 67 windows, but does not exclude the 538-digit block in any. Both exact blocks are co-prime, and their product is the entire compulsory fixed-output divisor coprime to the prefix. A balanced internal-emitter bound leaves 168 windows (94 with only one possible block, 74 with either). It removes 16 additional windows; it does not resolve the full path. Here is the proof of the bound for either center `z` and cyclotomic order `k`, as the earlier root-three bound cannot simply be applied with `z=3`.

Let `W=z^k`, `Y=z^s`, `delta=W/Y`, and `r^c || (W-1)` for an emitter on that block. The latter valuation is the same as `v_r(D)` since the two blocks are coprime and `gcd(block,z-1)=1`; removing the factor 5897 from the first block does not change the valuation at `r`. Define `u=(W-1)/r^c`, `t=r^(h-c)`, `w=σ(r^h)/e`, and `H=max(1,W/e)`. Then `uw<(3/2)Ht` since `σ(r^h)<(3/2)r^h`. Both integers

```text
A0 = u*w*(r-1)-u-r*t
B0 = u*(w+σ(r^(c-1)))-σ(r^(h-c))
```

are divisible by `Y`: for `A0`, multiply by `e*r^c` and reduce using `W≡0`, `e≡-1`; for `B0` use `r^c B0=W*(w+σ(r^(c-1)))-(e+1)w`. Neither vanishes. `A0≡-W mod (r-1)` and even `r-1` does not divide odd `W`; for `B0` the second term has `z`-valuation at most the exact fixed exponent of `z` in `N`, strictly below `k`. This uses the combined contributions from the Euler and its distinct ordinary emitter; no assumption that `w` is coprime to `z` is needed. If `r-1<delta+2`, then oddness gives `r<=delta+2`. The exact identity `A0=((W-1)/e-1)*r*t-u*(1+1/e)` bounds a positive `A0` by `H*r*t` and a negative one's magnitude by `(2*H+r)*t` (use `u<=uw`, `e>=3`). These bounds and `|A0|>=Y` imply `t>Y/[H*(delta+4)]`. Otherwise `B0<(3/2)*Ht+W/(r-1)` when positive and `-B0<(3/2)t` when negative. In the positive case `W/(r-1)<=Y*delta/(delta+2)`; in both cases the same lower bound on `t` follows. Replace the true `e` by its lower endpoint in the increasing function `1/H=e/max(W,e)`. All replay comparisons are integer or rational.

Additionally, on all 184 windows the emitting exponent satisfies `ord_e(r)=h+1`. In fact, if `r≡1 mod e`, then odd prime `e` divides `h+1` by LTE, so `h>=e-1` and `r^h` itself exceeds the budget. Otherwise `ord_e(r)=o>1` divides the odd `h+1`; if proper, `h+1>=3o`, while `σ(r^(o-1))` is divisible by `e`. This gives `r^h>(2e/3)^3`. The exact inequality `X*a*ceil(2a/3)^3>B` for every nontrivial surviving window excludes it, since `r` is distinct from the prefix and `e`. Thus `e≡1 mod 2(h+1)` and `h+1|e-1`. This does not force `h+1` prime.

There is also a parity completion in each rough block. Both blocks are nonsquare, coprime to one another and to the prefix, and the Euler prime is exterior. Hence on the support of each block some prime with odd exponent in `D` must acquire at least one additional unit before its final ordinary exponent is even. These two distinct primes each exceed 20,000,000, so `N>=XD e*(20,000,001)^2`. This removes 14 of the 168 balanced windows and subsumes the earlier six small-rest exclusions. Conditional on the emitter's block, take the maximum of its bound for the block's net size and that block's parity floor. Multiply only by the disjoint *other* block's parity floor, then minimize across the two possible emitter blocks. This removes one further window; 153 remain. An exact small-rest abundancy check provides an independent fallback when its size test applies. For their common roughness threshold, the checker augments the earlier trial audit by also testing the 386-digit block through 20,000,000. If the residue `R=N/(XD e)` is bounded by `L < 20,000,001` and `e>L`, then `R` is coprime to `D`, `X`, and `e` and is an odd square. Enumerate `R` up to the chosen cap, retaining only coprime squares and rejecting forbidden output. An upper bound for the unknown `σ(D)/D` is `(M/(M-1))^k` with `M=20,000,001` and `M^k≤D<M^(k+1)`, and `σ(e)/e≤(a+1)/a`. The lower bound for each ratio is 1. Multiplying the exact ratios for `X` and `R` gives an interval; the test rejects a candidate only if this interval excludes 2. An unresolved small-rest candidate is not called impossible.

This leaves a genuine joint mass/incoming valuation obligation for the internal emitter. Merely multiplying the size and supply lower bounds would double-count any supplier already dividing the forced output blocks.
