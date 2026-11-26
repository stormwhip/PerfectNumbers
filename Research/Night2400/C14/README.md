# Night2400 C14 — (19,312), P19_I00063

Offline at the repository root with standard-library Python and assertions enabled:

```text
python -I -S -B Research/Night2400/C14/Verify.py
```

For an odd perfect `N <= 10**2400` with `19^312 || N`, the ECPP/deterministically certified prime `q = 1481866508237449` is forced. The first split has 40 live exponents, 40 direct exclusions, 26 incompatible exponents, and a monotone tail at 107. The packet closes **only exact first exponents 8 and 36** and does not replay the other independent first-fiber certificates or a prior verdict.

- **8:** 3 complete splits and 57 direct cases, with 53 dual integer forests and one exact all-support subleaf. The latter is `(312,8,6,2,2)` (exponents in path order). It examines all 128 masks containing 19 over `(19,7,11,31,13,3,5,17)`: 96 direct conflicts, 26 strict rational abundancy proofs and 6 dual forests.
- **36:** one complete split with 25 direct cases, 24 dual integer forests and the prefix-aware joint-price leaf `(312,36,30)` at target indices `[0,1]`, receipt `(10,[7476,3792,0])`. Every compatible exponent at the 160883 split, including both formerly unresolved children, is covered.

| Packet | SHA-256 |
| --- | --- |
| [Exact fiber 8](Fiber8.json.gz) | `3a0ea6297c7ad999eafb5ca4cb2f302e380fd3189e49ef64852ce21d6eef5b75` |
| [Exact fiber 36](Fiber36.json.gz) | `0cf4fadc039684f114af89d36cdd181393ad1aa30a8d09eee7acfed9de9c128d` |

The [prefix price](PrefixPrice.py) includes the exact LCM budget for a hypothetical supplier and is held locally for standalone replay. The factor index, PARI, shared discovery files, generated caches and other Night2400 packets are not used by replay.
