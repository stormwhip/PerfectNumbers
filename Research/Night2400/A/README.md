# (7,12): 68 certified first-pivot fibers, not a shard closure

Take an odd perfect number `N <= 10^2400`, `v_7(N)=12`, with `19` absent (canonical root order). The integer `sigma(7^12)=16148168401=Q` is prime by the repository’s deterministic 64-bit primality check and divides `N`. All claims are about **exact** `v_Q(N)`, not divisibility. No hypothesis about the rest of the small-prime support is needed.

From the repository root, with no optional dependency, shared factor index or PARI:

```text
python -I -S -B -X int_max_str_digits=0 Research/Night2400/A/Verify.py
```

The packet [Fibers12.json.gz](Fibers12.json.gz) has SHA256 `bc75d954a42fefa5ac9da8f6e6ecc9ac5dc454d7820a35c8f94d507f3130c0dd`. The replay rederives the entire initial split: `7^12 Q^234 <= 10^2400 < 7^12 Q^235`; of exponents 1 through 234, 67 fail parity or the forbidden-divisor test, 84 more give direct contradictions, and 83 remain before this packet. The packet closes 68 of those 83: 60 with one forest each, five with single-pivot complete split trees (`v_Q=33,52,78,80,85`), `v_Q=38,70` with nested splits, and `v_Q=106` with a five-level tree. The latter fixes the successive primes `13697,2800321,67,29,31`, splitting further only along valuations `2,6,2,2` until the final complete split; its 101 forests and 107 direct contradictions exclude every sibling. Both integer forest recursions must strictly exceed `10^2400`; no comparison of rounded floors is used. Every split enumerates all candidates through its monotone size tail and refuses a missing live sibling. The arithmetic imports are from the frozen [TreeCheck/PivotCheck implementation](../../Session20261126/PivotCheck.py) and its dependencies. The recent [7,90 packet](../../FinalSprint/Tree7x90.json.gz) was independently cold-replayed as a transfer control: 454 forests, 16 splits, 469 direct branches.

## Remaining gap

```text
v_Q = 1,2,4,8,12,16,26,28,42,46,60,72,88,100,102
```

Only 12 remains in the baseline shard `P7_I00005`, but this is **not** yet a single exact leaf of a closing tree. The 15 uncovered first-pivot fibers above remain open, so the credit is **0 actual exponents and 0 shards**.

Uncertified discovery (not counted): `v_Q=100,102` had no proved primality factors from the available data index and the smooth-factor pilot; the one-target price transfer stalled in large Hensel lifts. The shallow forests for `v_Q=1,2,4` reached floors 1138,1201,1300 in the stronger run; the first assigned pivots for `v_Q=2,4` have low-exponent siblings still far below threshold. The favorable large-component certificates at `v_Q=96,108` are now included; extrapolating those to `v_Q=100,102` would assume unproved factor information.
