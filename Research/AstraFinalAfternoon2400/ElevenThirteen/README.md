# Canonical roots 11 and 13 — partial proof packet

Frozen reference: `495c59f55456a70994ce7848487e0c4e262c1984`. The target is an odd perfect `N≤10^2400`. Root 11 excludes 19 and 7; root 13 excludes 19, 7, 11, 31. The frozen [projection](../../FinalNight2400/OpenFrontier.json#L293-L384) gives **9 shards / 11 exact keys / 7 singleton shards**. **No full exact key or shard is closed by this packet.**

| Shard | Key `(p,e)` | First forced pivot | Canonically live exponents | Raw strict size tail starts at | Certified complete fibers | Live remainder |
|---|---|---:|---:|---:|---:|---:|
| `P11_I00001` | `(11,4)` | 3221 | 211 | 683 | 42 | 169 |
| `P11_I00002` | `(11,6)` | 45319 | 98 | 514 | 21 | 77 |
| `P11_I00002` | `(11,48)` | 100641220283951395639601683 | 19 | 90 | 4 | 15 |
| `P11_I00005` | `(11,16)` | 50544702849929377 | 47 | 143 | 25 | 22 |
| `P11_I00006` | `(11,18)` | 6115909044841454629 | 37 | 127 | 15 | 22 |
| `P13_I00001` | `(13,2)` | 61 | 297 | 1343 | 51 | 246 |
| `P13_I00001` | `(13,8)` | 1609669 | 89 | 385 | 13 | 76 |
| `P13_I00002` | `(13,4)` | 30941 | 122 | 534 | 28 | 94 |
| `P13_I00003` | `(13,6)` | 5229043 | 50 | 357 | 13 | 37 |
| `P13_I00111` | `(13,612)` | anonymous 2265-bit `A` | — | — | — | [supplies `s≥537` excluded](HighLinear.md) |
| `P13_I00113` | `(13,618)` | anonymous 2287-bit `A` | — | — | — | [supplies `s≥537` excluded](HighLinear.md) |

The [coverage verifier](Coverage.py) binds the two frozen Git blobs (canonically normalizes CRLF before comparing full Git SHA-1), reconstructs the complete factorization of the nine small `A=σ(p^e)` and exact first domains, and prints the inherited support masks as diagnostics. In particular no historic support mask is needed for the 212 negative results. For the largest pivot a three-level Pocklington certificate binds all nodes. If `q|A`, let `c=v_q(A)`; then `p^e(A/q^c)q^f|N` for every `f=v_q(N)`. Enumerate from `f=c` to the first strict raw size exceedance, reject only forbidden factors, Euler incompatibility, too much flow into fixed exact rows, abundancy above two, or size of the fully stripped fixed remainder. At equality retain the state. The exact lists (not merely counts) are in [ForestCoverage.json](ForestCoverage.json).

## Forest certificates

[Forests.json.gz](Forests.json.gz) stores 212 rooted conditional forests and 92 bound ECPP chains. A leaf fixes the canonical root and its first-pivot valuation only. It does not assume a support mask, Euler location, complete factorization of the first-pivot sigma, or a particular sub-exponent. The frozen [Compose recurrence](../../Nov25/Compose/Compose.py#L54-L177) and the distinct frozen [direct recurrence](../../Session20261126/PivotCheck.py#L12-L43) both give `N>B`. For each candidate child verify the node labels are prime and the forest is acyclic and one-parent. A child activates only when its parent’s actual sigma has positive valuation there (recomputed, not inferred from the bank). Strip the support of explicit bases and the fixed remainder before multiplying outgoing anonymous charges; their product is a divisor of `N` by multiplicativity. At most one actual exponent is Euler, including the case Euler is outside the forest. Head exhaustion retains a monotone prime-power-only tail, not a finite-exponent assumption. Some integer floors equal 2400, but both unsimplified integer bounds are strictly greater than `10^2400`. The read-only WSL factor bank was used only by the discovery script, not during verification.

## High-weight Hensel regression

[AllLifts.py](AllLifts.py) independently reconstructs admissible congruence classes. For order `o`, weight `num/den`, and exact depth `z`, positive deficit requires `r^(den*(o−1))<p^(num*z)`. Intersect **every** lifted root progression with the independently provided inclusive size bound, strict integer degree-root bound and optional CRT constraints. The code checks the next level to ensure exact depth and deliberately fails closed instead of giving coverage credit if a resource cap is exceeded. It compares 180 exhaustive small-domain profiles with a brute-force implementation: in particular 29 at 13 and 83 at 19 both have exact order-3 depth one and positive deficit with weight 6 but are not their least residues. This addresses the mathematical defect described in [withdrawn PR #11](https://github.com/stormwhip/PerfectNumbers/pull/11), not that PR's result: **no withdrawn scope is reinstated**. Neither the conditional forests nor the anonymous upper-s proof uses high-weight Hensel pricing.

## Reproduction

Run from the repository root, without `-O`:

```
python -I -S -B Research/AstraFinalAfternoon2400/ElevenThirteen/Coverage.py
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/ElevenThirteen/ForestPacket.py
python -I -S -B Research/AstraFinalAfternoon2400/ElevenThirteen/HighLinear.py
python -I -S -B Research/AstraFinalAfternoon2400/ElevenThirteen/AllLifts.py
```

Local Windows CPython 3.11 replays exited 0. Forest pack generation and separate cold replay took 14.44 s combined; high-window replay took 139.76 s in a concurrent run. Counts are conditional; they do not change global `3029/3072` or the 43 open shards / 53 open keys.
