# P19_I00094 — exact exponent 502

Complete certificate against baseline `49b19bbdf6c46ac3cdd4cb0da2b6b08e1360fdec`. Applies only to the exact key `(19,502)`, not to divisibility by `19^502`. This covers the frozen shard's single remaining actual, `remaining_actuals = [502]`; no ledger was modified.

- First pivot `q = 14401804750392751` (54 bits), `v_q(D)=1`, `q≡3 (mod 4)`. Live first-pivot domain: even exponents from 2 to 34 inclusive.
- All 17 live exponents `2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34` are covered; no siblings remain.
- Odd exponents 1 through 69 fail the Euler constraint. Even exponents 36 through 70 fail the exact-prefix base bound (at 36 the decimal floor is 2431). The monotone size tail starts at 71, before constructing another exact-prefix state.
- Forest-only fibers: `8,10,12,14,18,20,24,26,32,34`; exact trees at `2,4,6,16,22,28,30`. Child domains, tails, and exact-state exclusions are recomputed at each split. The packet uses neither joint CRT pricing nor factor data during replay.

Packet: [Tree19x502.json.gz](Tree19x502.json.gz), 1,311,466 bytes.
SHA-256: `27faabaa543d51c082763fa4674ddf917df6447e28ee202c578bd6cea8d872ea`.

Cold replay from the repository root using ordinary Python 3.11, assertions enabled:

```text
python -I -S -B -X int_max_str_digits=0 Research/Session20261126/TreeCheck.py Research/Night2400/F/Tree19x502.json.gz
```

Expected `(19, 502, [1843, 103, 2038])` (forest leaves, split nodes, direct child exclusions). This counts the root split; 18 direct exclusions are at that split. Replay uses bundled ECPP chains, without network, the factor index, or the Night2400 verifier.

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

At fiber `16`, pivot `b = 3920383` has 23 live children, even `2..46`; its monotone size tail starts at `95`. An ECM scan on the remaining `Phi_d(b)` cofactors used `ecm -one -c 90 -q 140000` for `d = 9,17,19,23,29,31,37,41,43,47`. On the four residual children `2,4,18,22`, stronger smooth witness growth (`smooth_bits = 14`) and two targeted recoveries closed the gaps: `ecm -one -c 140 -q 300000` split the residue of `Phi_7(70179939667)` into `168661907185199` and `24426595370364318707942886021440199946666162217527`; `ecm -one -c 250 -q 500000 180000000` yielded `917201144988603572717` from the remaining `Phi_19(b)` cofactor and `6473486445949548374437551548543` from `Phi_23(b)`. The last of these primes has only two live exponents, `2,4`, both closed by single forests. Factoring `Phi_17(q)` was unnecessary.

Plain forests and split trees use the smallest witnessed lower bounds as growth targets; splits are ranked by minimum exact-prefix base across their surviving children. For `22`, one joint-price leaf also passed experimentally, but an ordinary exact tree avoids the CRT replay entirely.
