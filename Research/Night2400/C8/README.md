# Night2400 C8 — (31,352), P31_I00069

Offline from the repository root with standard-library Python and assertions enabled:

```text
python -I -S -B Research/Night2400/C8/Verify.py
```

Assume odd perfect `N <= 10**2400` in the inherited root-31 class (19, 7 and 11 absent), and `31^352 || N`. The certified 41-bit prime `q = 1797674429773` divides the forced prefix. The verifier rebuilds the first split: 31 compatible live exponents, 33 direct exclusions, 47 incompatible exponents, and a monotone size tail starting at 112.

**Strict coverage is 17 complete first fibers**, not the entire key or shard:

- **2** uses all 16 independent masks for 13, 3, 5 and 17, including masks absent from inherited projections. Eight are directly contradictory, two are strictly abundant, and six have dual forest bounds with minimum decimal floor 2401.
- **4, 6, 10, 30, 33, 45, 48, 50, 54** use one certified extra forced prime and a complete exponent split. The verifier checks every compatible child, all direct siblings, and the tail. In particular exponents 30, 50 and 54 have no surviving children. Other children use both integer forest recurrences.
- **25, 37, 38, 40, 42, 46, 52** use the [exact prefix price](PrefixPrice.py), reproduced locally for standalone replay. Its transferable condition is `r^f/gcd(r^f,C) <= floor(10^2400/(X C))`: it charges only the part beyond the already forced cofactor and applies without factoring `C`.

**Open first fibers:** 1, 12, 13, 14, 16, 18, 20, 21, 22, 24, 28, 32, 34, 36. For exponent 1 the weak-support pilot still leaves all 16 masks open, and even the ideal two-target price has floor 1587. None of these fibers is credited by the candidate.

| Packet | SHA-256 |
| --- | --- |
| [Forced split forests](Fibers31x352.json.gz) | `bd5b58aeafe8101f3f63f27d4254980c867e392022a7f16600c65a5d0e07339d` |
| [Fiber 2 support masks](Support2.json.gz) | `d6c193bcb9dbdcb751cf3b8a17a736f95b8973238fbab4e51199f542bfe1a185` |

The official factor index and PARI are discovery-only. All required primality chains are included; no discovery cache, network, or another Night2400 packet is used during replay.
