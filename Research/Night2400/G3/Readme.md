# Two new complete first-pivot fibers at (7,438)

For an odd perfect `N ≤ 10^2400` with `19 ∤ N` and `7^438 ∥ N`, the [certificate](Seven438.json.gz) excludes `v_Q(N)=2` and `v_Q(N)=16`, where `Q=572749682520506652634407616247`. No additional support condition is imposed. This is partial; it does not close `P7_I00084`. Together with the six earlier first-pivot fibers at frozen handoff `1cf13e79`, the open valuations are `10,12,18,22`. This directory does not modify a ledger.

```powershell
python -I -S -B Research/Night2400/G3/Verify.py
```

The [cold checker](Verify.py) uses only the standard library and existing public proof arithmetic. It does not load the handoff tree, ECM executables, factor dictionary, or discovery outputs. New packet SHA-256: `86801a494e509019196ec3a69a4c297bf64f3c33b4405dfe1c44dea27a3e506b`.

## Coverage

The independent domain checker proves Q prime and `v_Q(σ(7^438))=1`. The root split requires `19` absent, tests Euler parity, incoming oversupply, forbidden divisors, the exact product divisibility bound, and partial abundancy. The live root valuations are `2,4,6,10,12,14,16,18,20,22,24,28`; the first monotone size-only tail value is 57. The second recurrence, [PivotCheck.exact_leaf](../../Session20261126/PivotCheck.py), and [Compose](../../Nov25/Compose/Compose.py) must both give a strict integer product greater than `10^2400` for each forest. A reported decimal floor of 2400 is never sufficient on its own.

| Exact first pivot | Forests | Nested splits | Direct contradictions inside nested splits | First size-only values at nested splits (preorder) |
|---|---:|---:|---:|---|
| 2 | 86 | 5 | 129 | 42,70,83,51,177 |
| 16 | 22 | 1 | 29 | 103 |

The newly solved paths for `f=2` set the subsequent exact valuations of `1736025745269326566865242460701882510513` and `41375431991085967` to 6, then that of `529749166171` to 4 or 6. Those for `f=16` set the exact valuation of `18220567` to 2 or 30. All their other feasible siblings are present in the certificate. In particular these are exact assignments, not divisibility lifts.

## Discovery and remaining work

Support splitting would have left substantial domains: the four deep holes had 8, 24, 11 and 27 live projected masks respectively after direct arithmetic and minimum abundancy. Some masked variants closed, but the more effective route was a deterministic short [ECM search](Ecm.sh) and [witness follow-up](EcmWitness.sh). At `f=2` these found the 58-bit factor and 267-bit prime cofactor in the `41375431991085967` emission, and a 38-bit factor in the `529749166171` emission. At `f=16`, a 41-bit new factor helped close the exponent-30 split; recurrent witness emission factors (including `22519488005494943`, `710412610294973` and `1090834951`) closed exponent 2. The discovery code [Search.py](Search.py) and [Seal.py](Seal.py) are optional and read authorized discovery resources only; cold replay uses the complete sealed tree and checks all prime labels. Brief probes for `f=18,22` did not close those branches (forests of floor 1953,2019); no claim is made for them.
