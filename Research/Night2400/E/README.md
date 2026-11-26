# P7_I00031 / (7,130): conditional exact-pivot exclusion

Base commit: `49b19bbdf6c46ac3cdd4cb0da2b6b08e1360fdec`. Scope: odd perfect
numbers `N ≤ 10^2400` in canonical root 7 and `7^130 || N`. No lift from
an exact exponent to a divisibility case is claimed.

The forced prime
`q = 85053461164796801949539541639542805770666392330682673302530819774105141531698707146930307290253537320447270457`
is 366 bits and has valuation one in `σ(7^130)`. The verifier proves
its primality and derives every assignment. With `M=(7^130·σ(7^130))/q`,
`M q^f | N` for `f=v_q(N)`; the monotone tail `f ≥ 21` is rejected
since `M q^21 > 10^2400` (exact floor log10 2418). Before the tail,
`f=3,5,7,11,15,17,19` fail parity/forbidden-emission checks, and
`f=12,13,14,16,18,20` fail the direct exact-state bound. The seven
remaining fibers are `1,2,4,6,8,9,10`.

| `f` | Current claim |
|---:|:---|
| 1 | Closed by exact forest, floor 2407 |
| 2 | Closed by exact forest, floor 2419 |
| 4 | Open in this packet |
| 6 | Open in this packet |
| 8 | Closed by exact forest, floor 2608 |
| 9 | Closed by exact forest, floor 2514 |
| 10 | Closed by simultaneous incoming-valuation pricing with target `[q]`, zero blanket exceptions, Euler windows `[8,0,2]` |

The packet is [Conditional7x130Fibers128910.json.gz](Conditional7x130Fibers128910.json.gz),
SHA-256 `0c77d6471930aeff690e7d01891b556c244eadf3adf28db0919ca734915330e6`.
To replay offline from the checkout root (Python standard library only):

```powershell
python -B -I Research/Night2400/E/Verify130.py Research/Night2400/E/Conditional7x130Fibers128910.json.gz
```

[Verify130.py](Verify130.py) checks all 150 ECPP chains used by the packet,
derives the complete domain at each split as in [TreeCheck.py](../../Session20261126/TreeCheck.py),
and checks both integer forest evaluations, as in the reference
[7×168 tree](../../FinalSprint/Tree7x168.json.gz) and [7×90 tree](../../FinalSprint/Tree7x90.json.gz).
The price leaf uses the existing [JointValuation argument](../../FinalSprint/JointValuation.md).
`CONDITIONAL_ONLY` means that the returned `open_paths` were not proved empty.
This packet does not close the shard and must not be included in exclusion totals.

## Refined conditional cover

[Conditional7x130Refined.json.gz](Conditional7x130Refined.json.gz), SHA-256
`c3215e5a7456cee4ba8c266b0103c1316cbc18aa369813429f112e396161b8f6`, keeps the
same five fully closed first fibers and refines both open first fibers. It
replays 17 splits, 122 exclusion leaves, 44 open paths and 626 ECPP chains.
Of the exclusion leaves below partial fibers, 48 are below `f=4` and 69 below
`f=6`; each partial fiber also has 22 open paths. The receipt's `closed_fibers`
contains only completely exhausted first fibers. `partial_fibers` maps every
other first fiber to its **open paths** and separately to its **excluded leaves**.
Neither an open path nor any ancestor of an open path counts as an exclusion.
The `splits` member gives all children, direct rejections, infeasible exponents,
and the first exponent of the proven monotone tail at every internal node.

```powershell
python -B -I -S Research/Night2400/E/Verify130.py Research/Night2400/E/Conditional7x130Refined.json.gz
python -B -I -S Research/Night2400/E/Test130.py
```

## Discovery notes

Optional discovery used depth zero with head 100 and six rounds, then a
second trial with head 64 and 50 rounds. The fifth complete fiber was sealed
by pricing instead of proving the 3559-bit probable-prime factor from discovery.
[Seal130.py](Seal130.py) optionally packages discovery trees; GP and factor-bank
data are not needed during replay. The refined packet used [Merge130.py](Merge130.py)
to preserve proved leaves when combining trials, plus price-only leaves under
`f=4` at second exponents 20/21/22/24/25 and under `f=6` at 16/18.

Subsequent discovery experiments (not proof dependencies) used [Scout130.py](Scout130.py)
for per-subtree bounded growth and [Price130.py](Price130.py) to try target sets.
[Factor130.py](Factor130.py) ran GMP-ECM with `-maxmem 64 -q -one`; initial
parameters `B1=70000`, at most 800 curves and 150 seconds per residual;
then `B1=1000000`, at most 1200 curves and 900 seconds per residual on the
1341-bit and 2049-bit main remainders and two selected descendants. The
smaller descendant residuals used `B1=100000`, at most 500 curves and
60 seconds each. No exclusion relies on a factor search failing.
