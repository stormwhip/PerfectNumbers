# Night2400 C5 — conditional fibers of (13,372), P13_I00073

From the repository root, with standard-library Python and assertions enabled:

```text
python -I -S -B Research/Night2400/C5/Verify.py
```

This packet covers only odd perfect numbers `N <= 10**2400` in the inherited root-13 class (19, 7, 11, 31 absent), with `13^372 || N`. The 69-bit prime `Q = 438552673580231875649` is ECPP-certified and checked to divide the forced cofactor. The raw bound first exceeds `10**2400` at exponent 78; the checker separates 29 incompatible and 23 direct exponents below that tail, leaving 25 first fibers. **Full-fiber coverage of this packet** is exactly **1, 4, 6, 8, 16**, not the entire key or shard. Of the seven delegated fibers, **2 and 12 remain open**. Fiber 2 is additionally excluded on five canonical support masks, `16,80,144,208,240`, leaving only `48,112,176` there. The other 18 first fibers are outside this packet.

| Exact `Q` exponent | Method | Forest leaves / splits / direct subcases | Minimum forest floor |
| --- | --- | --- | --- |
| 1 | Exact exponent tree | 62 / 3 / 66 | 2401 |
| 4 | Exact exponent tree | 11 / 2 / 15 | 2403 |
| 6 | Exact exponent tree | 70 / 3 / 74 | 2401 |
| 8 | Exact exponent tree | 1 / 1 / 2 | 2457 |
| 16 | All eight support masks on 3, 5, 17 | 7 forests, 1 exact abundancy exclusion | 2404 |

Each split regenerates all compatible children and proves the monotone tail. Both integer recurrences verify every forest above `10**2400`. At exponent 8, bounded ECM split the previously unknown relevant cofactors. The checker certifies the 355-bit forced prime `49878608039259205967178870556535925590313831061118822840556903751765122818345190074015404087188641910497263`, then finds its only live exponent is 6 (10/12 direct, 1–12 scanned, with the size tail from 13; incompatible exponents are rejected by parity or inherited absent-prime conditions). Six forced forest roots and no ownership edges close that sole child. At exponent 16, all masks are replayed without trusting any support projection; mask 240 is excluded using exact minimal abundancy.

| Packet | SHA-256 |
| --- | --- |
| [Fibers 1,4,6](Fibers13x372.json.gz) | `8cf67c23f0a3aa1d10c4773ef59cce4d141b35aa57f61dadac6643aba458ec7c` |
| [Fiber 8](Fiber8.json.gz) | `89ab2b0f89c9a177c7cf95134069a43565304e93160907fa61ef9f265694572a` |
| [Fiber 16](Support16.json.gz) | `ffa5a3f1d0eec87ff9c5aa1d8ec91c87dbe88b6ca6b907fe17061fbccd2e3434` |
| [Five masks at fiber 2](Support2.json.gz) | `c37a5e66c1203a91a5bc4f0cd0ceb83664a8c1bbe271224ded6312f93b206fd1` |

The official discovery index, bounded scout, ECM, and PARI are discovery-only. Replay needs none of these, no generated caches, and no other Night2400 candidates.
