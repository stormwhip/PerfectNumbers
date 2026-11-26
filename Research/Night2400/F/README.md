# P19_I00094 — exact exponent 502

Candidate against baseline `49b19bbdf6c46ac3cdd4cb0da2b6b08e1360fdec`; applies only to the exact key `(19,502)`, not to divisibility by `19^502`. The frozen shard has `remaining_actuals = [502]`; the certificate does **not** close that key or shard.

- First pivot `q = 14401804750392751` (54 bits), `v_q(D)=1`, `q≡3 (mod 4)`. Live first-pivot domain: even exponents from 2 to 34 inclusive.
- Covered: `10,14,18,20,24,26,28,30,32,34`. Open siblings: `2,4,6,8,12,16,22`.
- Odd exponents 1 through 69 fail the Euler constraint. Even exponents 36 through 70 fail the exact-prefix base bound (at 36 the decimal floor is 2431). The monotone size tail starts at 71, before constructing another exact-prefix state.
- Forest-only leaves at `10,14,18,20,24,26,32,34`; exact trees with internal pivot `3920383` at `28,30`. Child domains, tails, and exact-state exclusions are recomputed at each split. The packet uses neither joint CRT pricing nor factor data during replay.

Packet: [P19_I00094-502.json.gz](P19_I00094-502.json.gz).
SHA-256: `7c01b17c11490c53471555c1ad06bff9d9716fb181c1ebe0fc570e24adb4cc1b`.

Cold replay from a repository checkout containing the Night2400 verifier (ordinary Python 3.11, assertions enabled):

```text
python Research/Night2400/VerifyFibers.py Research/Night2400/F/P19_I00094-502.json.gz
```

When an independent candidate worktree has only frozen baseline code and this packet, use the lead's verifier explicitly:

```text
python E:/PerfectNumbers/Research/Night2400/VerifyFibers.py Research/Night2400/F/P19_I00094-502.json.gz
```

Expected `counts_forest_split_direct_price = [89,6,107,0]`; 18 of the direct exclusions are at the first pivot. Missing compatible exponents are `open`, not excluded.
