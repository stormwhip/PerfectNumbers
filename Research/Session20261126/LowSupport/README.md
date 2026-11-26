# Three universal Euler-location restrictions for 3|(e+1), root 19

**Theorem (no bound on N).** Suppose N is an odd perfect number, 19^e||N with e positive even, e≡2 (mod 3), and H is the exact set of primes from {19,7,11,31,13,3,5,17} dividing N. Then:

|Exact H|Necessary Euler component|Necessary 3 component|
|---|---|---|
|{3,7,13,19,31}|13^1||N|3²||N|
|{3,5,19,31}|5^1||N|v3(N)=6,12, or an even number ≥14|
|{3,5,13,19}|5^1||N|3²||N|

No existence is asserted for the surviving branch. None of these three supports has been wholly excluded by this theorem.

**Proof and replay.** Since 3|(e+1), 3·127=σ(19²) divides σ(19^e); also σ(19^e)/19^e≥381/361. Treat 19² as an abundance and incoming-divisor lower bound, never as an *upper bound* on v19(N). For each row split on the indicated Euler candidate, then on 3. At each split enumerate all even exponents h≤12 plus the possible Euler exponents 1,5,9, and an unrestricted integer tail h≥13. At a finite node, the *odd part* of σ(r^h) divides N. Add valuations across different fixed components using σ(N)=2N. Partial factorization is allowed: each credited prime is odd, trial-division proved prime, and its exact claimed power is checked to divide the original odd part. A forbidden support divisor or excess incoming valuation at an exact node makes that branch impossible.

For every distinct forced prime u, its exponent is at least its incoming multiplicity, the support minimum 1, and any split-tail minimum. The abundance σ(u^h)/u^h is increasing. Use the smallest even h meeting these minima, skipping only an initial run whose sigma is proved divisible by a forbidden prime. Permit one Euler adjustment at any compatible u≡1 (mod 4) with h≡1 (mod 4); even and Euler exponents are both accounted for in each tail. If the product of all these rational lower bounds is strictly larger than 2, N is impossible. The two-level checker returns the complete list of surviving branches. `python -I -S -B Verify.py` replays the three rows without any external dependencies. The dictionary entry `19:2` printed in these traces denotes the proxy, not the actual e.

**Projection, not a new closure.** `python -I -S -B Verify.py REPOSITORY` optionally rebuilds the support ledger (archived SupportSplit, published Support/Ledger.json, global hit {3,5,17,19}, current Delta). Among the original 244 actual exponents there are 6556 previously open support triples, 413 distinct previously proved support-only exclusions, and 14 still-unexcluded exact (19,e,H) triples whose internal Euler/3 branches are now constrained. On the observed Delta containing 100 proved actuals, four of the 14 are already covered by a complete exponent; **10** open triples are sharpened. New complete mask exclusions = **0**, new complete exponents = **0**; count of previously open triples remains 4156 across 144 surviving actuals. The exact Delta digest and ten cells appear in Verified.txt. A development search in the parent workspace once treated an even remainder as a label; those provisional whole-mask claims are withdrawn. This package strips all powers of two before factor enumeration, checks every claimed label, and verifies the surviving branch itself rather than suppressing it.
