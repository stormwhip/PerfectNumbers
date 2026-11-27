# Task 20 — independent acceptance receipt, reviewera

Reviewed detached commit `82a52f1ac637641249dd9b7a5cab7de6acc14da6` in `E:\PerfectNumbers-Night2400-reviewa` (Windows, Python 3.11.9). Initial porcelain status empty, HEAD not symbolic. Sparse rules `/*` and `!/Research/NightOrder/ECPP/`; all 17,801 skip-worktree paths fall under that prefix, and no tracked path below it is active. No directory contents there or author-side caches were used. Only this receipt directory is written. The candidate is bound by commit and the following SHA-256 values:

```text
a6ee8017516474539625c35e1672ee91328e18f6dccd18856ec00162f140b068  Research/Night2400/A/Verify.py
005e30587a5da7c8324d7f0dbc2bf446a3d9155ccc5ba202fb930109663369a2  Research/Night2400/A/Fibers12.json.gz
199e11c7181e6010496587a04f9ebfdcc3c0024406a94c160d67892f92ff0ba6  Research/Night2400/A/Price12.py
c11c8083a1dda795ecbdb86ab5b55e4c402250d8968edc118c14b35a67a9030d  Research/Session20261126/PivotCheck.py
d59d3f61d5d4035efb740d512967ba8cb8fd0a4964b4fb70009049ec4c4868ca  Research/Nov25/Compose/Compose.py
6d814d53da26c446244eed7736c9d54421dc601084275247f8a737a91187dba1  Research/NightLowRoute/Release/ForestReplay.py
2407b0df2a006ba8b95ca7b548206a6570dff47cb090f501c4dfeaed1f408fe8  Research/RootFiveNext/PrimeCheck.py
97794766a3bba670d2888d430dbb11b258c2955eac57cef739a2713c06bc1660  Research/Night2400/Receipts/Audit7x12.py
ca7abd66b05c6b86ab299645f10a1278b9e185c423f5e946322a8a7ff844a3ea  Research/Night2400/Receipts/Domains7x12.txt
```

## Cold candidate replay

Run from the checkout root, without inheriting project paths/site packages or writing bytecode:

```text
python -I -S -B -X int_max_str_digits=0 Research/Night2400/A/Verify.py
```

Wall clock 2026-11-27 01:16:00.9608420 to 01:23:46.2542023 (UTC+08:00); stopwatch 465.287011 s; Python and background job both exit 0. Terminal output:

```text
PARTITION live 83 covered 77 uncovered 6 forests 2138 splits 82 direct 2258 prices 2 ECPP 8656
UNCOVERED [1, 2, 4, 12, 28, 42]
```

## Independent branch enumeration

```text
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/Audit7x12.py domains
```

Elapsed stopwatch 1.312303 s; wall clock 2026-11-27 01:20:19.1516724 to 01:20:20.3446827 (UTC+08:00); exit 0 on the run producing [the UTF-8 branch transcript](Domains7x12.txt). This script reads only the compressed packet and does not import candidate modules. It proves `Q` prime by exhaustive trial division through `isqrt(Q)`, derives `σ(7^12)=Q`, and computes outgoing exact-branch lower bounds from the full product of sigmas with all factors 2 and all fixed-prime powers removed. It tests incoming overflow, forced size and abundancy, after parity/Euler and exclusion of 19. It checks every split's compelled divisor, exact set of live children and terminal size inequalities; primality of nested split pivots and all numerical forest bounds are checked in the cold candidate replay, not duplicated by the independent script.

For `v_7(N)=12`, `19∤N`, `N≤10^2400`, first-level exponents `1..234` are examined and `7^12 Q^234 ≤ B < 7^12 Q^235` proves the entire tail. Exclusions: 58 by parity/Euler, 9 more by forbidden 19, 84 direct, 83 live. Of these, 77 are claimed in the packet; uncovered `[1,2,4,12,28,42]`. In covered subtrees, all live sibling sets match; 82 splits, 2,138 forests, 2,174 nested direct contradictions (2,258 including the first level), 2 price leaves. The five-deep chain `13697→2800321→67→29→31`, taken only at exponents `2,6,2,2` up to the final split, is in the **106** fiber (101 forests and 107 direct), not the **72** fiber (651 forests across 23 splits). Candidate README line 11's “The latter” is misleading; this is a wording defect, not a certificate failure.

## Independent quadratic pricing of 100 and 102

```text
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/Audit7x12.py 100
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/Audit7x12.py 102
```

Separate, cache-free processes. The independent implementation factors `Q−1`, finds a generator of the whole unit group modulo `Q`, uses Newton doubling for the lifts and examines the exact incoming valuation `j` of each admissible cheap residue; its even-residue rejection follows from `r<Q^j` when `r^e<Q^(2j)` and `e≥2`. No factorization of `D=σ(Q^f)` or assumption that a surviving relaxed supplier is prime. It reserves one maximum rational loss per distinct supplier, and prices the remaining incoming demand `f−1` at `Q^(2j)` per component. With an exponent-one Euler prime, uses the residual demand `f−1−s`, with `s=v_Q(p+1)`. The external and internal Euler checks are alternative necessary bounds, not multiplied into the independent valuation price. Every internal progression is empty in both runs. No floating point used in any proof bound.

| Fiber | Wall start → end, UTC+08:00 | Stopwatch (s) | Exit | Size-derived max exponent | Orders | Relaxed suppliers | Incoming Euler windows | Internal windows, all empty |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 100 | 2026-11-27 01:19:49.1317753 → 01:20:47.4328862 | 58.464649 | 0 | 2869 | 102 | 1 | 64 | 36 |
| 102 | 2026-11-27 01:19:49.2170667 → 01:20:48.8981375 | 59.831057 | 0 | 2826 | 101 | 1 | 70 | 32 |

Both supplier relaxations retain the same base `626452921779998693356330974134487153561560877116246276877453472417044901053736926369289784516463816351639866492158807039016333048593048514870506341346579`.

**Scope:** 77 exact fibers, not closure of `v_7=12` nor of `P7_I00005`; credit 0 actual exponents, 0 shards.
