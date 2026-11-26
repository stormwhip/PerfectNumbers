# (7,12): 51 certified first-pivot fibers, not a shard closure

Take an odd perfect number `N <= 10^2400`, `v_7(N)=12`, with `19` absent (canonical root order). The integer `sigma(7^12)=16148168401=Q` is prime by the repository’s deterministic 64-bit primality check and divides `N`. All claims are about **exact** `v_Q(N)`, not divisibility. No hypothesis about the rest of the small-prime support is needed.

From the repository root, with no optional dependency, shared factor index or PARI:

```text
python -I -S -B -X int_max_str_digits=0 Research/Night2400/A/Verify.py
```

The packet [Fibers12.json.gz](Fibers12.json.gz) has SHA256 `872c59c2b29a7da800338e20f6ecfd6082498135fa3c50b6be7e23339c31ac5a`. The replay rederives the entire initial split: `7^12 Q^234 <= 10^2400 < 7^12 Q^235`; of exponents 1 through 234, 67 fail parity or the forbidden-divisor test, 84 more give direct contradictions, and 83 remain before this packet. The packet closes 51 of those 83: 46 with one forest each, four with single-pivot complete split trees (`v_Q=33,78,80,85`), and `v_Q=106` with a five-level tree. The latter fixes the successive primes `13697,2800321,67,29,31`, splitting further only along valuations `2,6,2,2` until the final complete split; its 101 forests and 107 direct contradictions exclude every sibling. Both integer forest recursions must strictly exceed `10^2400`; no comparison of rounded floors is used. Every split enumerates all candidates through its monotone size tail and refuses a missing live sibling. The arithmetic imports are from the frozen [TreeCheck/PivotCheck implementation](../../Session20261126/PivotCheck.py) and its dependencies. The recent [7,90 packet](../../FinalSprint/Tree7x90.json.gz) was independently cold-replayed as a transfer control: 454 forests, 16 splits, 469 direct branches.

## Remaining gap

```text
v_Q = 1,2,4,5,6,8,9,10,12,13,14,16,17,24,25,26,28,30,36,38,42,46,
      52,60,70,72,82,88,96,100,102,108
```

Only 12 remains in the baseline shard `P7_I00005`, but this is **not** yet a single exact leaf of a closing tree. The 32 uncovered first-pivot fibers above remain open, so the credit is **0 actual exponents and 0 shards**.

Uncertified discovery (not counted): at `v_Q=38`, a split on the 404-bit component `24184431630358017189722420442790936263972733350624509678066930704096840309459344712976298206511417239870211176890697330401` had only valuation 2 below threshold in the sampled trees (best floor 2063). `v_Q=96,108` have discovery forests above threshold but fresh 3189/3554-bit root certificates exceeded 25-second attempts and are not in this packet. The one-target pricing transfer stalled in large Hensel lifts. The shallow forests for `v_Q=1,2,4` reached at most floors 282,547,884 in the sampled runs; neither more of the same shallow forest nor the recent large-pivot examples justify claiming these fibers closed.
