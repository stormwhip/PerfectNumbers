# Night2400 C9 — low exact fibers of (11,12), P11_I00004

Cold replay from the repository root, using standard-library Python with assertions enabled:

```text
python -I -S -B Research/Night2400/C9/Verify.py
```

This candidate concerns odd perfect `N <= 10**2400` with `11^12 || N` and neither 19 nor 7 dividing `N`, the inherited root-11 class. The exact identity `sigma(11^12) = 1093 × 3158528101` forces the certified 32-bit pivot `q=3158528101`. Its raw prefix-only scan covers exponents 1–251 and the monotone tail from 252, yielding 96 incompatible, 78 direct, and 77 live values. The only fully closed first fibers here are **4 and 5**; no whole-key or shard claim is made.

Support masks encode `(19,7,11,31,13,3,5,17)` in that bit order, with 19 and 7 absent and 11 present. Every one of the 32 masks over 31, 13, 3, 5 and 17 is checked for the two full fibers, without trusting a prior support verdict.

| Exact pivot exponent | Direct | Strict abundancy | Dual forests | Remaining masks |
| --- | ---: | ---: | ---: | --- |
| 1 | 0 | 0 | 3 | 29; only 28, 140, 156 covered |
| 2 | 16 | 7 | 0 | 36, 44, 52, 60, 100, 164, 172, 180, 188 |
| 4 | 24 | 4 | 4 | None |
| 5 | 16 | 0 | 16 | None |
| 8 | 16 | 7 | 0 | 36, 44, 52, 60, 100, 164, 172, 180, 188 |

[JointTree11x10](../../FinalSprint/JointTree11x10.json.gz) uses the same inherited exclusions, but a different pivot. The [root-3 low proof](../../FinalSprint/LowBranches/Verify.py) also uses 1093 for `(3,6)`, yet its inherited exclusions additionally forbid 11, 31 and 13; it is not a valid source of verdicts for `(11,12)`. The shared structure used here is the support split and exact forest recurrence, not root-3 numerical bounds. The [local independent recurrence](IndependentRoot11.py) is the frozen [independent forest recurrence](../../Nov25/Compose/IndependentForest.py) with only its root guard changed to 11. Both recurrences require strict integer size greater than `10**2400`.

The [sealed support packet](Support11x12.json.gz) SHA-256 is `0bc1a9d8192ffb95cfff657054902d79a4e13fc9b56f045e60d504e668852ab4`. Discovery used read-only official data and PARI for certificates; cold replay uses neither. Directed attempts at the shared 62-bit factor for the still-open masks found a broad split (38 and 37 live branches at pivot exponents 2 and 8), and remnant forest floors 2056 and 1983 on the two chosen test masks, so no full exponent scan or additional coverage is claimed.
