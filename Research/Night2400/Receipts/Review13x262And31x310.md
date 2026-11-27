# Lead — canonical (13,262) and (31,310), exact partial first fibers

**PASS both conditional packets.** Detached clean tracked `c8ce03ef7c2f5c1d85bc4ced37cc52e781e780a4`, CPython 3.11.9. From review root, replay each file with `python -I -S -B -X int_max_str_digits=0 Research/Night2400/VerifyFibers.py PACKET` and independently check domains with `python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/FiberPartition.py PACKET`.

- `Research/Night2400/Fibers13x262.json.gz`, SHA-256 `0f6195cd7468f1334fb07b2307a6a5da4c8ed1ba622bb8e70e3281e10dfcfc2d`; 2026-11-27 03:40:53.626–03:41:00.231 +08:00, 6.7685617 s, both exit 0. Complete 22/29, OPEN `[1,12,16,28,42,46,60]`; exact pivot 231050784610489 compelled with valuation one; strict tails 128(root),67, exact full sibling sets; 29 forest, 39 direct, 481 ECPP, no price. Canonical excludes 19/7/11/31.
- `Research/Night2400/Fibers31x310.json.gz`, SHA-256 `e2ee5e887691ca7ccf00042b6b70c3faa2d73201d60134ee7ca663f1cdd15985`; 03:41:00.443–03:41:17.185 +08:00, 16.742615 s, both exit 0. Complete 21/26, OPEN `[4,6,16,18,58]`; exact pivot 5691933643219 compelled with valuation one, strict tails `[117,77,65,50,42,54,46,99]`; 108 forest, 122 direct, 650 ECPP, no price. Canonical excludes 19/7/11.

Both exact domain replays require equality of internal sibling sets, and respect strict terminal bounds and first strict size overflow. Neither closes its key or shard, neither lifts by divisibility.
