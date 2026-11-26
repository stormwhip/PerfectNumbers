# E6 — exact canonical (7,682), P7_I00123

Detached clean tracked candidate `e9e799ad1c744ec8ec311456f474f287f4718ab9`, CPython 3.11.9. Gzip SHA-256 `856e9c4dd428cec862860d1c1fb8effead573020d9673e68e0cd998142eff138`; stock verifier byte-identical to `850bee532621cdf5aca0fea142ef4364015007ad`, blob `851e597b656f8c0db640e07409d7aebee7b86742`, materialized only in review tree. No author caches or discovery data.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/Night2400/VerifyFibers.py Research/Night2400/E6/Fibers7x682Complete.json.gz
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/FiberPartition.py Research/Night2400/E6/Fibers7x682Complete.json.gz
```

**PASS COMPLETE 32/32, zero OPEN.** Cold replay 2026-11-27 03:32:00.502–03:40:10.476 +08:00, elapsed 489.9780864 s, exit 0; counters `[1378,29,1423,1]` and sole price receipt `(99,[37010,2604,0])`. Independent domain command also exited 0.

Independent domain replay finds all 32 even live first exponents `2..64`, first pivot `6298826803≡3 mod 4` compelled with incoming valuation one; 64 odd exponents illegal and 32 even exponents 66–128 directly too large, first raw monotone strict overflow 129. All 30 split domains including root match, inclusive at B and strict on the tails, with 1423 direct exclusions, 2845 incompatible finite cases, 1378 dual forest terminals and one price leaf exactly `[(7,682),(6298826803,58)]` targeting both fixed primes. 6679 embedded ECPP, no OPEN. Canonical root 7 excludes 19; frozen `P7_I00123` in `FinalSprint/Delta.json` has only `[682]` remaining, permitting exact residual-shard closure but no divisibility lift.
