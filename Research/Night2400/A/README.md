# (7,12): 48 certified first-pivot fibers, not a shard closure

Take an odd perfect number `N <= 10^2400`, `v_7(N)=12`, with `19` absent (canonical root order). The integer `sigma(7^12)=16148168401=Q` is prime by the repository’s deterministic 64-bit primality check and divides `N`. All claims are about **exact** `v_Q(N)`, not divisibility. No hypothesis about the rest of the small-prime support is needed.

From the repository root, with no optional dependency, shared factor index or PARI:

```text
python -I -S -B -X int_max_str_digits=0 Research/Night2400/A/Verify.py
```

The packet [Fibers12.json.gz](Fibers12.json.gz) has SHA256 `7b9c694d67ff2d51972a308faae4875540bcda9b8770f1322fadac318d537a72`. The replay rederives the entire initial split: `7^12 Q^234 <= 10^2400 < 7^12 Q^235`; of exponents 1 through 234, 67 fail parity or the forbidden-divisor test, 84 more give direct contradictions, and 83 remain before this packet. The packet closes 48 of those 83: 46 with one forest each, and 2 (`v_Q=80` and `85`) by complete second splits on `200741603328100897` and `110563`, respectively. Both integer forest recursions must strictly exceed `10^2400`; no comparison of rounded floors is used. Every second split enumerates all candidates through its monotone size tail and refuses a missing live sibling. The arithmetic imports are from the frozen [TreeCheck/PivotCheck implementation](../../Session20261126/PivotCheck.py) and its dependencies. The recent [7,90 packet](../../FinalSprint/Tree7x90.json.gz) was independently cold-replayed as a transfer control: 454 forests, 16 splits, 469 direct branches.

## Remaining gap

```text
v_Q = 1,2,4,5,6,8,9,10,12,13,14,16,17,24,25,26,28,30,33,36,38,42,46,
      52,60,70,72,78,82,88,96,100,102,106,108
```

Only 12 remains in the baseline shard `P7_I00005`, but this is **not** yet a single exact leaf of a closing tree. The 35 uncovered first-pivot fibers above remain open, so the credit is **0 actual exponents and 0 shards**.

Uncertified discovery (not counted): at `v_Q=33` a split on the 482-bit component `8260970923369115853457183041657234616918437806224160936671841022031485875549572430710328691620714145492242475544100054549410854404134881834297419` had only valuation 2 below threshold (best floor 2339); at `v_Q=38` the analogous 404-bit component had only valuation 2 below threshold (best floor 2063). At `v_Q=78`, `r=4272939075950359114787719`, the two below-threshold siblings were `v_r=4,6` (floors 2380,2393); at `v_Q=106`, `r=13697`, they were `v_r=1,2,4` (floors 2351,2268,2314). `v_Q=96,108` have discovery forests above threshold but fresh 3189/3554-bit root certificates exceeded 25-second attempts and are not in this packet. The one-target pricing transfer stalled in large Hensel lifts; a more direct low-cost follow-up is to strengthen the above near-threshold second-pivot siblings first. The shallow forests for `v_Q=1,2,4` reached at most floors 282,547,884 in the sampled runs; neither more of the same shallow forest nor the recent large-pivot examples justify claiming these fibers closed.
