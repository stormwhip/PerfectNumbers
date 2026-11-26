# P19_I00094 — exact exponent 502

Candidate against baseline `49b19bbdf6c46ac3cdd4cb0da2b6b08e1360fdec`; applies only to the exact key `(19,502)`, not to divisibility by `19^502`. The frozen shard has `remaining_actuals = [502]`; the certificate does **not** close that key or shard.

- First pivot `q = 14401804750392751` (54 bits), `v_q(D)=1`, `q≡3 (mod 4)`. Live first-pivot domain: even exponents from 2 to 34 inclusive.
- Covered: `2,4,6,8,10,12,14,18,20,22,24,26,28,30,32,34`. The only open sibling is `16`.
- Odd exponents 1 through 69 fail the Euler constraint. Even exponents 36 through 70 fail the exact-prefix base bound (at 36 the decimal floor is 2431). The monotone size tail starts at 71, before constructing another exact-prefix state.
- Forest-only fibers: `8,10,12,14,18,20,24,26,32,34`; exact trees at `2,4,6,22,28,30`. Child domains, tails, and exact-state exclusions are recomputed at each split. The packet uses neither joint CRT pricing nor factor data during replay.

Packet: [P19I00094x502.json.gz](P19I00094x502.json.gz).
SHA-256: `2a20e55f0e5dff6fce3706ba7f20ebe53c2a5f3c5d46a898f1bcaef14e1cf0f9`.

Cold replay from a repository checkout containing the Night2400 verifier (ordinary Python 3.11, assertions enabled):

```text
python -I -S -B Research/Night2400/VerifyFibers.py Research/Night2400/F/P19I00094x502.json.gz
```

When an independent candidate worktree has only frozen baseline code and this packet, use the lead's verifier explicitly:

```text
python -I -S -B E:/PerfectNumbers/Research/Night2400/VerifyFibers.py Research/Night2400/F/P19I00094x502.json.gz
```

Expected `counts_forest_split_direct_price = [927,52,1014,0]`; 18 of the direct exclusions are at the first pivot. Missing compatible exponents are `open`, not excluded.

## Discovery notes (not needed for replay)

The factor index supplied initial root and forest labels. For `q = 14401804750392751`, divide each `Phi_d(q)` by its known factors before running GMP-ECM. First pass: `ecm -one -c 100 -q 20000` on the cofactors at `d = 7,9,11,13,17,23`; second pass: `ecm -one -c 150 -q 250000` on the remaining cofactors at `d = 7,9,13,17,23`. The runs used ECM's randomized curves; the recovered prime seeds below allow discovery to start deterministically without rerunning ECM. Labels in the packet are instead certified and their divisibility is checked by the offline verifier.

| `d` | Recovered prime seeds beyond the index |
| --- | --- |
| 7 | `49499718549480847050819378607`, `1772672823932701726062551609349341244303375454034618766101` |
| 9 | `5347`, `57928627`, `170745597409659016976479` |
| 11 | `766901279`, and the quotient after removing `46817`, `450803`, `766901279` from `Phi_11(q)` |
| 13 | `131`, `1245522784481`, and the quotient after removing both from `Phi_13(q)` |
| 23 | `139` |

At fiber `2`, the next pivot is `r = 5325670984080451`, with 17 live children at even exponents `2..34`. The hardest early children at `2,4` benefit from smooth-witness factor search (`smooth_bits = 14`; head up to 160); at `6`, GMP-ECM fully separates `Phi_7(r)` into `678199904683466760337` and `33642500759072872659525350459955076820019491913057000369390394124572942261`. Scanning `Phi_d(r)` with `ecm -one -c 150 -q 200000` also yielded seeds `1913297,27179066333,249655884677` (`d=11`), `53,1823849,157963651` (`d=13`), `31,998551` (`d=15`), and `43247627` (`d=17`).

At fiber `4`, the next pivot `s = Phi_5(q)/5` has live children `1,2,4,5,6,8`. ECM on the cyclotomic values of `u = Phi_3(s)/3` uses `ecm -one -c 250 -q 250000`. For `Phi_3(u)`, the recovered factor `155759304137208051` splits into `3,7,31,139,157,12841,853807`; its quotient is also prime. `199` divides `Phi_2(u)/2`. On the open child `s^4`, `ecm -one -c 300 -q 450000 100000000` recovered `248861` from the remaining `Phi_5(s)` cofactor; stronger smooth witnessed search (`smooth_bits = 15`) closed the child without fully factoring its cofactor.

Plain forests and split trees use the smallest witnessed lower bounds as growth targets; splits are ranked by minimum exact-prefix base across their surviving children. For `22`, one joint-price leaf also passed experimentally, but an ordinary exact tree avoids the CRT replay entirely.
