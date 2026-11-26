# F2 expanded — (19,238), four complementary fibers

Candidate `7693d79b422126d98dec3ccdbe7cd1363fbdba0f`, detached and clean tracked files, CPython 3.11.9. Packet SHA-256 `28f84ea1c75a5116e318cceba2720d231121157303ddc78bd64b02029b200a45`. Stock verifier byte-for-byte from `850bee532621cdf5aca0fea142ef4364015007ad`, blob `851e597b656f8c0db640e07409d7aebee7b86742`. No author caches.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/Night2400/VerifyFibers.py Research/Night2400/F2/Fibers19x238.json.gz
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/FiberPartition.py Research/Night2400/F2/Fibers19x238.json.gz
```

**PASS, combined 8/9, only `[6]` OPEN.** Both commands exit 0; 2026-11-27 01:54:30.029–01:56:57.317 +08:00, replay 147.4395054 s. 2292 forests, 93 internal splits, 2588 direct exclusions, 4418 ECPP. Independent data-only audit examined all 94 split domains including the root. New f2 subtree has 41 splits, 1013 forests, and eight compatible second exponents `[1,2,4,5,6,8,9,10]` before strict raw tail 23.

One new first fiber 2 is added to the preceding `[4,10,12]` exact coverage, for `[2,4,10,12]` in this packet. The disjoint union with the separately certified lead `[8,14,16,18]` packet leaves only `[6]` open. Both use pivot `606492758240679674698864343145363724798136175178043`, compelled valuation one, exact domain all even `2..18`, odd exponents illegal, evens 20–36 direct overflow, and strict monotone raw tail beginning at 37. No exact-key or shard credit yet, and no divisibility lifting.
