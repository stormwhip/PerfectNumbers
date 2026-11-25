# Conditional support exclusion packet

Copy this directory as `Research/Session20261126/Support` into a complete checkout of `stormwhip/PerfectNumbers` at `2889e47f6db49c8a9bc8dda2c9153829c18a70ca`. No changes to existing files are required. Run:

```sh
python -I -S -B Research/Session20261126/Support/Verify.py
```

One may instead use `--repo PATH` to point to an unmodified checkout; the data beside the script are the same. The verifier uses the public repository and Python standard library only, does not solve an LP, use the network, or write any files. `Ledger.json` lists distinct closed (p,e,H) triples, with H the **exact** subset of the eight roots, not a lower bound on support. `EulerPositions.jsonl` is separate and cannot close a support triple.

**Frozen denominator:** 204 open canonical shards, 244 distinct open (p,e), 6,556 surviving (p,e,H), after the 4,833+9 established SupportSplit exclusions. The 13 price vectors exclude 387 such triples, with two disjoint Euler trees bringing the count to **389**, involving 149 distinct pairs (by root p=7/13/19/31: 165/31/161/32 triples). This leaves **6,167** surviving conditional triples, **244** pairs and **204** open shards. Additional 37 `(p,e,H,Euler=q)` leaves (all outside the newly closed H) have no shard credit. Within H={7,11,13}, all 59 outstanding canonical p=7 exponents are excluded by a single packet; that is not a proof for p=7 with arbitrary H.

**Why a single price vector suffices:** standard `MiddayTerminal/Audit.replay` rebuilds a conservative selection/flow/abundancy relaxation with actual factor-of-sigma divisibility and directed integer coefficients. Its lower bound `u` contains `min(0,min_j rc_j)` for each group. If a real counterexample has a fixed `p^e || N`, and the exact option `i=(p,e,exact)` exists, it must choose that option. Replace that one group term by `rc_i`; all other group terms, unbounded-column checks and the Euler allowance stay intact. With nonnegative row prices the result is a lower bound on actual cost. Only strict `u' > 2400*W*logs(10)[1]` counts. No tail option is promoted to an exact choice. Banned and required primes are enforced for each covered H.

**Why an Euler tree works:** if q is Euler, its exponent is `1 mod 4`, so `(q+1)/2` divides the odd part of its sigma. Multiply that odd divisor together with the actual odd sigma parts of distinct fixed components; strip known supported primes before charging the residual. Count individual known prime powers via the product's incoming valuations and Euler parity, not twice. For the two trees the enumerated branch order returned by `SupportSplit.states` comprises every exact allowed exponent up to 8 and the entire remaining tail. Euler-absent-from-the-listed-support permits every listed unknown base to be charged as ordinary; it does not assume that N has no Euler prime.
