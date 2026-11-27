# E4 — canonical (7,420), nine of ten exact fibers

Candidate `48280554bae3d5daa4f993f744ab84d6cab51e93`, detached clean tracked files, CPython 3.11.9; gzip SHA-256 `6fa4aedf044f62e21c365ceec486b9c97ddbda3fe801783c362609d75d050a5f`. The stock verifier came byte-for-byte from `850bee532621cdf5aca0fea142ef4364015007ad` blob `851e597b656f8c0db640e07409d7aebee7b86742` local to the review tree; no external cache.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/Night2400/VerifyFibers.py Research/Night2400/E4/Fibers7x420Nine.json.gz
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/FiberPartition.py Research/Night2400/E4/Fibers7x420Nine.json.gz
```

**PASS conditional 9/10; only first `6` OPEN.** 2026-11-27 01:29:53.654–01:30:22.232 +08:00, elapsed 28.7529031 s; both commands exit 0. Replayed forest/split/direct/price `[55,4,65,1]`, price `[[0,[8,0,14]]]`, 525 ECPP; independent raw tails `[48,27,62,63,42]`.

Canonical 19-absent branch; this is not the separate `(19,420)` key. First 120-bit pivot `1169407471026387018305554817094515359`, compelled valuation 1, raw tail 48, ten direct root exclusions, ten compatible children; `[2,4,10,12,14,16,18,20,22]` covered, `[6]` OPEN. Internal branches are exhaustively rebuilt. The four internal splits and all forest tails retain exact integer threshold semantics (no rounded rejection). At valuation 22 the one-target joint price compares strict bounds and handles all Euler cases. No shard or divisibility credit here.
