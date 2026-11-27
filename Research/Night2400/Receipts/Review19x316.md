# D — exact (19,316), complete mask partition for P19_I00064

Candidate `700d089093a20dca10d30eab5a97bc7aa4a22523`, detached, clean tracked files; CPython 3.11.9. SHA-256 for `Pivot316Residual.json.gz`: `6a5f278ce8bca89a721078b2c19f3a80fbb52821bba8580b3539d235b590d58e`.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/Night2400/D/Verify.py
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/Partition19x316.py
```

**PASS, complete exact (19,316), all 128 masks, no open fibers.** First command started 2026-11-26 23:50:23.929 +08:00 and ended 23:54:14.748 +08:00; elapsed 230.9127337 s, exit 0. It replayed 529 new packet ECPP chains and reported minimum floor 2404 for new forests and 2400 for historical forests.

The independent arithmetic partition replay (second command) passed in 0.2480227 s. It imports no proof code. Uses exact integers and rational abundancy; the candidate separately certifies prime labels and both forest recurrences. No author cache, builder, external factor database, or historical verdict is used.

- Support order `(19,7,11,31,13,3,5,17)`: fixing 19 leaves exactly all 128 odd masks in `[1,255]`. The 57 projected masks split into 36 historical and 21 residual. For the 71 exterior masks, 36 use historical forests or direct exclusions and 35 use independent root-abundancy. Outside projection is not assumed excluded by the baseline.
- At `Q=1255900817071954721881883552067931`, `Q≡3 mod 4` and compelled `v_Q(σ(19^316))=1`. Raw divisibility bound `19^316·(σ(19^316)/Q)·Q^f` is at most `B` through `49` and strictly above at `50`; everything afterwards is larger. Odd exponents are not possible for this pivot. Exact incoming-overrun, full divisibility-size, partial-abundancy and forbidden-support tests yield the globally legal superset `[2,4,6,...,24]`, with individual masks filtered further. No equality at `B` or abundancy 2 is rejected by the proof.
- Ten historical forests at `[6,8,10,12,14,16,18,20,22,24]` are replayed without extra mask assumptions, so justify their reuse. The residual obligations are five masks at `f=2` (four forests, one abundancy) and sixteen at `f=4` (sixteen forests). Exact test for mask 59 gives floor 2020638 ppm and the 35 exterior root abundancy tests have minimum floor 2014197 ppm. Each applies monotone `σ(r^a)/r^a` to least legally permitted exponents; an exterior Euler prime retains the all-even case, while one listed Euler prime can be considered in only one place. Omitted components can only increase the rational abundancy.
- `Compose.Forest` and `IndependentForest` both validate scoped compelled roots, prime labels, unique noncyclic private owners, and pay only positive checked edge loads; the residual anonymous cofactor is not factored. At most one Euler location is allowed. Each local tail is bounded by its own monotone prime power and any omitted factors are at least one. Both recurrences require strict integer `>B`; the reported decimal floor is only diagnostic.
- `FinalSprint/Delta.json` frozen row for `P19_I00064` has existing `remaining_actuals=[316]`. This proves exhaustion of that residual shard, not the stronger divisibility predicate `19^316 | N`, and does not change a ledger.
