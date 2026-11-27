# Night2400 C4 — (19,82), P19_I00021

Offline, from the repository root with standard-library Python and assertions enabled:

```text
python -I -S -B Research/Night2400/C4/Verify.py
```

The [packet](Fibers19x82.json.gz) has SHA-256 `aec8f229f79c35290939d85e1b5db0ff3cc0bcf7bb2fabba0ead3cb7d7ee9265`. It pertains only to odd perfect `N <= 10**2400` with `19^82 || N`. Its certified 342-bit pivot is `4555750199199950437649290574576123158785621674690043100726048398827989978120480865989375363338094993243`, with valuation one in `sigma(19^82)` and residue 3 mod 4. The raw prefix-only size scan stops at 23; odd exponents up to 21 are Euler-incompatible, even exponents 12–22 are directly excluded, and all exponents at least 23 are too large. Of the five surviving even exponents, this packet closes **2, 4, 8, 10**. Only **6** remains, in 84 support masks listed by the verifier. There is no whole-key or shard closure and no lifting to other actual exponents.

For pivot exponents 2, 4, 6, 8 the verifier rebuilds all 128 masks on `(19,7,11,31,13,3,5,17)` containing 19, without trusting the projected support ledger. Direct arithmetic checks conflict/size/abundancy. The explicit support abundance check minimizes the necessary exact rational abundancy over the all-even choice and each single possible Euler assignment among the listed forced/supported primes. Both [forest](../../Nov25/Compose/Compose.py) and [independent forest](../../Nov25/Compose/IndependentForest.py) recheck every remaining sealed forest, including its tails. Pivot exponent 10 uses the [joint price](../../FinalSprint/JointValuation.py) at `19` and the pivot with receipt `(7, [629, 2, 199])`, regardless of support.

| Exact pivot exponent | Direct masks | Abundancy masks | Dual forest masks | Open masks |
| --- | ---: | ---: | ---: | ---: |
| 2 | 64 | 42 | 22 | 0 |
| 4 | 64 | 24 | 40 | 0 |
| 6 | 0 | 44 | 0 | 84 |
| 8 | 64 | 42 | 22 | 0 |

Discovery used the official data-v1 Finder with witness-guided ownership growth; PARI supplied ECPP certificates. Neither discovery nor the C/C2/C3/D packets run during replay. A bounded ECM trial extracted the 49-bit prime `461874284924809` on pivot exponent 6, but left a 1991-bit composite and did not reduce the 84 unresolved masks; the factor is not needed by this packet.
