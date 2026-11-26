# F2 — complete exact (19,238), P19_I00050

Detached clean tracked candidate `18d1aad0ae80a4d474c9cfa1dc8a938e3d025dbf`, CPython 3.11.9; gzip SHA-256 `cf38a926adfcfdf75674b4e8c524d89cf8d6661da908893ff9df9bbbe475fd2d`. No author data, caches, or discovery tools. Frozen source identities for JointTree, JointValuation, PivotCheck, Compose, ForestReplay and PrimeCheck all match base `49b19bbdf6c46ac3cdd4cb0da2b6b08e1360fdec`.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/FinalSprint/JointTree.py Research/Night2400/F2/JointTree19x238.json.gz
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/FiberPartition.py Research/Night2400/F2/JointTree19x238.json.gz
```

**PASS COMPLETE, 9/9 first fibers; zero OPEN.** Cold replay 2026-11-27 03:13:58.305–03:26:27.003 +08:00, elapsed 748.7115627 s, exit 0. Frozen output `(19,238,[10385,354,11062,1], [...,(4,[4287,15,0])])`, matching the independent domain audit and proving the sole price leaf was executed.

Independent integer audit exit 0, elapsed 8.2056861 s. First pivot `606492758240679674698864343145363724798136175178043`, compelled valuation 1, `3 mod 4`; all nine even first exponents 2–18 present. Before raw monotone tail 37, the 18 odds fail Euler parity and the nine evens 20–36 fail exact-state arithmetic. All 354 split domains and first strict overflow endpoints were rebuilt with equality at B retained; exact live child sets match everywhere. Audit counts 10,385 forest, 11,062 direct, 18,156 incompatible, one price, zero OPEN; 15,598 embedded ECPP labels.

The sole price is the exactly fixed prefix `[(19,238),(606492758240679674698864343145363724798136175178043,18)]`, targets `[0,1]`. Frozen `JointTree.py` executes `JointValuation.excludes` by default; no structural-only mode was used. Forest leaves require both independent integer recurrences strictly above B. The mathematical result exhausts the frozen `P19_I00050` residual singleton `[238]`, not a blanket divisibility lift to another actual exponent.
