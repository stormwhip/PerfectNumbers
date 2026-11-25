# Conditional low-root branches (not full root exponents)

For a hypothetical odd perfect N≤10^2400 with canonical root 3, no member of {19,7,11,31,13} divides N. If v3(N)=6 then 1093 divides N; if v3(N)=12 then 797161 divides N. The identifier of a branch is the exact valuation of that compelled prime. The geometric sums and primality are recomputed, not assumed.

The reconstruction exhausts all size- and Euler-compatible exponents, removing immediate size/abundance/forbidden contradictions before the following counts. Of 182 surviving possible v1093 exponents at 3^6, the packet rules out 142 and leaves 40. Of 100 possible v797161 exponents at 3^12, it rules out 90 and leaves 10. The verifier reports the full remaining lists. Neither canonical root-exponent class nor shard closes. Do not count the 232 branches in the canonical actual/shard ledger. In particular the already separately closed 3^10 and 3^22 are not in this packet.

Each supplied forest is checked both by Compose.Forest's integer lower bound and PivotCheck.exact_leaf, with every forest node's primality, actual sigma divisibility, Euler exception, depth cap and unbounded exponent tail covered. Splits (where supplied) must contain exactly all noncontradictory children. The subset restriction only occurs at the outermost specified valuation; the rest of the integer tree is complete.

```sh
python -I -S -B Research/Session20261126/LowBranches/Verify.py
```

Or `--repo PATH` when the packet is outside a full checkout. Standard library only; no LP solver, factoring backend, internet or research caches. Packet SHA-256: `4d746a1d6e913953761b0b07ec5df5a42bdbf89aaca2e345467005964c96bfa0`.
