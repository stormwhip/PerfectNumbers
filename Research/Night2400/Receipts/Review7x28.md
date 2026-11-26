# D2 — exact (7,28), complete canonical mask partition for P7_I00009

Candidate `2fcb9397f1410e8fac959fcb0f90fece8770d527`, detached, clean tracked files, CPython 3.11.9. `Seven28.json.gz` SHA-256 `0b416d8f3cca2ae2d4a275cbdfc24b4d87a91c33fcb0cff814d3bb455f0f256f`. `OPN_REPO` unset; embedded ECPP and baseline files from the review tree only, no author/discovery cache.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/Night2400/D2/Verify.py
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/Partition7x28.py
```

**PASS complete exact canonical `(7,28)`, all 64 masks and no open branches.** Started 2026-11-27 00:06:53.358 +08:00; ended 00:10:43.292 +08:00; elapsed 230.0740645 s; exit 0. Minimum forest floors: historical 2405, new 2400; 43 embedded new ECPP entries.

The independent stdlib arithmetic script passed in 0.7449999 s. Using order `(19,7,11,31,13,3,5,17)`, a canonical root 7 has 19 absent and 7 present, exactly the 64 masks `m≡2 mod 4`. Independently checked partition: 13 historical forest masks, 27 new forest masks, 24 rational abundancy exclusions, disjoint and exhaustive. Of the 26 historical projected masks, 13 are historical forest masks and 13 are new forest masks; exterior 38 = 14 new forests + 24 abundance. Projection is not a premise for exclusion; its complement is audited. Frozen `FinalSprint/Delta.json`: `P7_I00009` has `remaining_actuals=[28]`.

`σ(7^28) = 59 × 127540261 × 71316922984999` was recomputed, and all three factors are proved prime by the candidate, hence mandatory. Optional abundance-only masks recompute exact geometric sums, minimum legal exponents and exact rationals, minimizing over the all-even configuration and each permitted single Euler placement; unknown exterior components only increase it. Minimum floor is 2015058 ppm, and exact `>2` is checked before reporting it. Historical proof shapes are retrimmed to present/absent scope and then fully replayed; historical verdicts are not used as proof.

The diagnostic largest-pivot split independently reproduces 28 live even exponents, and raw budget `7^28 (σ(7^28)/Q) Q^f` has `f=170` within `B`, strict overflow at `171`. The proof does not rely on that diagnostic: its two forest recurrences handle every exponent of each compelled prime, enumerating legal finite candidates and bounding the unenumerated monotone tail by the first omitted `q^f`. The forest predicates check compulsion, prime labels, unique scoped ownership, and only charge positive checked edge valuations. At most one Euler placement is allowed and both recurrence bounds must be strictly `>10^2400`. Exact full closure applies to `19∤N, 7^28 || N`; it is not a divisibility lift and does not exclude `7^28|N` with another exact power or with 19 present.
