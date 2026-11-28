# `(19,222)`: second independent forest overlay

Frozen canonical key `(19,222)` at `495c59f55456a70994ce7848487e0c4e262c1984`. All listed powers are exact. Use first pivot `t=7579985624053` with exponent `f` and second pivot `r=3705121363` with exponent `g`. After the frozen Thirds coverage, Gemini, and [Forest222](Forest222.md), this supplemental packet excludes:

| `(f,g)` | third prime | newly closed third values | remaining values | strict raw tail |
|---|---:|---|---|---:|
| `(1,2)` | 3789992812027 | 2, 4 | 16, 18 | 144 |
| `(2,2)` | 2032322226061 | 4, 18 | none | 145 |
| `(2,46)` | not needed | entire second prefix | none | not split |
| `(18,2)` | 108501737266216818637411 | 2, 12 | 4, 6, 10 | 60 |

This adds seven strict terminals, including six distinct third prefixes and a direct second-prefix witness. The union completes **two whole second prefixes** `(f,g)=(2,2),(2,46)`; these are not counted as two additional terminal witnesses. Under first exponent `f=2`, the exact second values `g=16,22` still remain, hence this package closes no first fiber, whole key, or canonical shard.

The verifier re-enumerates every original relevant exact domain and its strict monotone bare-size tail. It verifies that each new row is in the set difference after frozen exclusions and previous overlays, then checks the two independent exact unrestricted-Euler forest recurrences and compares both unrounded integer lower bounds strictly to `10^2400`. [The first-stage proof](Forest222.md) documents the same forest's no-double-counting, all-Euler-locations and tail invariants. The bundled deterministic prime evidence is 255 ECPP and 22 Pocklington cells; both prime-evidence sets are checked exactly against the cells used. The Pocklington helper requires complete verified factors of a sufficiently large divisor of `n−1` with explicit gcd witnesses; neither the factor service nor discovery software is used for replay.

SHA-256 [Forest222Stage2.json.gz](Forest222Stage2.json.gz) `10688cbd5ecab9ca8fbd88ffc3c61a454f86febcdac43289359685a037f6dae0`. [Verifier](VerifyForest222Stage2.py) isolated command exited 0:

```text
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Nineteen/VerifyForest222Stage2.py
```

The original [Forest222 checker](VerifyForest222.py) should still be run separately when accepting the union. No PR #11 method or results are used.
