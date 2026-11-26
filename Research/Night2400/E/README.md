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

The packet is [Conditional7x130V128910.json.gz](Conditional7x130V128910.json.gz),
SHA-256 `0c77d6471930aeff690e7d01891b556c244eadf3adf28db0919ca734915330e6`.
To replay offline from the checkout root (Python standard library only):

```powershell
python -B -I Research/Night2400/E/Verify130.py Research/Night2400/E/Conditional7x130V128910.json.gz
```

[Verify130.py](Verify130.py) checks all 150 ECPP chains used by the packet,
derives the complete domain at each split as in [TreeCheck.py](../../Session20261126/TreeCheck.py),
and checks both integer forest evaluations, as in the reference
[7×168 tree](../../FinalSprint/Tree7x168.json.gz) and [7×90 tree](../../FinalSprint/Tree7x90.json.gz).
The price leaf uses the existing [JointValuation argument](../../FinalSprint/JointValuation.md).
`CONDITIONAL_ONLY` means that the returned `open_paths` were not proved empty.
This packet does not close the shard and must not be included in exclusion totals.

Optional discovery used depth zero with head 100 and six rounds, then a
second trial with head 64 and 50 rounds. The fifth complete fiber was sealed
by pricing instead of proving the 3559-bit probable-prime factor from discovery.
[Seal130.py](Seal130.py) optionally packages discovery trees; GP and factor-bank
data are not needed during replay.
