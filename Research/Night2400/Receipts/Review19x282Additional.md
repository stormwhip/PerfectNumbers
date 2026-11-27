# F4 — (19,282), five added exact first fibers

**PASS conditional `[4,8,28,30,36]`; union with separately verified lead is 24/27, OPEN `[2,10,16]`.** Detached clean tracked `53ee0eb410846f0e0eb8afe38650f75e0db58be8`, CPython 3.11.9. Gzip SHA-256 `1823c62fd811f8fb0e95202ec02397b11992b1f4b365d4b172892eeca39a0ae8`.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/Night2400/VerifyFibers.py Research/Night2400/F4/Fibers19x282.json.gz
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/FiberPartition.py Research/Night2400/F4/Fibers19x282.json.gz
```

Both exit 0; 2026-11-27 04:18:30.399–04:19:48.863 +08:00; cold 78.6291831 s. Stock verifier byte-exact from `850bee532621cdf5aca0fea142ef4364015007ad`, no caches. Independent root pivot `1735317810514627` compelled valuation 1 and congruent 3 mod 4; root domain 27 evens 2–54, 56 incompatible odds, 28 direct overflows before strict tail 112. Exact arithmetic independently reproduced all 86 split child sets including root; 2302 forests, 2586 direct, 4571 incompatible finite cases, 3314 embedded ECPP. No price or full-key claim. Forest bounds are strict, while size budgets keep equality, and there is no lifting to other valuations.
