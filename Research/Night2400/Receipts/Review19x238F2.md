# F2 — (19,238), three complementary exact fibers

Candidate `52dcdbfb9b6a004c51e44beb2110169188ab3500`, detached clean tracked files; CPython 3.11.9; packet SHA-256 `b6eccf864b4209dfd8e938758cf7575775b45bc5f2ab4e0f00baf46332092bb7`. Stock verifier exact Git blob `851e597b656f8c0db640e07409d7aebee7b86742` from `850bee532621cdf5aca0fea142ef4364015007ad`, materialized only inside review tree; no author cache.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/Night2400/VerifyFibers.py Research/Night2400/F2/Fibers19x238.json.gz
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/FiberPartition.py Research/Night2400/F2/Fibers19x238.json.gz
```

**PASS conditional `[4,10,12]`; both commands exit 0.** 2026-11-27 01:27:30.813–01:28:48.648 +08:00, cold replay 77.9809498 s. Counts `[1279,52,1514,0]` forest/nested split/direct/price, all 52 internal domains reproduced independently, 2938 embedded ECPP entries.

The candidate discharges first fibers `[4,10,12]` under the exact same root/pivot scope as the separately cold-reviewed lead `[8,14,16,18]` packet. The disjoint union covers 7 of 9 compatible branches, leaving only `[2,6]`. Root valuation 1, pre-split tail 37, no odd legal exponent (`q≡3 mod 4`), evens 20–36 directly excluded. Nested exact-state budgets are inclusive at `B` and monotonic overflow is strict. No whole-key or shard credit unless the two remaining first fibers are separately discharged.
