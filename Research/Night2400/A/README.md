# (7,12): 79 certified first-pivot fibers, not a shard closure

Take an odd perfect number `N <= 10^2400`, `v_7(N)=12`, with `19` absent (canonical root order). The integer `sigma(7^12)=16148168401=Q` is prime by the repository’s deterministic 64-bit primality check and divides `N`. All claims are about **exact** `v_Q(N)`, not divisibility. No hypothesis about the rest of the small-prime support is needed.

From the repository root, with no optional dependency, shared factor index or PARI:

```text
python -I -S -B -X int_max_str_digits=0 Research/Night2400/A/Verify.py
```

The packet [Fibers12.json.gz](Fibers12.json.gz) has SHA256 `69347f43301312df23e0d6737837de682d233b30b8f05fcf4538c6b1b7e3464f`. The replay rederives the entire initial split: `7^12 Q^234 <= 10^2400 < 7^12 Q^235`; of exponents 1 through 234, 67 fail parity or the forbidden-divisor test, 84 more give direct contradictions, and 83 remain before this packet. The packet closes 79 of those 83: 60 with one forest each, six with single-pivot complete split trees (`v_Q=28,33,52,78,80,85`), `v_Q=4,8,16,26,38,46,60,70,72,88,106` with nested splits, and `v_Q=100,102` by [factor-free quadratic incoming valuation pricing](Price12.md). The exponent-4 tree uses 1,250 forests, 40 split nodes and 142 abundance leaves. In two difficult sectors, 5 is compulsory and 3 is rigorously absent: the abundancy lower bound for `7^12 3^2 5` already exceeds 2. Their masked forests are checked by [a separate integer recursion](MaskedForest.py). At 28, a compulsory 950-bit prime has only exponents 1 and 2 after direct checks. At exponent 1 it is Euler, and its divisor sum forces 3 and 5; the exact abundancy lower bound from their squares is strictly greater than 2. At exponent 2 the forest bound applies. The 8, 16, and 72 trees use respectively 224, 238, and 651 forests and 3, 10, and 23 split nodes. The valuation-106 tree fixes the successive primes `13697,2800321,67,29,31`, splitting further only along valuations `2,6,2,2` until the final complete split; its 101 forests and 107 direct contradictions exclude every sibling. Both integer forest recursions must strictly exceed `10^2400`; no comparison of rounded floors is used. Every split enumerates all candidates through its monotone size tail and refuses a missing live sibling. The arithmetic imports are from the frozen [TreeCheck/PivotCheck implementation](../../Session20261126/PivotCheck.py) and its dependencies. The recent [7,90 packet](../../FinalSprint/Tree7x90.json.gz) was independently cold-replayed as a transfer control: 454 forests, 16 splits, 469 direct branches.

## Remaining gap

```text
v_Q = 1,2,12,42
```

Only 12 remains in the baseline shard `P7_I00005`, but this is **not** yet a single exact leaf of a closing tree. The four uncovered first-pivot fibers above remain open, so the credit is **0 actual exponents and 0 shards**.

The remaining first-level searches use `110563` at `v_Q=1`, `200741603328100897` at `v_Q=2`, and `173` at `v_Q=42`. A separate [support packet](SupportLeaf12.md) certifies an exact descendant of first value 1 without changing the first-pivot count. The factor-free proof for 100 and 102 was needed because the available index and a bounded ECM pilot did not expose a proved factor there; unlike 96 and 108 it makes no large-component primality assumption.
