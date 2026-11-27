# Independent replay of $(19,270)$

The complete replay certifies exclusion of the canonical exact pair $(19,270)$. The frozen ledger assigns this pair as the sole remaining member of `P19_I00056`.

## Complete replay

Detached clean tracked commit `5b9bd25c67d3b0862ade41b75a9b3a3674417df7`, CPython 3.11.9. Gzip SHA-256 `6a12206c48ccfef12f61111df5e27dd11ecf7c4f3352e8f3f0228b20f649eadd`. Frozen joint tree, price, forest and primality code is byte-identical (by Git diff) to `49b19bbdf6c46ac3cdd4cb0da2b6b08e1360fdec`. No author caches or discovery dependencies.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/FinalSprint/JointTree.py Research/Night2400/F3/JointTree19x270.json.gz
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/FiberPartition.py Research/Night2400/F3/JointTree19x270.json.gz
```

**PASS COMPLETE, 11/11 first fibers, zero OPEN.** Cold stock replay 2026-11-27 03:46:03.215–03:49:22.684 +08:00, elapsed 199.4735315 s, exit 0. Counters `[2815,80,2972,1]`; price receipt `(4,[3242,1099,537])` proves execution of the sole price leaf.

Independent data-only exact replay passed with zero open paths. Compelled pivot `107499032325771819886598832053082701603` has valuation one and is `3 mod 4`, so all 23 odd exponents through 45 fail the Euler rule. The first raw size tail is 46; evens 24–44 fail direct inequalities, leaving all eleven even exponents 2–22. Independent arithmetic rebuilt all 80 exact split domains (including root) with first strict raw overflow and equality retained at B. Trees account for 2,815 exact forests, 2,972 direct exclusions, 4,659 incompatible finite cases, one price and 7,651 ECPP labels.

The sole price is exactly `[(19,270),(107499032325771819886598832053082701603,18)]` and targets both fixed primes `[0,1]`. Stock JointTree runs the price checker by default. Both integer forest recurrences must be strictly above B. Frozen baseline confirms `P19_I00056` has only `remaining_actuals=[270]`; proof of this exact key does not lift to a divisibility assertion at different valuation.

## Earlier replay stages

The following stages all use the canonical root and exact exponent of the complete replay. Their conditional exclusions are included in the corresponding first-pivot domain above.

### Initial partition

For the compulsory pivot $107499032325771819886598832053082701603$, valuations 1 through 45 were tested before the strict size tail. Seven of eleven admissible values were excluded, leaving $\{4,10,12,16\}$. Both nested split domains were independently rebuilt. The cold arithmetic replay took 13.015 s. [Original replay record](https://github.com/stormwhip/PerfectNumbers/blob/b4b2a30601ef5e3f135c47c846c1e9801af57b3f/Research/Night2400/Receipts/Review19x270.md).
