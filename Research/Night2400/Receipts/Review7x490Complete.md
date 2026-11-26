# E3 — canonical exact (7,490), P7_I00093

Detached clean tracked candidate `c5c07d2074044f524b941a5c767fc917fc8bc39d`, CPython 3.11.9. Packet SHA-256 `caeabb5d0ddedfa7fffb071404e712ad0a8233a47b8131c68d2f570df34a226d`. Sole extra stock source materialized from `850bee532621cdf5aca0fea142ef4364015007ad:Research/Night2400/VerifyFibers.py`, blob `851e597b656f8c0db640e07409d7aebee7b86742`; no author caches.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/Night2400/VerifyFibers.py Research/Night2400/E3/Fibers7x490Complete.json.gz
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/FiberPartition.py Research/Night2400/E3/Fibers7x490Complete.json.gz
```

**PASS COMPLETE, all 14 first fibers and zero OPEN.** Cold verifier exit 0, 2026-11-27 01:14:20.328–01:14:48.422 +08:00, elapsed 28.2685912 s; `[277,10,295,0]` forest/nested split/direct/price. The combined wrapper initially returned 2 because the independent audit script was absent after checkout; the audit ran separately and exited 0 after restoring the same checksum-verified script from `35cc4a951535c1d63fcf964ca53fe492ea932e1b`. Independently checked 11 splits including root, 525 incompatible finite exponents, and 1588 embedded ECPP entries.

Canonical root 7 means 19 absent. The certified first pivot `6644251020606657127` is compelled by `σ(7^490)` with incoming valuation 1. Raw size tail at 85, strict beyond `B`. Every live first branch `[4,6,10,12,16,18,22,24,28,30,34,36,40,42]` included. Late first fiber 16 splits on 696239: all 42 evens 2–84 live, even exponents 86–170 directly rejected, odd illegal, tail starts at 171. All branches are exact and proofs check both integer forest recurrences strictly `>B`; no threshold rounding, anonymous factor guesses, or transfer between incomplete siblings. Frozen `FinalSprint/Delta.json` confirmed singleton residual `[490]` for `P7_I00093`. The scope excludes neither different valuations nor cases with 19 present.
