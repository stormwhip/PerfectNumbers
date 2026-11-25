# Near-threshold forests for roots 7 and 11

The target is to exclude exact components `p^e || N` in a hypothetical odd perfect number `N <= 10^2400`, subject to the fixed root order `(19,7,11,31,13,3,5,17)`. These are exact-exponent obligations, not standalone shard closures. The four representative seeds each occur in two baseline shards with other outstanding exponents.

## Discovery and proof boundary

The input `seed*.json` files under the historical `NightSevenForest` directory were used **read-only**; no historical discovery script was executed. [Scout.py](Scout.py) traces the minimizing finite local exponent states, separating ordinary even exponents from the single possible Euler exponent `1 mod 4`. [Search.py](Search.py) expands only the active witness configurations, not all finite local exponents: it splits `f+1` into cyclotomic divisors; tries a read-only factor bank, bounded small factorization, and probable primality for large factors; then adds/reassigns a prime's unique owner only along an acyclic graph. The discovery score uses logs and has no proof status. A larger head checks more individual exponents, while the tail is still retained with a monotone component-size bound. [Optimize.py](Optimize.py) is an optional price-coordinate pilot, not needed by any unpriced ordinary packet.

For proof, [Pack.py](Pack.py) collects exact prime certificates from cache or new ECPP, checks them with the fixed integer primality checker, and calls the pinned [Replay.py](../../NightSevenForest/Release/Replay.py). Pack production is not required by a proof recipient. For each row, the pinned verifier holds the exact root sigma, checks that every explicit base is prime and every root label divides the root sigma, and validates the ownership graph. It evaluates an edge only when the exact local sigma contributes a positive valuation to that child. A child gets its component exponent from its one owner; cross-source multiplicities of unlabelled primes are charged to their actual total valuation from checked sigmas. No factor decomposition assumption is made for the residual integers. A prime equal to the global Euler component may obtain its coupon in at most one subtree; root modes and the case where it is not itself a root label are minimized. Only a strict integer comparison larger than `10^2400` establishes a result.

## Initial pilot, floating discovery only

| `(p,e)` | Historical graph | Initial nominal score | First expanded score |
|---|---:|---:|---:|
| `(11,220)` | 7 roots, 822 owners | 2337.529590 | 2419.704266 |
| `(7,234)` | 3 roots, 925 owners | 2322.942406 | 2400.001788 |
| `(11,132)` | 7 roots, 1,160 owners | 2308.584039 | 2436.797048 |
| `(7,252)` | 6 roots, 1,832 owners | 2302.183363 | 2400.226384 |

A second sample prioritized near-threshold `(11,66)` (singleton `P11_I00017`), then `(11,214)` and `(7,412)`, then the lower-scoring singleton `(11,46)` (`P11_I00013`). Expanded scores for the first three were 2414.434314 (from 2297.006725), 2428.836129 (from 2211.678840), and 2408.672529 (from 2184.288745), respectively. A discovery crossing does not count if its exact packet is absent or fails replay.

The 11/220 minimizing historical mode has its coupon at 3,158,528,101; the 7/234 minimizer uses 1933 at exponent 1 below a root label. The nominal gaps are not simply overlooked parity at active labels: when adding all visible outflows in the minimizing historical states, no active labelled component's required exponent increases in either case. The pilot instead exploited overlooked/discoverable cyclotomic children. For reference, the 11/132 minimizer contains two truncated tail states (43, 31); a change to the head must retain a legal tail minimum rather than treating that cutoff as a contradiction.

## Literature check

- [Nielsen, *Odd perfect numbers have at least nine distinct prime factors*, §3](https://arxiv.org/html/math/0602485v1#S3): cyclotomic sigma decomposition and the two cases in prime-adic valuations. These inform candidate discovery, not trust in factor-bank output.
- [Ochem–Rao, *Odd perfect numbers are greater than 10^1500*](https://doi.org/10.1090/S0025-5718-2012-02563-4): conventional precise component branching and abundance/size contradictions. A lower-bound divisor `r^c | N` does not authorize using `sigma(r^c)` without branching to exact equality of the exponent.
- [Fathi, *Seed-free receiver cores, complete-row reductions, and sigma-graph cut identities*, v17](https://zenodo.org/records/21795420): a recent working paper gives a general full-graph cut identity and strong connectivity; its tighter conditional casework assumes a restricted support of higher components and cannot be transferred to these roots. For a set `U` of exact components, `Outgoing(U)/Incoming(U) = product(sigma(q^f)/q^f)/2^[Euler in U]` follows directly by cancelling the internal incoming valuations in `sigma(N)=2N`. This does not justify treating a trial ownership forest as the full sigma graph, or counting an unknown returning edge as a new prime. The proof packets do not use those claims.

## Portable replay

Use Python with the standard library only. Run each final packet both directly through the pinned integer verifier and through the [baseline adapter](Verify.py), which verifies the pinned audit and emits the affected exponent pairs for the main ledger. Discovery logs, factor banks, and ECPP-generation software are not used by final replay.

| Verified seed | Portable packet | Euler modes | Exact lower-bound floor `floor(log10 L)` | ECPP chains | Affected baseline shards (remain open from this seed alone) |
|---|---|---:|---:|---:|---|
| `(11,220)` | [11x220](best-11x220-1.pack.json.gz) | 6 | 2419 | 121 | `P11_I00004`, `P11_I00005` |
| `(7,234)` | [7x234](best-7x234-1.pack.json.gz) | 2 | 2400 | 132 | `P7_I00002`, `P7_I00014` |
| `(11,132)` | [11x132](best-11x132-1.pack.json.gz) | 4 | 2436 | 123 | `P11_I00002`, `P11_I00006` |
| `(7,252)` | [7x252](best-7x252-1.pack.json.gz) | 2 | 2400 | 288 | `P7_I00004`, `P7_I00008` |
| `(11,66)` | [11x66](best-11x66-1.pack.json.gz) | 3 | 2414 | 106 | **Closes `P11_I00017`** |
| `(11,214)` | [11x214](best-11x214-1.pack.json.gz) | 4 | 2428 | 71 | `P11_I00001`, `P11_I00012` |
| `(7,412)` | [7x412](best-7x412-1.pack.json.gz) | 8 | 2408 | 101 | `P7_I00003`, `P7_I00016` |
| `(7,162)` | [7x162](best-7x162-1.pack.json.gz) | 5 | 2451 | 47 | **Closes `P7_I00037`** |

Rows with floor 2400 still have `L > 10^2400` by strict integer comparison.

```powershell
$packets = Get-ChildItem Research/Nov25/seven -File -Filter '*.pack.json.gz' | ForEach-Object FullName
python -I -S -B Research/NightSevenForest/Release/Replay.py @packets
python -I -S -B Research/Nov25/seven/Verify.py @packets
```

For one packet, pass its path rather than `@packets` to either command. The pinned verifier prints seed, mode count, and floor; the adapter prints the exact baseline exponent obligations.
