# P19_I00094 — exact exponent 502

Candidate against baseline `49b19bbdf6c46ac3cdd4cb0da2b6b08e1360fdec`; applies only to the exact key `(19,502)`, not to divisibility by `19^502`. The frozen shard has `remaining_actuals = [502]`; the certificate does **not** close that key or shard.

- First pivot `q = 14401804750392751` (54 bits), `v_q(D)=1`, `q≡3 (mod 4)`. Live first-pivot domain: even exponents from 2 to 34 inclusive.
- Covered: `6,8,10,12,14,18,20,22,24,26,28,30,32,34`. Open siblings: `2,4,16`.
- Odd exponents 1 through 69 fail the Euler constraint. Even exponents 36 through 70 fail the exact-prefix base bound (at 36 the decimal floor is 2431). The monotone size tail starts at 71, before constructing another exact-prefix state.
- Forest-only fibers: `8,10,12,14,18,20,24,26,32,34`; exact trees at `6,22,28,30`. Child domains, tails, and exact-state exclusions are recomputed at each split. The packet uses neither joint CRT pricing nor factor data during replay.

Packet: [P19I00094x502.json.gz](P19I00094x502.json.gz).
SHA-256: `9a3a1f2d8c04ed07de3b4ee9ea55991b77ccf5eda1077d6eb9d729026b9ba519`.

Cold replay from a repository checkout containing the Night2400 verifier (ordinary Python 3.11, assertions enabled):

```text
python -I -S -B Research/Night2400/VerifyFibers.py Research/Night2400/F/P19I00094x502.json.gz
```

When an independent candidate worktree has only frozen baseline code and this packet, use the lead's verifier explicitly:

```text
python -I -S -B E:/PerfectNumbers/Research/Night2400/VerifyFibers.py Research/Night2400/F/P19I00094x502.json.gz
```

Expected `counts_forest_split_direct_price = [517,29,568,0]`; 18 of the direct exclusions are at the first pivot. Missing compatible exponents are `open`, not excluded.

## Discovery notes (not needed for replay)

The factor index supplied initial root and forest labels. For `q = 14401804750392751`, divide each `Phi_d(q)` by its known factors before running GMP-ECM. First pass: `ecm -one -c 100 -q 20000` on the cofactors at `d = 7,9,11,13,17,23`; second pass: `ecm -one -c 150 -q 250000` on the remaining cofactors at `d = 7,9,13,17,23`. The runs used ECM's randomized curves; the recovered prime seeds below allow discovery to start deterministically without rerunning ECM. Labels in the packet are instead certified and their divisibility is checked by the offline verifier.

| `d` | Recovered prime seeds beyond the index |
| --- | --- |
| 7 | `49499718549480847050819378607`, `1772672823932701726062551609349341244303375454034618766101` |
| 9 | `5347`, `57928627`, `170745597409659016976479` |
| 11 | `766901279`, and the quotient after removing `46817`, `450803`, `766901279` from `Phi_11(q)` |
| 13 | `131`, `1245522784481`, and the quotient after removing both from `Phi_13(q)` |
| 23 | `139` |

Plain forests and split trees use the smallest witnessed lower bounds as growth targets; splits are ranked by minimum exact-prefix base across their surviving children. For `22`, one joint-price leaf also passed experimentally, but an ordinary exact tree avoids the CRT replay entirely.
