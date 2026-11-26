# (7,12): 58 certified first-pivot fibers, not a shard closure

Take an odd perfect number `N <= 10^2400`, `v_7(N)=12`, with `19` absent (canonical root order). The integer `sigma(7^12)=16148168401=Q` is prime by the repository’s deterministic 64-bit primality check and divides `N`. All claims are about **exact** `v_Q(N)`, not divisibility. No hypothesis about the rest of the small-prime support is needed.

From the repository root, with no optional dependency, shared factor index or PARI:

```text
python -I -S -B -X int_max_str_digits=0 Research/Night2400/A/Verify.py
```

The packet [Fibers12.json.gz](Fibers12.json.gz) has SHA256 `f06b07784bdf0158eb466d880ddf51ec7553bcacfdb7a383f0d5da14d35aad78`. The replay rederives the entire initial split: `7^12 Q^234 <= 10^2400 < 7^12 Q^235`; of exponents 1 through 234, 67 fail parity or the forbidden-divisor test, 84 more give direct contradictions, and 83 remain before this packet. The packet closes 58 of those 83: 52 with one forest each, four with single-pivot complete split trees (`v_Q=33,78,80,85`), `v_Q=38` with two nested splits, and `v_Q=106` with a five-level tree. The latter fixes the successive primes `13697,2800321,67,29,31`, splitting further only along valuations `2,6,2,2` until the final complete split; its 101 forests and 107 direct contradictions exclude every sibling. Both integer forest recursions must strictly exceed `10^2400`; no comparison of rounded floors is used. Every split enumerates all candidates through its monotone size tail and refuses a missing live sibling. The arithmetic imports are from the frozen [TreeCheck/PivotCheck implementation](../../Session20261126/PivotCheck.py) and its dependencies. The recent [7,90 packet](../../FinalSprint/Tree7x90.json.gz) was independently cold-replayed as a transfer control: 454 forests, 16 splits, 469 direct branches.

## Remaining gap

```text
v_Q = 1,2,4,6,8,9,12,16,24,25,26,28,30,36,42,46,52,60,70,72,82,88,
      100,102,108
```

Only 12 remains in the baseline shard `P7_I00005`, but this is **not** yet a single exact leaf of a closing tree. The 25 uncovered first-pivot fibers above remain open, so the credit is **0 actual exponents and 0 shards**.

Uncertified discovery (not counted): at `v_Q=36`, only valuation 4 of `367730753610118471143355854964667` remained below threshold in the sampled split (floor 2159); for `v_Q=52`, the analogous gap is valuation 4 of `55834426643085762053546201` (floor 2322). `v_Q=108` has a discovery forest above threshold but a 3554-bit root certificate exceeded the 95-second attempt. `v_Q=100,102` had no proved primality factors from the available data index and the smooth-factor pilot; the one-target price transfer stalled in large Hensel lifts. The shallow forests for `v_Q=1,2,4` reached floors 571,736,1076 in the stronger run; the first assigned pivots for `v_Q=2,4` have low-exponent siblings still far below threshold.
