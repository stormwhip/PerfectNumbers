# (7,732): complete exact first-pivot cover for P7_I00129

The forced first pivot is `564817549`. The domain has 44 live exact
exponents, with the monotone size tail starting at 134. Only the complete
packet is retained here. In the first fiber 42, its second exponent
`348559^30` is excluded by joint price targeting the two initial components,
with 128 blanket exceptions and Euler-window counts `[20333,9384,1069]`.

## Complete certificate

[Complete packet](Fibers7x732Complete.json.gz), SHA-256
`69eaf78fb475799a4300a8c826cbedf58a36a2a0a6ed6fb70936cd5cf702d1fa`, includes
all 44 first fibers, with 2,989 forest leaves, 78 inner splits, one price
leaf and 13,822 ECPP chains.
The nontrivial first fibers' second partitions are listed below. Each
second pivot is initially compelled to valuation one. The live case
count is shown; replay recomputes the exact sibling lists and all
immediate or deeper tails.

| First exponent | Second pivot | Live cases | Size tail starts |
| ---: | --- | ---: | ---: |
| 1 | `1026941` | 48 | 194 |
| 2 | `155701973893` | 34 | 103 |
| 4 | `1544868523952944283509860181` | 14 | 42 |
| 6 | `32871726687193746147590911542407649424943089` | 6 | 26 |
| 16 | `10711` | 55 | 223 |
| 18 | `7130958097` | 31 | 88 |
| 28 | `233` | 96 | 289 |
| 30 | `3790156163` | 15 | 69 |
| 42 | `348559` | 17 | 80 |
| 58 | `6835033` | 5 | 24 |

The last two conditional paths, both in first fiber 28, were closed by
single-root forests. The path with `233^112` uses the 881-bit prime
`σ(233^112)`, floor 2511. The path with `233^1,13^282,3^2` uses the
1044-bit prime `σ(13^282)`, floor 3289. Both prime claims are checked
using the embedded ECPP chains, not a probable-prime flag. The discovery
prime-size cap had hidden these two simple roots in earlier passes.
No divisibility lift or ledger edit is made here.

```powershell
python -B -I -S -X int_max_str_digits=0 Research/Night2400/VerifyFibers.py Research/Night2400/E7/Fibers7x732Complete.json.gz
```
