# `(3,856)` exact primitive-source prefix addendum

This refines [Proof856](Proof856.md) under the same canonical E3 assumptions; all fixed inequalities and the rough-factor range are rechecked by the indicated command. We exclude the exterior-source branch at `s=696,697,698` and the interior-source branch at `s=678,679`. Hence the source-specific lower constraints strengthen to `s≥699` and `s≥680`, respectively. Neither source branch nor the whole key is closed.

## Exterior source, `s=696`

For `k=856−s`, compute `F=X·min_i [M[k−i] max(A·R,R^(2i))]`. Exterior source implies `N>(2/3)F q²` by disjointness. With `Y=3^s` and `q=2Ym−1` this bounds the whole multiplier domain by

```text
m ≤ (1+isqrt(floor(3B/(2F)))) // (2Y) = 74.
```

Enumerate every positive odd `m≤74`, removing multiples of `3,7,11,13,19,31` (16 left). The true prime `q` cannot have a factor from the small trial sieve; also the emitter's odd index `d=f+1` is prime to 3, divides `q−1` by primitive order, and `5^(d−1)≤B/(Fq)` by the same disjoint allocation. Compute every allowed order `d` through the exact strict size tail using the integer power bound and check `d|(q−1)`. Three candidate `m` survive, all eliminated by explicit Fermat witnesses, so no assumption that a pseudoprime is prime is made in this branch. The checker also supports exact conditional finite-field root tests if a candidate survives Fermat; these are not used at `s=696`.

At the next exterior `s=697` the same necessary inequality gives `m≤114235`. [PrefixPair856.py](PrefixPair856.py) uses the same complete range but inverts the order condition `d|(q−1)` to the residue class `m=Y^−1 mod d`. For each `d`, odd representatives are generated through the exact bound `q≤floor(B/(F·5^(d−1)))`. This yields 4796 distinct candidate `m`; modular powers 2 and 3 retain 77 (digest `ea89bfe769cbf4bb644c85ba38b45441e2ca1838f524cd9b22294e7e85f48e80`). For each candidate `(m,d)`, absence of a usable exact-order generator would leave it open; the verifier checks the order of the proposed generator by every prime divisor of `d`. It enumerates every element of exact order `d` (all coprime powers), possible actual ordinary sources since the full direct cap implies `r<q`. No residue both satisfies the ordinary base and size bound, so the 77 rows yield zero survivors. An optional GMP modular-power backend evaluates the same exact integer operations; the stdlib fallback requires longer but has no network or discovery dependence.

### Third exterior window `s=698`

Use the exact [square-kernel bound](KernelBounds.md), `sf(A)≥13000000000001`, replacing `AR` by `A·sf(A)` without adding any duplicated charge. The same exterior formula then gives `m≤15199714`. [Native698.cpp](Native698.cpp) constructs the complete small-prime/order wheel from the exact tariffs, and tests all 648244 candidates left in the wheel using GMP (exact) computations; 9481 pass Fermat tests. Every eligible `(q,d)` has its integer source bound strictly below `q²`, and primitive order forces one of the full set of nontrivial coprime powers of a verified order-`d` generator. No retained source is possible. The native replay completed with `FINAL 15199714 648244 9481 0`. The separate, independently reconstructed candidate wheel and repeated full native terminal are documented in [the audit receipt](../Audit/Root3Native698Receipt.md); no incomplete run is used as evidence. Compile `g++ -O3 -std=c++17 -pthread Native698.cpp -lgmpxx -lgmp -o Native698` and run `./Native698 6`; independently compile and replay [KernelRange](KernelRange.cpp) first with `3 857 13000000000000`, and also replay the certified roughness [Range.cpp](Range.cpp) with `3 857 58400000`. The thread count changes only performance. For the exterior emitter at `s≥699` and interior at `s≥680`, these arguments provide no full source exclusion; in particular no incomplete large-range progress is counted as a closed endpoint.

## Interior source, `s=678`

For `i=0,…,856−s`, use the four independently valid bounds on its `A`-support from [Proof856](Proof856.md). For fixed `i`, the right hand sides of the required lower constraints are nondecreasing in positive `q`, including expressions proportional to `q/max(W,q)`. A counterexample must pass all four for at least one `i`; equivalently it belongs to the union of their finite closed initial multiplier intervals. Binary search over the union computes the exact largest `m` whose necessary inequalities still hold: **911**. Conservatively test every positive odd `m≤911`; no assumption about sufficiency of those inequalities is made.

For each `m`, test the initial bans and small divisors as above. Independently use the bound `r^f≤B/(X q M[k])`: 3-root, Euler, emitter and all remaining ordinary 3 suppliers are distinct because the emitter has zero 3-supply, even if it lies on `A` support. Hence `R^(d−1)≤B/(X q M[k])`. Apply `d|(q−1)`, odd `d>1`, `3∤d` and full cap. Of 35 `m` with candidate `d`, Fermat checks leave a single pair `(m,d)=(313,13)`. If its `q` is prime, exact order 13 permits obtaining all 12 roots as the twelve nontrivial powers of one explicitly verified order-13 generator. At this pair `r^12` cap is strictly below `q^12`; thus actual `r<q` and the least positive residue represents every actual possibility. [Single856.py](Single856.py) checks all twelve; each violates at least one necessary test among `r=1 mod1714`, `r=±1 mod12`, oddness, roughness, size and `r|A`. If `q` is composite it could not be Euler, so no need for a primality certificate of this discarded `q`.

For the next interior `s=679`, the same exact `m` bound is 1689429. The direct modulus wheel in [PrefixPair856.py](PrefixPair856.py) uses smallest possible `r=R`, so the per-order bound is `q≤floor(B/(X·M[k]·R^(d−1)))`. This treats all odd `d>1,3∤d`, including composite orders, and tests every `m` in each residue class through its own integer endpoint. 60008 distinct `m` are represented before Fermat checks; 860 remain with validated modulus/order lists (digest `590021d1b4eb607347ad85c41a5d498d9c044184defa0b1c28c6da5b936c3ecc`). Each conditional prime and order is checked (`r<q` or retained if not), using each full set of exact-order residues; the interior test adds `r=1 mod1714`, the mod-12 condition, and `r|A`. No residue can be an emitter. Thus both tags of this entire `s` are excluded for the interior source role.

## Replay

From the repository root, compile [Range.cpp](Range.cpp) as documented in [Proof856](Proof856.md), then run:

```powershell
$d='Research/AstraFinalAfternoon2400/Three'
python -B "$d/Prefix856.py" "$d/Range.exe"
python -B "$d/PrefixPair856.py" "$d/Range.exe" 697 0
python -B "$d/PrefixIn856.py" "$d/Range.exe"
python -B "$d/PrefixPair856.py" "$d/Range.exe" 679 1
```

The interior starter driver calls the final [Single856](Single856.py) check. The two larger prefix enumerations were independently rebuilt by [AuditPrefix856.cpp](AuditPrefix856.cpp), including recomputed tariffs, a direct linear multiplier sweep (rather than the Python modular wheel), finite exact-order generators, and the root checks. With GCC/GMP, compile `g++ -O3 -std=c++17 AuditPrefix856.cpp -lgmpxx -lgmp -o AuditPrefix856` then run `./AuditPrefix856 697 0` and `./AuditPrefix856 679 1` (the independent checker uses the roughness premise from the separately replayed range proof). Outputs `PASS 0 697 114235 4796 77` and `PASS 1 679 1689429 60008 860`. These lower-source windows were part of the 322/358 conditional remainders in [Proof856](Proof856.md), not additional exact canonical root exponents. No ledger changes are implied.
