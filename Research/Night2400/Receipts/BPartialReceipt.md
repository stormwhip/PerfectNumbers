# B (3,12), primary fibers 1 and 66 — independent partial receipt

Worktree `E:\PerfectNumbers-Night2400-reviewa`; initial clean detached `cb63942ae25396015cb3439769231ef7ab2487fa` (also exact ref `research/night2400-b` when selected); sparse excludes only `Research/NightOrder/ECPP/`. No access to the reserved tree, no factor bank or author caches. Python 3.11.9.

```text
9e9f70749693231dff7ed4e07fa97d794601480db5caaf6a828f8c8f492b2436  Research/Night2400/B/DomainAudit.py
e03d7dfa7a13ddf88166ad36dd2b2f8e8f69f8e0856b56a4f02fc6a1c891cfa4  Research/Night2400/B/Verify.py
e565b4b7db1a8bb9698ca1d5ec3fb1a5e23986c6b3fdcf3aba5b533f65400034  Research/Night2400/B/Fiber1.json.gz
af0771bb9e32df928bd40ae770e0c172ee6b7db376b44bf5d4c3c77612a2aac3  Research/Night2400/B/Fiber2.json.gz
caa7837039a620cd4451dc9344f1455d6c9956550e55c014a9aa7321dcae186c  Research/Night2400/B/Fiber66.json.gz
b022dd8e1ef74a3b192e1d28df08ef3f1bf014a10a49a81fb76d242aa02d239e  Research/Night2400/Receipts/BDomainAudit.py
86d091492658e1648dc523b0b6ae7ab2db2123014573518371b260d2c6f6844c  Research/Night2400/Receipts/BBudgetAudit.py
4704145ef1dd33d1b0f7884459c484320f453025f30e8a95bc2044067530e15f  Research/Night2400/Receipts/BDomains.txt
```

```text
python -I -S -B -X int_max_str_digits=0 Research/Night2400/B/DomainAudit.py Research/Night2400/B/Fiber1.json.gz
python -I -S -B -X int_max_str_digits=0 Research/Night2400/B/DomainAudit.py Research/Night2400/B/Fiber66.json.gz
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/BDomainAudit.py Research/Night2400/B/Fiber1.json.gz Research/Night2400/B/Fiber2.json.gz Research/Night2400/B/Fiber66.json.gz
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/BBudgetAudit.py
```

Domain-only candidate invocation (no packets), UTC+08:00 2026-11-27 03:11:26.4021424 → 03:11:28.6441978, 2.232464 s, exit 0; archived counts `[90,2,4,0,0]` and first raw range 1–405. The independent domain script imports no candidate code; it trial-divides `797161`, removes fixed-prime and 2-adic contributions from the full divisor sums, rebuilds every regular internal split and both sides of each size tail, and compares the exact keys. UTC+08:00 03:12:15.8963923 → 03:12:19.5056576, 3.594929 s, exit 0; [per-split transcript](BDomains.txt). First domain 100, first tail 406, 96 excluded by the frozen archive, leaving `[1,2,66,96]` before the new packets.

| Primary exact exponent | Secondary pivot | Live | Covered | Raw unresolved | Tail | Forests | Inner splits | Other leaves | ECPP |
| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | --- | ---: |
| 1 | 398581 | 79 | 77 | `[102,108]` | 427 | 381 | 11 | 13 joint | 4884 |
| 2 | 22996651 | 71 | 71 | `[]` | 324 | 325 | 2 | none | 2585 |
| 66 | 5897 | 97 | 96 | `[6]` | 430 | 644 | 13 | 1 joint, 8 budgets, 1 supplier split | 5338 |

The row 2 gets an independently rebuilt domain here but not a duplicate full replay; its forests are separately reviewed. This receipt does not claim to replay the EulerRoute collateral. In particular, no new complete first fiber is credited by the f=1 and f=66 cold replays; after separately credited f=2, the remaining primary list is `[1,66,96]`. The raw secondary lists above are deliberately before any EulerRoute refinement.

Cold `Fiber1` candidate run, UTC+08:00 03:10:55.9738684 → 03:33:10.8266942, **1334.840668 s**, exit 0. `full_fiber=false`, `secondary_only={"1":77}`, `unresolved=[102,108]`, minimum floor 2400 (strict integer acceptance). Proof counts and hash match the table.

Cold `Fiber66` candidate run, UTC+08:00 03:10:56.1502890 → 03:18:01.1404846, **424.980018 s**, exit 0. `full_fiber=false`, `secondary_only={"66":96}`, `unresolved=[6]`, minimum floor 2400 (strict integer acceptance). Proof counts and hash match the table; the joint leaf is at secondary exponent 198 with zero exceptions and Euler windows `[12651,417,0]`.

The independent budget replay exited 0, UTC+08:00 03:13:22.6886564 → 03:13:23.5709538, 0.873378 s. The supplier split has exactly `[23:490,37:490,41:490,43:490]`. It derives the only possible odd order >1 modulo 983 (`491`) and directly enumerates odd multiples of that order (or of 983 for residue 1) as possible exponent-plus-one values. Large bases are excluded using bare budget `B/X`; each small prime's net cost removes its existing charge in the forced block. Sparse multiplicative dynamic programming gave maxima `2,1,1,1,1,0,0,0` against required incoming `5,129,137,147,149,177,191,221` across the eight budget leaves.

**No canonical root exponent or shard closure.**
