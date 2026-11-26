# Canonical (19,30): ordinary partial plus three conditional full masks

Clean detached `4ce99bab0a04baaba6028601033c3ccf8a50164b` in `E:\PerfectNumbers-Night2400-reviewa`. Only `Research/NightOrder/ECPP/` sparse-excluded; no author cache or reserved folder used. Python 3.11.9. Scope is an odd perfect number `N≤10^2400`, exact `v_19(N)=30` and canonical root 19, with additional presence/absence stipulated by the respective mask only.

SHA-256:

```text
bfe6c3d9f0147189536b9e1cd69fac55d7e0d92e1be37b418da52d09f1f708f2  Research/Night2400/Mask19x30.py
da990213ce827464d480a9d37423195d5197375e0f385433bb571b92f6395c04  Research/Night2400/Fibers19x30.json.gz
b441659c4610a2994d1c59f65e9945dd39bfa112c411a2fedb956f2c133b0181  Research/Night2400/Masks19x30.json.gz
7f652874ac1c3bef9f7da6b2c230b471f438e7163c83af583129f3db5dafe080  Research/Night2400/VerifyFibers.py
```

```text
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Mask19x30.py
python -I -S -B -X int_max_str_digits=0 Research/Night2400/ReceiptsA/Mask19x30Scope.py
```

Candidate cold replay: 2026-11-27 04:58:11.6039905 → 05:02:17.8487590 UTC+08:00, stopwatch 246.233828 s, exit 0. Independently rederived the ordinary domain and each conditional domain, exit 0. The standalone audit reuses the preserved integer domain routine in reviewer snapshot `2a0f5152dd796dbf1a2dfdcd291b54ef6ae0389c`, not candidate imports. It also verifies that each of the nine masked forests explicitly includes all stipulated present primes as roots.

Ordinary pivot `243270318891483838103593381595151809701`, 19/23 covered, unresolved `[1,2,12,18]`, size tail 62, 301 ordinary ECPP entries. Within every listed mask, forbidden-emission testing eliminates ordinary residual exponent 2; the exact residual complement `[1,12,18]` is closed by three forests per mask. Both candidate forest recursions must prove a strict integer threshold, not merely the reported floors. 325 ECPP entries in the mask packet.

| Complete mask | Present beyond 19 | Absent within the mask universe | Minimum second forest floor |
| --- | --- | --- | ---: |
| 21 | 11, 13 | 7, 31, 3, 5, 17 | 2408 |
| 89 | 31, 13, 5 | 7, 11, 3, 17 | 2403 |
| 153 | 31, 13, 17 | 7, 11, 3, 5 | 2414 |

No assertion is needed about the historical support projection: this validates these explicit masks only, with arbitrary primes outside the mask universe. No newly closed root exponent or shard.
