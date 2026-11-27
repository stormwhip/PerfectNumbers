# A expanded — canonical (7,12), 68 candidate conditional fibers

Detached clean tracked candidate `cd7a982fbb9a79ff3c0edb4a80fe4f73a9189e34`, CPython 3.11.9. Compressed SHA-256 `bc75d954a42fefa5ac9da8f6e6ecc9ac5dc454d7820a35c8f94d507f3130c0dd`. The verifier is identical to the first reviewed A version `64647233885d4a22dc60435042e06e60433fcf70`.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/Night2400/A/Verify.py
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/FiberPartition.py Research/Night2400/A/Fibers12.json.gz
```

**PASS conditional 68 of 83, 15 OPEN; both commands exit 0.** Start 2026-11-27 00:12:21.964 +08:00; end 00:16:45.848 +08:00; cold replay elapsed 264.0494787 s.

The independent data-only audit confirms the root domain, 67 incompatible and 84 direct exponents, root tail 235, and all 15 nested split children and size-tail bounds. Root pivot `16148168401≡1 mod 4`, compelled valuation 1, with absent 19 (canonical branch). Trees use 290 forest leaves and no price leaves; 322 direct exclusions across all depths; 1943 ECPP entries. On this candidate 68 of 83 live initial fibers have no unresolved descendants. OPEN root fibers `[1,2,4,8,12,16,26,28,42,46,60,72,88,100,102]`. Proof is exact-only; all live nested siblings must be represented, all finite scan bounds include equality at `B`, and all terminal forest lower bounds use strict `>B`.
