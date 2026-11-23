# Independent root-class and valuation audit for 10^2400

This audit uses the original root order (19, 7, 11, 31, 13, 3, 5, 17)
at repository baseline `8f1db36`. The archived coprime-class certificate
replayed with a lower exponent of 4183.209493. The canonical census
returned 3,072 covered root tasks and accepted all 1,447 previous
integer closures.

| Root | Total | Independently verified | Open |
| ---: | ---: | ---: | ---: |
| 19 | 287 | 130 | 157 |
| 7 | 412 | 192 | 220 |
| 11 | 341 | 154 | 187 |
| 31 | 253 | 117 | 136 |
| 13 | 325 | 146 | 179 |
| 3 | 676 | 311 | 365 |
| 5 | 481 | 281 | 200 |
| 17 | 297 | 297 | 0 |
| **Total** | **3,072** | **1,628** | **1,444** |

The increase is 181 unique top-level tasks. Of these, 125 are from a
whole-class dual for root 17, 54 from a cyclotomic residual dual for
root 5, and two from integer valuation and exponent deductions.
The theorem status is `INCOMPLETE_FRONTIER`. Gemini v5's 1,679 reported
closures remain an external count. This audit establishes its own
accepted set and does not add those reported counts to it.

## Root 17 whole-class dual

Use the original terminal model with the first seven roots excluded.
Admit 17 and require the sum of its exponent-option variables to be
one. The model still includes the parity-dependent Euler budget and
an infinite-prime abundance tail. Archived implication edges remain
valid upon relaxing the exclusions. The verifier checks each new edge
by an exact divisor test and proves the destination prime using a sieve
or recursive Pocklington witnesses.

The integer dual gives log10(N) >= 2847.836220. All 297 tasks for root
17 are covered, including 125 absent from the direct integer baseline.

## Cyclotomic residual and Euler lift

Let p be the root, d=m-1 for a prime m>p, and let the shard imply
m divides v_p(N)+1. Put A=Phi_m(p). Then A divides N and every prime
q dividing A satisfies q=1 mod 2m. Indeed q=m is excluded by
Phi_m(p)=1 mod m, and for the remaining q the order of p modulo q
is m. Let M be the part of N supported outside p and A. The
truncated LP models the true exponents of M. Its explicit base
primes are below 2m+1 for every covered task, and every explicit
destination above that threshold is checked to be coprime to A for
all covered tasks. Implications into p or a possible factor of A are
omitted. Prime factors of M therefore have the original N exponents,
and inherit the Euler budget.

If A has t distinct prime divisors, its prime support contributes at
most the product of (2mi+1)/(2mi) for i=1,...,t. The verifier bounds t
by comparing A to powers of 2m+1. It subtracts an upper bound for this
abundance and for p/(p-1) from the total abundance requirement.
The resulting integer dual bounds log10(M) from below.

Any q=3 mod 4 must have an even exponent in N. For each such q with
odd v_q(A) found by the deterministic sieve through 20,000, the size
bound can include one extra q. If the residual A after removal of
all tested q=3 mod 4 is 3 mod 4, at least one further q=3 mod 4 has odd
valuation. The verifier uses the first integer above 20,000 in the
class 2m+1 mod 4m as a numerical lower bound for this additional
factor. Denote the resulting numerical multiplier by L. Then

    N >= p^d * A * L * M.

L is used only as a numerical size bound. In particular, the lower
endpoint used for an unidentified q is not used as an integer divisor
of N or in any factor-chain implication.

For root 5 and m>=1201 the verified residual exponent is 651.080201.
With the fixed-part bound this yields 54 net new top-level closures.
The separate model with 17 excluded, for m>=901, gives a residual
bound of 853.058981. It also discharges the 17-absent branch of
18 tasks still open at the top level. Their 17-present branches
remain necessary; none of those 18 count as closed.

## Exact proofs for two other shards

For each distinct source prime, retain an odd divisor of its
sigma value, then multiply the retained values across distinct
sources. This product divides N by multiplicativity and oddness.
Use known prime valuations of that product, earlier root exclusions
and the size cap to construct complete exponent domains for forced
primes. If a source has possible exponents e in a domain E, the
geometric sum with length gcd(e+1 : e in E) divides each possible
sigma value. Update that source by an LCM, then update the product.
Size tests combine the mandatory lifts with the at-most-one
Euler-special rule. A bounded search exhausts selected exponent
domains. Hitting its node budget keeps the task open.

- `P7_I00222` (d=1408). The size budget forces the root exponent
  to 1408. The mandatory divisor includes 2819, whose compatible
  exact exponents are 4 and 6. Both exact sigma products exceed
  the size cap. The exponent 2 would force the earlier excluded
  prime 19.
- `P31_I00137` (d=796). The mandatory divisor includes 11159.
  Its only possible exponent is 2, since exponents 4 and 6
  would force 11 and 7. This forces 11839, whose only size-feasible
  positive even exponents, 2 and 4, respectively force the
  excluded primes 7 and 11.

## Replay

Run from the repository root with the Python standard library.

```sh
python -S -O Research/Session20261122/Python/AuditRootClass2400.py --output RootClassAudit.json
```

The optional output includes the exact open top-level manifest and
the partially closed prime-presence branches. The archived
[dual bank](../../Session20261122/Certificates/RootClassDuals2400.json.gz)
has SHA-256
`9b7d0dfce463b4630f015d5d9ddd33a9cd1130820d52c605699821fe465108fd`.
A local replay also rejected a negative dual multiplier, a forged
sigma valuation, missing Pocklington chains and unilateral branch
promotion. Exhausting a one-node valuation budget left the root-7
task open.

The largest remaining root classes are 3 (365), 7 (220), and 5
(200). The next targeted search for root 5 is the 17-present
branch on the 18 listed tasks. The remaining work still requires
complete, replayable search trees or additional whole-class bounds.
