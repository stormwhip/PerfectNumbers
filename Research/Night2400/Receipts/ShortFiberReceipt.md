# Scope-only independent review: canonical 19×282 and 31×16

Clean detached `c22fccb8366d5b1b80e2da01a29311181c3c9fad` from `E:\PerfectNumbers-Night2400-reviewa`, with only `Research/NightOrder/ECPP/` sparse-excluded. Python 3.11.9, no author caches or reserved files. The 31×16 author commit `818735f2b6e13ed7dba76438d4ad20aac7b7406a` has identical 31×16 packet and VerifyFibers Git blobs (`53ed69800f63a533ddf58899bf9b0847cc529c90`, `851e597b656f8c0db640e07409d7aebee7b86742`) and unchanged imported arithmetic dependencies. Verifier working-copy SHA-256 `7f652874ac1c3bef9f7da6b2c230b471f438e7163c83af583129f3db5dafe080`.

```text
python -I -S -B -X int_max_str_digits=0 Research/Night2400/VerifyFibers.py Research/Night2400/Fibers19x282.json.gz
python -I -S -B -X int_max_str_digits=0 Research/Night2400/VerifyFibers.py Research/Night2400/Fibers31x16.json.gz
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/ShortFiberScope.py
```

- **19×282:** UTC+08:00 2026-11-27 03:49:00.5614406 → 03:49:14.9778669, **14.405536 s**, exit 0. Packet SHA-256 `c54a126ff25576ba71ea8850f50902902d746b9103e370165d4dfcadd7c9fb0b`. Pivot `1735317810514627`, size tail **112**. All 27 live first exponents are the even integers 2 through 54. Covered 19: `[6,12,14,18,20,22,24,26,32,34,38,40,42,44,46,48,50,52,54]`; open `[2,4,8,10,16,28,30,36]`. One inner split, at first exponent 18, pivot `12814581503`, live 2–56 even, tail 115. Counts 46 forests / 1 split / 57 direct / 0 prices / 295 ECPP.
- **31×16:** UTC+08:00 2026-11-27 03:49:15.0012839 → 03:50:04.0902350, **49.087533 s**, exit 0. Packet SHA-256 `3192f91503433346399e5c5170f054311526a86f0c37d1571c5328deca20b8bb`. Canonical absence of 19, 7, 11; pivot `751670559138758105956097`, size tail **100**. Covered 14 of 16: `[4,6,10,12,18,24,28,30,34,36,40,42,46,48]`; open `[16,22]`. One inner split, at first exponent 18, pivot `8644393694750251101532589104938147961545996767`, exactly `[2,6,8,10,12,16]`, tail 35. Counts 19 forests / 1 split / 22 direct / 0 prices / 291 ECPP.

The standalone scope script imports no candidate modules and rebuilt both first domains and both internal sibling sets and tails, exit 0. All claims are exact first exponents for their stated root scope; **0 root exponents and 0 shards**.
