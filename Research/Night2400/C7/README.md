# Night2400 C7 — exact prefix supplier budget

From the repository root, using standard-library Python with assertions enabled:

```text
python -I -S -B Research/Night2400/C7/Verify.py
python -I -S -B Research/Night2400/C7/Verify.py --regression
```

The [prefix price](PrefixPrice.py) is the frozen [joint valuation recurrence](../../FinalSprint/JointValuation.py) with one additional necessary condition at deficit suppliers. Let `X` be the product of the exact assigned prime powers and `C` the fixed odd sigma product with assigned support removed. Both `C` and the actual unassigned prime power `r^f` divide `N/X`, whether or not `r` already divides `C`. Consequently

```text
r^f / gcd(r^f, C) <= floor(10^2400 / (X C)).
```

An exterior supplier (`r ∤ C`) is charged its full cost; an interior supplier is charged only the excess over already forced multiplicity. This exact condition excludes impossible deficit exceptions without factoring `C`. The original enumeration and all closure assertions are unchanged; the filter only removes cases inconsistent with a necessary divisibility bound. The price lower bound still uses `X`, not `XC`, to avoid charging a forced interior prime twice.

**Strict coverage:** at `(13,372)` in the root-13 class (19, 7, 11, 31 absent), the [sealed leaf](Leaf2.json) excludes only the exact assigned path `[(13,372), (438552673580231875649,12), (756749110661077,4), (463891,28), (2239,2), (128599,60), (3,2)]`. Certified targets are 13 and 128599, and the receipt is `(1, [4442, 9335, 8483])`. This does not cover the `3` siblings, the `128599` or `2239` siblings, or the entire first fiber, key or shard. The optional known [Tree31x388](../../FinalSprint/JointTree31x388.json.gz) regression returns `(10, [5188, 1814, 0])` with the same checker. Neither check loads discovery inputs.

On the two other unresolved exact paths (indices 1 and 3 in the discovery sequence), this filter eliminated all exterior Euler windows but left 377 and 628 unresolved interior block windows, respectively. Tightening the cofactor range by the exact price upper endpoint and using the prime cyclotomic order congruence still left 109 and 368 interior windows even when all discount losses were hypothetically removed. Those observations are diagnostics, not exclusions. No ECM or forest scouting is involved in this packet.
