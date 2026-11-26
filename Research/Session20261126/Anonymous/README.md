# Anonymous cyclotomic valuation guards (partial results; no new closed exponents)

This 0.81 MB proof packet is relocatable and contains the ten compressed small-root witness lists, exhaustive CRT premium checker, ordinary prime-count corollary and five scalar obstruction examples. `AnonymousGuard.md` explains the theorem, its limitations and the arithmetic. Run the following inside this directory, replacing REPO with the read-only fixed checkout at 2889e47f:

```
python -I -S -B AnonymousGuard.py REPO verify
python -I -S -B ExceptionalCube.py 100000
python -I -S -B ManySuppliers.py
python -I -S -B CountGuard.py REPO
python -I -S -B Bottlenecks.py
```

No third-party dependency for verification; FLINT is optional only for regenerating the 268 short-polynomial witnesses. Frozen primitives are Research/NightMerge/LatticeLeaf.py SHA256 f8d2dfd6da576fcfe328d3e36dcd4159060802407fd026367350f06ebb137954, and Research/EulerOneSieve/TeichmullerBaseline.py SHA256 84cdab409bbce2745a9d1124c1e93e7b01fa20b30b1eee2dd6072d4ba2d3c73b. These two primitive files are imported from REPO; no writes to checkout. Expected outputs are beside scripts. None of the five scalar witness parameterizations constructs an odd perfect integer or claims to realize unknown A factorization; the Euler prime itself is certified, while the emitter and sharing of A-supply are relaxed.
