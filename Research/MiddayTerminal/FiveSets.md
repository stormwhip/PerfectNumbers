# Three five-prime hitting sets

**Theorem.** Every odd perfect `N ≤ 10^2400` has a prime factor in each of `{3,5,11,13,17}`, `{3,5,11,13,19}`, `{3,5,11,13,23}`. Equivalently, if 3,5,11,13 are all absent then 17,19,23 are all present; 7 is also present by the prior theorem. No complete root exponent or shard is excluded by this statement alone. It does not say that `{3,5,11,13}` hits every such N.

## Cold replay

From the repository root, Python 3.11+, no optional packages or network:

```
python -I -S -B Research/MiddayTerminal/ReleaseFive.py --baseline
```

Omit `--baseline` only if relying on the published `{3,5,7}` theorem. The command verifies every new packet numerically, binds its specified support hypotheses, and checks the three implications by enumerating every support assignment. Each line prints the packet SHA-256 and independently recomputed floor. A displayed integer floor is not itself the test: every packet must strictly exceed the directed upper enclosure of `2400 log(10)`.

## Six numerical premises and their composition

Put `D={3,5,11,13}` and `Q={17,19,23}`. Each of the following positive-support rows assumes all the indicated primes occur; no exponent is fixed.

| Absent | Required present | Lower bound, floor log10 N |
|---|---|---:|
| D + 17,19 | none | 2524 |
| D + 17,23 | none | 2457 |
| D + 19,23 | none | 2438 |
| D + 17 | 7,19,23 | 2459 |
| D + 19 | 7,17,23 | 2462 |
| D + 23 | 7,17,19 | 2426 |

If D is absent then 7 is present by the previously published `{3,5,7}` theorem. The first three rows prohibit any two members of Q being absent. If exactly one is absent, the other two are present, so the corresponding last-three row gives the contradiction. Thus all are present.

## Numerical proof

All allowed odd primes below L=10001 are explicit. Recover legal exponent options from scratch under the stated exclusions: all admissible positive even exponents and, only for primes 1 mod 4, exponents 1 mod 4 with at most one selected globally. Divisibility of the geometric sum by any absent prime makes that exact exponent impossible. If `p+1` is so divisible, the entire Euler progression is impossible. Every retained finite prefix has its own admissible upper tail, priced at the first tail exponent; the tail emits no sigma divisor. The optional large-prime labels are not assumed to divide N; prime status is checked by deterministic 64-bit tests or recursive Pocklington. The old archival cutoffs simply choose some optional labels/prefix sizes and cannot remove a prime below L. Every actual outgoing valuation is recomputed by integer division. No old multiplier or lower bound is used.

For a selected exact component p^f, split the odd part of its divisor sum into explicit prime powers and a residual u. The product of these odd divisor sums divides N, even when the different u share prime factors. Charge log u per source, and credit all residual-prime abundancies (duplicate credits allowed). Outside explicit primes and all emitted residuals, an ordinary prime costs at least 2 log(L) and contributes at most log(L/(L-1)); a separate globally limited Euler option pays log(L). Sieve residuals up to T, credit each actual trial divisor at most log(q/(q-1)), and the unclassified part at most floor(log_T remaining) further primes. Model every explicit component by its selected local cost plus possible surplus exponent. The surplus covers incoming valuations above the minimum paid by the selected option; exact fixed components cannot use surplus. An active exact source forces a compatible target choice; the sum of incoming valuations cannot exceed actual holdings. The selected groups respect the two-sided abundancy inequalities: upper credits must reach log(2), and the lower credit from selected explicit components alone is at most log(2). These rules give a feasible point for any putative N in the respective class; its charged cost is at most log(N).

Apply the submitted nonnegative dyadic row prices (denominator 2^24) to the independently reconstructed inequalities. Use directed interval logs at scale 2^80, require all unbounded reduced columns nonnegative, minimize each remaining explicit group's reduced cost over all choices including absence, and bound any other binary column by its nonpositive part. This yields a rigorous integer lower bound; in particular neither success nor infeasibility from a floating solver is a certificate.

## Whitelist

Only the following new filenames under `Research/MiddayTerminal/` are needed for this release:

```
FiveSets.md
ReleaseFive.py
Audit.py
Common.py
Cut0x0x3x5x11x13x17x19.json.gz
Cut0x0x3x5x11x13x17x23.json.gz
Cut0x0x3x5x11x13x19x23.json.gz
NewDrop17.json.gz
NewDrop19.json.gz
NewDrop23.json.gz
```

Pre-existing repository dependencies: `Research/RootFiveNext/PrimeCheck.py`, `Research/NightUniform/ThreeAvoid.json`, and the two `Research/Session20261122/Certificates/Terminal{Original,Replacement}.json.gz` archives. Full prior replay also uses the already published `Research/NightUniform/ThreeHittingWitness.py` and its repository dependencies. No root-three or root-thirteen private seed pack, MiddayFive directory, discovery script, solver, or factoring service is needed.
