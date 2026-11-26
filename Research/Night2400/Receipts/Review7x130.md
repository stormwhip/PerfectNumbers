# E — (7,130), five conditional exact fibers

**PASS conditional `[1,2,8,9,10]`; OPEN `[4,6]`.** Detached clean tracked candidate `c1e8bae6ccb5c7b947022b78f1afab64da5ade15`, CPython 3.11.9. Compressed SHA-256 `0c77d6471930aeff690e7d01891b556c244eadf3adf28db0919ca734915330e6`.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/Night2400/E/Verify130.py Research/Night2400/E/Conditional7x130V128910.json.gz
```

Integration renamed the original packet `Conditional7x130-128910.json.gz` (same compressed bytes).

Start 2026-11-26 23:57:33.609 +08:00; end 23:58:23.447 +08:00; elapsed 49.9478482 s; exit 0. No author caches. The four exact forests for `1,2,8,9` have replay floors `2407,2419,2608,2514`; both integer evaluators use strict `>10^2400`. At `10` the price receipt is `(0,[8,0,2])`. Embedded ECPP entries 150.

Independent arithmetic used only the compressed packet and stdlib: the 366-bit pivot has valuation 1 in the fixed source; the parent size bound keeps all raw exponents through 20 and strictly exceeds at 21, bounding the monotone tail. Under canonical root 7 (19 absent) and the Euler placement rule, inadmissible exponents are `[3,5,7,11,15,17,19]`. Exact structure, size, incoming valuation and partial-abundancy tests remove `[12,13,14,16,18,20]`; the exact domain is `[1,2,4,6,8,9,10]`. All root siblings are represented; explicit `open` terminals carry no mathematical exclusion, so `CONDITIONAL_ONLY` is correct. No nested splits occur in this packet. The result is not a full `(7,130)` or shard exhaustion.
