# Midday static-forest batch

Baseline: `main` 6732a1a, whose Nov25 ledger has 511 remaining distinct `(p,e)` obligations. This directory contains self-contained exact proofs for individual root exponents, not a universal `10^2400` proof.

From repository root, independent offline replay and intersection with that exact baseline:

```sh
python -I -S -B Research/MiddayForest/Verify.py
python -I -S -B Research/MiddayForest/Control.py
```

For a second implementation, use `Research/NightSevenForest/Release/Replay.py` on root 7/11 files and `Research/NightLowRoute/Release/ForestReplay.py` on root 13/19/31 files. Files have one seed row, including a finite prefix length, roots, and an acyclic assignment of candidate child primes. Large primes have attached ECPP chains. Both verifiers implement exact integer comparisons (possibly after raising to the price denominator); no discovery floor is trusted. The decimal floor 2400 does not alone prove strictness: both comparisons check the full integer `>`, not its decimal length.

## Why the packets prove their claims

For a canonical root `p` at exponent `e`, `A=σ(p^e)` divides `N`. Exclude forbidden canonical roots before admitting local exponents. For an active source `z^f`, remove the unique factor of 2 from its σ if it is Euler, then charge the part of σ coprime to `p A ∏child`. These residuals need not be pairwise coprime: their **product**, after deleting powers of the precharged labels, divides the odd part of σ(N), since the active sources are distinct exact components. For each owned child `q`, only its unique owner demands the local valuation `v_q(σ(z^f))`. A child activates only if its actual divisibility test succeeds. Acyclic ownership prevents double use of a component. Minimize over ordinary exponents or allow the unique Euler coupon once in exactly one subtree. Every finite prefix appends the elementary `z^f` tail (raised to `den−weight[z]` when priced). For a shared price `u/den`, charge `q^{(den−u) f}` from its component and `q^{u v_q(σ)}` across all active emitters; the latter valuations sum to at most `v_q(N)`. An Euler slot need not be in the forest. If `(f+1)` is divisible by `(e+1)`, then both `p^e|p^f` and `σ(p^e)|σ(p^f)` hold, so the seed claims exclude the corresponding higher exponents without assuming equality of σ-values.

## Discovery and failures (not inputs to replay)

Weakest-mode traces from archived proposals supplied exact emitting `(z,f)` cells. `Refine.py` adds candidate child factors and re-evaluates every mode; `Switch.py` reassigns already-owned divisors only when the entire forest improves. Hints came from an archived factor database, limited public FactorDB requests, and local integer factoring. All prime statuses and multiplicities are re-established at replay. These optional discovery scripts require the original scratch layout, `python-flint`/SymPy, and for packing PARI/GP; `Scratch/` is ignored and is not a proof dependency.

The most instructive cases were `(31,316)`, where changing just one owner raised the discovered minimum from 2392.3095 to 2401.2558, and `(13,366)`, where five changes of owner raised 2326.4017 to 2409.7920 before trimming. `(13,10)` also needed separate treatment of the one-Euler mode. Cross-exponent re-rooting tested 34 archived graphs and 103 target transfers without a threshold crossing (highest 1888.18). Exact-prefix exploratory trees for `(13,136)` and `(31,408)` remained open: the former left two branches at the first anchor's exponents 2 and 4; the latter left 12 open leaves after 23 nodes. These search results do not enter the ledger.
