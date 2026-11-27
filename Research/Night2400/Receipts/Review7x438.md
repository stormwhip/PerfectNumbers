# Lead — canonical (7,438), six conditional fibers

**PASS 6/12, OPEN `[2,10,12,16,18,22]`.** Detached clean tracked candidate `1cf13e79aef8701241b759394ed997a2b82b0fe3`, CPython 3.11.9. Gzip SHA-256 `112faa9f5618a97bdae40cad1eb6ada8df6b90a18ad68447ceb84383ca3d24a9`.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/Night2400/VerifyFibers.py Research/Night2400/Fibers7x438.json.gz
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/FiberPartition.py Research/Night2400/Fibers7x438.json.gz
```

Cold replay 2026-11-27 02:06:42.881–02:06:47.874 +08:00, 5.1035911 s; both commands exit 0. Covered `[4,6,14,20,24,28]`; root 19 absent and compelled pivot `572749682520506652634407616247` with valuation 1. Raw root tail 57; 31 raw incompatible, 13 direct, 12 live. The two nested raw tails are 18 and 71; all exact child domains independently verified. 24 dual-evaluator forest leaves, 35 direct exclusions, zero prices, 287 ECPP packet chains. Exact bounds admit equality at `B` until strict overflow; no divisibility lift or shard credit.
