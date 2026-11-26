# Support theorems (not full shard closures)

For an odd perfect number N ≤ 10^2400, its support must meet each row below. The certified floor is that of a lower bound for log10 N **assuming all listed primes absent**, hence each row is impossible. No frontier assumption is made.

| Forbidden set | Certified floor |
|---|---:|
|3,5,19,31,37|2453|
|3,5,19,31,47|2432|
|3,5,17,23,29|2574|
|3,5,17,23,31|2492|
|3,5,17,29,31|2423|

In particular if 3,5,17 are absent at least two of 23,29,31 occur. If 3,5,19,31 are absent both 37 and 47 occur. Proof: the [six inherited hitting sets](../../Session20261126/GlobalSupport/Readme.md) force the required support in each row. The [verifier](GlobalVerify.py) independently checks this implication by support enumeration. It replays the certified nonnegative dual against the [whole-domain relaxation](../../MiddayTerminal/Audit.py): allowed explicit exponents, both unbounded exponent tails, residual flow and the anonymous prime columns are included. All costs/abundancies are rounded in the conservative direction. For 47 use the looser domain without the 47 restriction, set the explicit group constraint prices to zero, refund each old minimum, impose the mandatory/forbidden groups and remove exact exponents emitting 47. Remove odd tail options only if 47 divides q+1. Sum even-or-absent minima and allow the greatest saving at **one** explicit odd exponent. A possible anonymous Euler prime was already allowed, and taking an additional explicit discount in that case only weakens the result. Recomputed lower bounds strictly exceed the upper threshold before division/flooring.

A separate [pivot packet](Pivot316.json.gz) excludes 36 of the 57 old support masks at (19,316). Its [checker](Pivot316Verify.py) proves the pivot prime divides the root sum, then enumerates every compatible valuation for each claimed mask. Ten surviving branches use integer forests. A floor of 2400 alone is never accepted; strict comparison is required. This result does not exclude the actual exponent 316.

Separately, the [root-seven packet](7x28.json.gz) rules out 13 previously open support masks at (7,28). The verifier reconstructs the required S8 primes and prohibited divisors, uses one Euler discount and computes complete exponent tails. These and the 36 previous masks total 49 disjoint conditional exclusions, **not 49 shards**.

From the repository root:
```
python -I -S -B Research/FinalSprint/Support/GlobalVerify.py --repo .
python -I -S -B Research/FinalSprint/Support/Pivot316Verify.py --repo .
python -I -S -B Research/FinalSprint/Support/ForestVerify.py --repo . Research/FinalSprint/Support/7x28.json.gz
```
