# F expanded — (19,502) fourteen conditional fibers

**PASS 14/17; OPEN `[2,4,16]`.** Detached clean tracked candidate `f861797989139c9af83698fe142f58b915e594a5`, CPython 3.11.9. Compressed SHA-256 `9a3a1f2d8c04ed07de3b4ee9ea55991b77ccf5eda1077d6eb9d729026b9ba519`. The sole added untracked entry point was byte-identical to `850bee532621cdf5aca0fea142ef4364015007ad:Research/Night2400/VerifyFibers.py`, Git blob `851e597b656f8c0db640e07409d7aebee7b86742`, SHA-256 `6e5d4c19f0b353f5a80998e120fe6b00c7f5dc285c42a241461f762db1987b6c`. The frozen dependencies were verified unchanged across the two commits.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/Night2400/VerifyFibers.py Research/Night2400/F/P19I00094x502.json.gz
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/FiberPartition.py Research/Night2400/F/P19I00094x502.json.gz
```

Start 2026-11-27 00:11:38.575 +08:00; end 00:11:48.704 +08:00; elapsed 10.2553076 s for cold replay; both commands exit 0. Certified `[6,8,10,12,14,18,20,22,24,26,28,30,32,34]`. Replay reports 517 forest leaves, 29 nested splits, 568 direct exclusions, 0 price leaves. Independent domain audit confirmed 487 embedded ECPP entries and the strict raw size tail at 71 (35 odd illegal, 18 legal even direct exclusions, live domain `[2,4,...,34]`). All 29 secondary split domains and tails were exhaustively rebuilt, matching every sibling in the packet; only root siblings 2, 4 and 16 remain open. Does not close shard `P19_I00094` or support a divisibility lift.
