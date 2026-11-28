# `(19,222)`: third forest overlay, with new large certified root factors

Frozen main `495c59f55456a70994ce7848487e0c4e262c1984`. For exact `19^222,t^f,r^g,q^j`, `t=7579985624053` and `r=3705121363`, this packet excludes:

| `(f,g)` | tertiary q | newly excluded j | remaining j | raw tail |
|---|---:|---|---|---:|
| `(1,2)` | 3789992812027 | 18 | 16 | 144 |
| `(2,16)` | 2032322226061 | 2,4,18,28 | none | 123 |

The latter whole second prefix follows after adding the separately verified [j=1 inert obstruction](Proof.md). With the first two forest overlays, `f=2` has only second exponent `g=22` left; this does not close any first fiber or complete key.

Both independent exact forest recurrences must give a strict value >`10^2400` at each leaf. The verifier recomputes every relevant raw exponent recurrence and the surviving frozen window, then removes precisely the older overlay cuts. The forest handling of Euler alternatives, distinct factor mass, activation and raw tails is the same as [the first forest overlay](Forest222.md). Newly found large factors remain merely untrusted labels until the supplied ECPP chains and actual divisibility are verified. No factor service or PARI is needed to replay.

[Verifier](VerifyForest222Stage3.py) cold replay exited 0: five terminals, 66 ECPP chains and five Pocklington records exactly consumed. [Forest222Stage3.json.gz](Forest222Stage3.json.gz) SHA-256 `a0082daac618fe518eb7365058024616168788abd9fd46a41d89000893a8acae`.

```text
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Nineteen/VerifyForest222Stage3.py
```
