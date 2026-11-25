# Exact Euler location as an exhaustive partition: `(7,700)`

For the canonical scenario, `7^700 || N` and `19 ∤ N`, set `A=(7^701−1)/6` and let `E` denote the unique Euler prime. The root itself is ordinary. Partition the problem into five pairwise disjoint cases, the four exact possibilities for `E` below and their complement. This is not the assumption that a forest contains the Euler prime: the last class includes **every prime outside the graph**.

| Euler case | Lower decimal floor |
|---|---:|
| All primes other than the four below | 2400 |
| 11777 | 2404 |
| 194674901 | 2403 |
| 3680030201 | 2446 |
| 4751504889569509596346336866349490924895794713 | 2430 |

The first row is a *strict* full-integer comparison, not acceptance from a decimal floor of 2400. In that case allow the Euler coupon at any other possible emitter; disallow it only at the four listed primes. The directed forest minima include the possibility that no activated emitter spends the coupon. On each of the other four branches the nominated `E=q` is **forced independently of its former parent**: delete its incoming ownership edge, make it a root, and put `q` in the stripped support. If `q` divides `A`, remove its old `q`-power from the base product before replacing it by `q^f` (`f≥v_q(A)`, `f≡1 mod 4`); otherwise the baseline exponent at this new root is one. Every other component is ordinary. Such re-rooting is valid only inside this positive branch. Every final graph is checked for acyclicity, reachability, primality and actual divisibility. The product of stripped outputs is safe by the ordinary forest proof. Together the five integer bounds exclude the canonical exact pair. No tail is skipped: each exponent prefix is followed by its monotone bare-power bound.

Package: [Euler7x700](Euler7x700.json.gz), SHA-256 `7f521c8f37aee7fbd52da609ebccb05c2a78e89873b6e36003a6407cb6b7286b`. Both implementations verified the five bounds above. The [primary verifier](ModeCheck.py) uses a one-coupon recursion and a separate scalar specialization; the [independent verifier](IndependentModes.py) uses sparse per-location costs and a different archived elliptic/Miller–Rabin implementation. They require only Python standard library.

```
python -I -S -B Research/Midday/ModeCheck.py Research/Midday/Euler7x700.json.gz
python -I -S -B Research/Midday/IndependentModes.py Research/Midday/Euler7x700.json.gz
```

Unconditional re-evaluation of the best individual specialized row reached only about 2397 in discovery. Taking the minimum over five separately proved branches, not the minimum of a single graph and not a product of five bounds, is the operative improvement. Register only `(7,700)`; the experiment has not proved an index lift for this new verifier.
