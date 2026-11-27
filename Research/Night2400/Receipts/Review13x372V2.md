# Combined lead + C5 — full exact first fiber 2 at canonical (13,372)

**PASS all eight canonical masks at first-pivot `f=2`; across earlier separately replayed packets 24/25 root fibers, only `f=12` OPEN.** No full exact-key or shard credit yet. CPython 3.11.9; separately detached clean tracked candidates, no author caches.

| Candidate | Input SHA-256 | Cold coverage | Elapsed |
|---|---|---|---|
| `4011372f36650ad2dae51172f05bc7ed4b18b810` | `e3ae8cebde61856b130b0f6fee803699a3871b9dcf68e72864392ecba9d9ce80` | masks 48,112,176; 34 forests and 2 rational abundancy checks | 10.3905284 s |
| `0824d5cf1060313417ddf4913e0eb80a428aa6a5` | `c37a5e66c1203a91a5bc4f0cd0ceb83664a8c1bbe271224ded6312f93b206fd1` | masks 16,80,144,208,240; 4 forests and 1 rational abundancy check | 11.7430901 s |

First command exit 0, 2026-11-27 01:04:22.908–01:04:33.155 +08:00:

```powershell
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Masked13x372.py Research/Night2400/Masked13x372V2.json.gz
```

Second command ran exactly the new support routine, not the unchanged already-replayed trees; exit 0, 01:05:15.982–01:05:27.569 +08:00:

```powershell
@'
from pathlib import Path
import sys
p=Path('Research/Night2400/C5').resolve();sys.path.insert(0,str(p));from Verify import support
support(p/'Support2.json.gz',2,(16,80,144,208,240))
'@ | python -I -S -B -X int_max_str_digits=0 -
```

Canonical root 13 excludes earlier bases `(19,7,11,31)`, fixes 13, leaves the three bits `(3,5,17)` unconstrained; the two disjoint sets exhaust exactly `16+32i` for `0<=i<8`. The 3-mask proof uses a fresh prime `1451320277645395737847≡3 mod 4` with incoming valuation 1. Independent geometric sums reproduce the same 12 live secondary exponents `[2,8,10,12,16,18,22,26,28,30,32,36]` on each mask, 13 direct and 47 illegal before strict raw tail 73. All live secondary child sets are exact matches; minimum forest floor 2401, 247 embedded ECPP. The five-mask proof instead handles the entire exact state per mask, no secondary truncation; forests have floors 2406/2403/2430/2406, and mask 240 has strict rational `>2`. Both use the established scoped two-recurrence forest accounting and strict integer comparisons. This coverage composes with the earlier exact tree partitions only because they use the same pivot, exact root key and canonical absence assumptions.
