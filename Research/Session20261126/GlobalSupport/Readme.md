# New global hitting set {3,5,17,19}

**Theorem.** If an odd perfect number N is at most 10^2400, at least one of 3,5,17,19 divides it. This is a support theorem, not a proof of the full target. It has no dependency on the 204/244 frontier ledger: the published three hitting sets {3,5,r}, r=7,11,13 imply that a putative counterexample with none of 3,5,17,19 contains all of 7,11,13. The last dual below rules this out.

| Forbidden primes | Required primes | Certified floor(log10 N lower bound) |
|---|---|---:|
|3,5,17,19,23|7,11,13|2729|
|3,5,17,19,31|7,11,13|2607|
|3,5,17,19|7,11,13|2467|
|3,5,19,23|7,11,13,17|2438|
|3,5,19,29|7,11,13,17|2408|

**Corollaries.** When 3,5,19 are all absent the first theorem forces 17. The last two rows force 23 and 29 as well. Hence {3,5,19,23} and {3,5,19,29} are two more global hitting sets. This does not show that 19 alone or 17 alone must occur when 3 and 5 are absent.

The first two cases would force both 23 and 31 in the remaining subcase, but the third packet works even without that inference. The last packet supplements the archival nominations with 27 validated prime/exponent-depth nominations, concentrating on 7,11,13,23,31 and emitted small factors. No asserted factor edge is trusted. Each replay checks all geometric-sum divisibility and primality, generic and surplus column reduced costs, and the strict fixed-scale integer target. All weights are nonnegative dyadic integers. See the existing MiddayTerminal model write-up for the relaxation.

Place this directory under Research/Session20261126; no modifications to upstream code required. Run both (no third-party modules):

```sh
python -I -S -B Research/Session20261126/GlobalSupport/Verify.py
python -I -S -B Research/Session20261126/GlobalSupport/Verify.py --integer-logs
```

Alternatively append `--repo PATH_TO_COMPLETE_CHECKOUT`. The two replays share the frozen LP construction and sparse price vectors but do **not** share log implementations: the second uses integer bounds on 2·atanh((m−1)/(m+1)), 1≤m≤2, at scale 2^176 with 60 positive terms, a proven residual <2^-176, then converts each ratio to outward endpoints at scale 2^80. Its unbounded-column checks must pass anew. No solver, downloaded hints or live endpoint is used in either replay; pre-existing support hitting-set proofs may independently be rerun as in Research/MiddayTerminal/ReleaseThirteen.py --baseline.
