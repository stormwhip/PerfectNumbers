# Exact closure of (19,316), shard P19_I00064

Assume an odd perfect number `N ≤ 10^2400`. The proof excludes **`19^316 ∥ N` without any support restriction**. It does not promote this to `19^316 | N`. The frozen [FinalSprint frontier](../../FinalSprint/Delta.json#L732-L740) has only actual exponent 316 left in this shard. No ledger is modified here.

## Cold replay

From the repository root, with Python 3.11+:

```powershell
python -I -S -B Research/Night2400/D/Verify.py
```

The [cold checker](Verify.py) uses only Python standard library, the frozen public source tree, and the [residual certificate](Pivot316Residual.json.gz). Packet SHA-256: `6a5f278ce8bca89a721078b2c19f3a80fbb52821bba8580b3539d235b590d58e`. Neither a factor database, the sparse ECPP directory, WSL, software for discovery, nor a preverified support ledger is needed to prove the result. The [historical pivot packet](../../FinalSprint/Support/Pivot316.json.gz) is input data, and all ten of its leaves are replayed, not trusted as historical verdicts.

## Complete support and valuation partition

Support bit order is `(19,7,11,31,13,3,5,17)`. The 57 projected masks divide into 36 historical masks and 21 residual ones. The certificate also covers all 71 masks outside the projection; this extra pass makes the exact-exponent claim independent of projection completeness:

| Coverage | Masks | Verifier action |
|---|---:|---|
| Historical part of the projection | 36 | Arithmetic prunes the raw pivot branches; all live ones use a replayed historical forest |
| Residual, pivot valuation 2 | 5 | 4 forests; mask 59 is excluded by `I(N) ≥ 2.020638` |
| Residual, pivot valuation 4 | 16 | 16 forests |
| Outside projection, historical forests or direct arithmetic | 36 | No new forest needed |
| Outside projection, root abundancy | 35 | Minimum bound at least `2.014197` |
| **Total** | **128** | Every S8 support containing 19 |

Residual `f=2`: `35,43,51,59,163`. Residual `f=4`: `69,71,77,79,85,87,93,95,197,199,205,207,213,215,221,223`.

Write `A = σ(19^316)` and `Q = 1255900817071954721881883552067931`. ECPP certifies Q, and `v_Q(A)=1`. Since `19^316 · (A/Q) · Q^f` divides N for its exact pivot valuation `f`, the monotone bound first exceeds `10^2400` at `f=50`. The checker tests every `1 ≤ f < 50`, including parity (`Q ≡ 3 mod 4`), forbidden support, known incoming overruns, exact divisibility-size bound, and partial abundancy. The only pivot values surviving these arithmetic filters on any mask are the 12 even values `2,4,6,…,24`. The historical forests exclude `6,8,…,24`; the residual subproofs exclude the remaining obligations at `2` and `4`.

Each forest is checked by the [primary integer recurrence](../../Nov25/Compose/Compose.py) and the [independent multiplicative recurrence](../../Nov25/Compose/IndependentForest.py). Both recompute sigma, permitted exponents, ownership, one Euler allowance, and size-only tails for every vertex; they require the exact integer lower bound to be **strictly** greater than `10^2400`. The minimum floor for the 20 new forests is 2404; for the old forests it is 2400 (the floor alone is insufficient). Incoming loads from the exact prefix are not charged twice. A forest label is a checked prime, but an edge is merely a candidate: it is used only if direct arithmetic proves that the actual emitter contributes a positive valuation. The root-abundancy branches take exact rational minima over all-even listed components and each permitted single Euler placement among them; an exterior Euler prime is covered by the all-even case, and its uncounted contribution only increases abundancy.

## Discovery recipe (optional, not proof)

The decisive change was the complete factorization of `σ(Q^4)`:

```text
5 × 11 × 761 × 232955070372754085071
× 255153692787972397812167227080247511906799034201829146831207531709920886827180456213124673685864777790858521
```

A bounded [ECM run](EcmF4.sh) extracted the 68-bit prime of the unresolved 425-bit cofactor; the other factor has 357 bits. Its two prime certificates are stored in [ECMF4.json](ECMF4.json) as discovery inputs and are included in the sealed packet. The extra two forced roots and witness-based forest refinement closed all `f=4` subcases; separate witness refinement closed the four `f=2` forest cases. No joint valuation pricing was needed. With the same fixed worktree and optional discovery DB:

```powershell
wsl --exec sh /mnt/e/PerfectNumbers/Research/Night2400/D/EcmF4.sh
$env:PYTHONPATH='E:/PerfectNumbers/Build/Night2400/Python'
python -B Research/Night2400/D/Search.py --index E:/PerfectNumbers/Build/Night2400/FactorData --mask 77 79 205 207 69 71 197 199 85 87 93 95 213 215 221 223 --rounds 25 --smooth 24
python -B Research/Night2400/D/Search.py --index E:/PerfectNumbers/Build/Night2400/FactorData --mask 35 43 51 163 --rounds 20 --smooth 26
python -B Research/Night2400/D/Pack.py
```

The ECM program can exit 1 on factor discovery; its output must be checked by exact multiplication and prime-certificate replay, not by its status. [Search.py](Search.py) writes only ignored `trials/` outputs. [Pack.py](Pack.py) tries local frozen Git blobs first, invokes PARI only for missing chains, and verifies all used prime labels before serialization. The sealed new packet contains 529 ECPP labels including inherited reused labels; 61 chains were newly generated by pack, in addition to the two ECM-derived factor chains.
