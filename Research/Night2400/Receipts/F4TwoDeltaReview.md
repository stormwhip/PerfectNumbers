# F4 — (19,282), incremental exact first fiber 2

**PASS incremental f2, union 26/27, only f10 OPEN.** Detached clean tracked `879c892159b0915a461f0642922de93034dcb65f`, CPython 3.11.9. Complete updated packet SHA-256 `0a1561392e8142d0d178322e5422d61646bffb7494904d153e90bd8269d91d8b`. The prior independently replayed packet `2251e5e8603e2edf82389d4f4d07a65716e9fef9` (SHA-256 `4cde99ecee143874fa6609c5858bb9c5f83673ee213c619c452ddd433beeefde`) was materialized byte-exact as `Research/Night2400/F4/ReviewOldPacket.json.gz`.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/F4TwoDelta.py Research/Night2400/F4/ReviewNewFiber2.json.gz
python -I -S -B -X int_max_str_digits=0 Research/Night2400/VerifyFibers.py Research/Night2400/F4/ReviewNewFiber2.json.gz
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/FiberPartition.py Research/Night2400/F4/Fibers19x282.json.gz
```

Extraction requires exact equality of all six prior parsed subtrees and previously certified ECPP chains, unchanged key/pivot, exactly one added f2 subtree, and all newly embedded ECPP reachable from f2; 2815 new chains, 4686 chains in the extracted packet. Extract SHA-256 `15e1fbb55f931b84e951a934fcc5dea39f0f779481f2eb22f2ccd0bdd9529d8b`; stock verifier from `850bee532621cdf5aca0fea142ef4364015007ad` only. 2026-11-27 05:09:24.716–05:11:49.796 +08:00, cold f2 duration 145.2284386 s, exit 0. 1959 forest leaves, 67 nested splits, 2089 direct including root, no prices. Prior proofs reused by exact identity, not rerun.

Full candidate data-only domain replay exit 0, exact root tail 112, 27 live even exponents. All 198 split domains including root (197 nested) and their first strict overflows independently match; full F4 counts 5513 forests, 5964 direct, 9542 incompatible finite cases, 7861 ECPP. Candidate covers `[2,4,8,16,28,30,36]`; with separate lead proofs only f10 remains. Strict lower proof bounds, inclusive finite budget and no divisibility/whole-key credit.
