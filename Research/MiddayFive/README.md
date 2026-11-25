# Canonical root five: unconditional terminal closure

All 14 actual exponents still open in the November 25 ledger now have unconditional certificates for `5^e || N`, under precisely the canonical prohibitions `3,7,11,13,19,31 ∤ N` and `N ≤ 10^2400`. Here the prohibition means that **none** of those six primes divides `N`. No auxiliary forest support or Euler location is assumed. This closes 13 more shards, not 14: `P5_I00003` contains both 6 and 48. The other IDs are `P5_I00004` through `P5_I00010`, `P5_I00012` through `P5_I00015`, and `P5_I00019`. Together with the frozen baseline this closes all 481 canonical root-five shards. It does not establish the full odd-perfect-number bound.

|e|lower floor log10 N|e|lower floor log10 N|
|---:|---:|---:|---:|
|6|2431|30|2658|
|10|2661|40|2767|
|12|2602|42|2473|
|16|2520|46|2514|
|18|2406|48|2442|
|22|2517|52|2975|
|28|2780|70|2933|

## Release replay

From the repository root; requires Python 3.10+ standard library. Both commands read the same [frozen 14 sparse duals](Accepted.json.gz) (SHA-256 `71e90ed991d3594154098c592aa0c73541cab6219b2070494c78c069c9e4df2b`). Add space-separated exact exponents for a subset.

```sh
python -I -S -B Research/MiddayFive/Replay.py
python -I -S -B Research/MiddayFive/Replay.py --audit
```

The [primary reconstruction](Joint.py) uses positive-series fixed-point interval logs from the pre-existing library. The [independent reconstruction](Audit.py) uses Decimal's correctly rounded logarithm and neighboring representables, a separate prime sieve, divisibility test, grouped factor extraction, row assembly and dual accumulation. The shared trusted arithmetic includes [64-bit Miller–Rabin and complete ECPP verification](../RootFiveNext/PrimeCheck.py), not historical claimed LB values. Both check Pocklington records for nominated larger labels independently. The [entry point](Replay.py) binds the list of covered `(5,e)` to the 14 differences actually open in [the Nov25 ledger](../Nov25/Delta.json). A solver, GPU, PARI or private factor database is **not** needed at replay. Every exponent is proven by one unconditional dual, even though some discovery work used conditional exact branches.

## Why simultaneous output charges are valid

Write `N=∏r^a`, and let `U` be all explicit base primes. This includes 5 and every allowed odd prime `<L`, for `L=5001,7001,12001` according to the selected instance. Positive exact exponent options and monotone higher-exponent tails exhaust all ordinary even and Euler `1 mod 4` exponents; a forbidden divisor in `σ(r^a)` discards an exact option. For an ordinary tail use the next admissible even exponent; handle the eligible Euler tail separately. Euler parity, `q ≡ 1 mod 4`, and the exponents excluded by forbidden divisors of `q+1` are mandatory. Fixing an exponent requires its option be selected, not merely an exponent lower bound. `Seeds`'s historical ownership map is used **only to nominate primes** and exponent cutoffs, not as evidence that any extra prime is present. Similarly the [archival terminal inputs](TerminalBank.py) nominate 4,572 labels; every output is recomputed by division at the actual exact option.

For each *selected exact* option `i`, write the odd part of its divisor sum as `Y_i=U_i ∏_{q∈U} q^{v_iq}`, where `U_i` has no explicit prime factor. Its prime factors are ≥L: excluded primes cannot occur in a legitimate divisor sum, 2 has been removed, and all remaining smaller primes are explicit. Since `σ(N)=2N`, one has **`∏Y_i | N`**, including multiplicities at shared prime factors. Thus we charge every `log U_i` rather than an lcm or an independently rounded square completion. No `U_i` is asserted prime, squarefree, coprime to another, or supported on a previously unknown set of exactly `floor(log_L U_i)` primes.

For each explicit `q`, the *sum* of incoming valuations cannot exceed its actual exponent. The base option quotes its exact exponent or lower tail exponent `h`. For an actual tail exponent `a`, assign the free surplus column `a-h` with price `log q`; if unnecessary this can always be relaxed downward. Unmodeled extra powers at an explicit target can only make this lower bound more conservative. If a grouped source option can emit ≥k units, the target must select an exponent with capacity ≥k, or a tail. Mandatory exact-source inflows can be added to that threshold **only for a different source**. These grouped implications and additive flow rows are independent valid inequalities, not multiple charges. Explicit sizes and `∏U_i` are disjoint classes of prime powers.

For each exact explicit option use exact log-abundance `log(σ(q^h)/q^h)`; use `log(q/(q−1))` for a tail. Give each `U_i`'s prime support an extra upper abundance of `floor(log_L U_i)·log(L/(L−1))`. Duplicate free abundance for overlapping supports only weakens the bound. Ordinary primes not explicit and not in any emitted `U_i` cost ≥`2 log L` per prime, and contribute at most `log(L/(L−1))` each. The unbounded continuous tail costs at least their ratio per log-abundance; it contains **only primes outside paid output supports**. A remaining outside Euler prime not counted in any cofactor gets the corresponding separate bounded column, costing `log L` for abundance at most `log(L/(L−1))`; if Euler already belongs to a residual its abundance is already covered, so this column may be zero. The sum of explicit odd option indicators and this Euler indicator is at most one. Costs are rounded down; abundance allowances are rounded up; the required abundance is rounded down.

For `Ax≤b`, nonnegative sparse weights `w/W` (`W=2^24`) yield the bound `−w·b+min_x (WC+wA)·x`, in integer log units. All free reduced costs must be ≥0. For each base, at most one option is active, so the minimum is bounded below by `min(0,min_j reduced_j)` in that group. The left side is compared strictly to the upper endpoint of `2400·W·log(10)`. SciPy only suggests the sparse nonnegative weights.

## Discovery notes

The first low-resolution scan was not close to full closure (root 70 scored only 1448). Explicit exact branches, ECPP and limited ECM provided genuine conditional improvements, including an independently replayable [507-digit forced prime](Arithmetic.py) on the `e=48, v_anchor=18` cell, whose pure-power floor is 3600. Enlarging the certified target list and accounting for several simultaneous sources at each valuation gave the full results; the sparse release includes no branch-tree or ECM dependency. An alternate larger `(5,6)` instance reaches 2500 but is not added to the count; the frozen release uses the cheaper 2431 proof. Historical runs and low-resolution research artifacts are not additional proof packets. A separate run of `Free.py 12001 96 125` (64,734 options, 58,802 rows) allowed every root-five exponent at once and only reached 1797; this stronger single-LP shortcut is not certified. The canonical class closure uses the pre-existing partition and the individual exact-exponent proofs.
