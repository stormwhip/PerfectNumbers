# F4 — (19,282), incremental exact first fiber 16

**PASS incremental.** Candidate `2251e5e8603e2edf82389d4f4d07a65716e9fef9`, detached clean tracked files, CPython 3.11.9. Complete candidate packet SHA-256 `4cde99ecee143874fa6609c5858bb9c5f83673ee213c619c452ddd433beeefde`. Prior independently cold-replayed `53ee0eb410846f0e0eb8afe38650f75e0db58be8` packet SHA-256 `1823c62fd811f8fb0e95202ec02397b11992b1f4b365d4b172892eeca39a0ae8` was materialized from its Git blob as `Research/Night2400/F4/ReviewOldPacket.json.gz` solely for comparison.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/F4SixteenDelta.py Research/Night2400/F4/ReviewNewFiber16.json.gz
python -I -S -B -X int_max_str_digits=0 Research/Night2400/VerifyFibers.py Research/Night2400/F4/ReviewNewFiber16.json.gz
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/FiberPartition.py Research/Night2400/F4/Fibers19x282.json.gz
```

The extraction script asserts exact key/pivot, equality of all old subtrees and old ECPP entries, and that the only new first case is `16` and every new ECPP chain is reachable from it. Delta used 2512 chains, with 1732 newly embedded; extract SHA-256 `0bc3c637c77acef0d36fd13b3caf5bf1c7504f6f97843f4a883120186eeae42c`. Extracted f16 cold replay 2026-11-27 04:39:10.801–04:40:32.115 +08:00, 81.520079 s, exit 0; 1,252 forests, 45 nested splits, zero prices. All other commands exit 0. Independent full-candidate arithmetic rederived compelled pivot valuation one, strict raw root tail 112, 27 live even exponents, and all 131 split child sets with strict monotone tails (root included), 3554 forest leaves, 3903 direct and 6328 incompatible cases. All 5046 embedded ECPP are partitioned into old and independently replayed new. No old forest was assumed without its prior cold receipt; old trees were deliberately not rerun.

Complete F4 coverage `[4,8,16,28,30,36]`; with the previously verified lead complementary subset, **25/27**, globally OPEN `[2,10]`. No full key/shard or divisibility credit.
