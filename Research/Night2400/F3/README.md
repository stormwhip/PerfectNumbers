# P19_I00056 — exact key (19,270)

This complete certificate covers only `(19,270)` against baseline `49b19bbdf6c46ac3cdd4cb0da2b6b08e1360fdec`; it does not lift to other exponents. The frozen shard's `remaining_actuals` is `[270]`; no ledger was modified here.

- Root pivot `q = 107499032325771819886598832053082701603` has `v_q(D)=1` and `q ≡ 3 (mod 4)`. Every live exponent is covered: `2,4,6,8,10,12,14,16,18,20,22`.
- Odd `1..45` fail the Euler constraint. Even `24..44` fail the exact-state base bound, starting at decimal floor 2478. The monotone size tail begins at `46`.
- The main candidate supplied `2,6,8,14,18,20,22` without redoing their discovery. Its sole joint-price leaf at `18`, targets `[0,1]`, is unchanged; all added leaves are ordinary forests.

Packet: [JointTree19x270.json.gz](JointTree19x270.json.gz).
SHA-256: `6a12206c48ccfef12f61111df5e27dd11ecf7c4f3352e8f3f0228b20f649eadd`.

```text
python -I -S -B -X int_max_str_digits=0 Research/FinalSprint/JointTree.py Research/Night2400/F3/JointTree19x270.json.gz
```

Expected receipt `[2815,80,2972,1]` (forest leaves, splits including the root, direct child exclusions, joint-price leaves) and a sole price receipt `(4, [3242, 1099, 537])`. The frozen verifier reconstructs exact domains, checks bundled ECPP chains and integer lower bounds, and needs no data index or ECM.

## Discovery notes

At `10` the lone open exponent was `4` of `19450029992258577663204506221`; an ECM pass (`-one -c 170 420000 125000000`) split the degree-5 remainder into `115468107094292201` and `434123146888057324654331103683042979638441893499386359395417484878806771518163648312706233571`. At `4` only four old holes were revisited; factoring the degree-3 remainder on the lowest child supplied `81188427881165503621483` and an 11-child exact split.

At `16`, the `137` split has 94 live cases. Only `137^1` and `137^2` remained after the shallow pass; they were completed by splits on `23` and `73`, respectively. The failed root-level joint-price test was not repeated. At `12`, the `131` split has 98 live cases; the final branching chain runs through `973001`, `3832922749`, and `4897098934544879917`. Splitting degree-3 and degree-5 remainders of the last prime completed the `2` and `4` valuations as single forests. Discovery used local factor data and bounded GMP-ECM stages; these are not trusted by cold replay.
