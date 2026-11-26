# Final elimination sprint: exact-exponent certificates

Assume that \(N\le 10^{2400}=B\) is an odd perfect number. Use the canonical root order \((19,7,11,31,13,3,5,17)\); all roots before the specified root are absent. The starting point is [main at 2b53c830](https://github.com/stormwhip/PerfectNumbers/commit/2b53c830dd903b460a315df04fa3a4a410fb8357), not an earlier progress estimate.

**Theorem.** The canonical root and its exact exponent cannot be \((7,168)\).

**Proof.** Write \(A=\sigma(7^{168})\). The certificate tests primality of

```
471014884186461786359976424959315520118992312411810290816288422077055549979204503
```

and exact division into \(A\); denote this prime by \(t\). Thus \(t\mid N\). For \(c=v_t(A)\), all candidate exponents \(f=v_t(N)\) obey \(f\ge c\) and \(7^{168}(A/t^c)t^f\le B\). Enumerate up to this monotone endpoint. Euler parity, forbidden primes, overflow of a fixed valuation, abundance greater than two, and the integer size bound leave six nontrivial cases: \(2,4,6,8,10,12\). For each the [packet](Tree7x168.json.gz) specifies a finite forest. At fixed components with product \(X\), the prime-to-\(X\) part \(D\) of the product of their odd divisor sums satisfies \(XD\mid N\). A child activates only on actual divisibility; the newly charged divisor-sum parts are stripped of all fixed and forest labels, so products from distinct sources are justified by multiplicativity. Every compatible exponent is either checked or covered by the bare prime-power bound at the start of its tail. Only one node can receive an Euler discount. Applying the [exact tree theorem and verifier](../Session20261126/TreeCheck.py) gives a lower bound strictly exceeding \(B\) on each of the six leaves, independently priced by [a second integer recursion](../Session20261126/PivotCheck.py). Hence no candidate remains. This uses exact exponents throughout, not divisibility lifting. ∎

**Two singleton closures by simultaneous valuation.** The canonical pairs $(31,388)$ and $(11,108)$ are impossible. The [joint deficit lemma and proof](JointValuation.md) applies to the full vector of incoming prime-power demands on each hard path. For $(31,388)$ the difficult leaf fixes the 85-bit pivot $29941246365965400246754591$ at exponent 18; all 7,002 Euler-one windows and the high Euler case are excluded. The other seven forest leaves and eight direct contradictions are covered by the [complete tree](JointTree31x388.json.gz). For $(11,108)$ the difficult path fixes two further primes at exponents 6 and 16. All 10,464 Euler-one windows (5,978 by price; 4,114 by block size; 372 by the remaining interior tests) and high Euler are excluded. The other 1,162 forest leaves, 54 split nodes and 1,294 direct cases are checked from the [full tree](JointTree11x108.json.gz). Thus `P31_I00075` and `P11_I00027` close: each had just the stated exponent. ∎

**Two further singleton forest proofs.** For $(7,70)$ and $(19,352)$ the [root-seven tree](Tree7x70.json.gz) and [root-nineteen tree](Tree19x352.json.gz) use the same exact splitting, valuation, Euler and disjoint-charging proof as above. Every split selects a proved prime dividing the compulsory part $D$, and enumerates every feasible actual exponent; both integer lower bounds must pass on every remaining leaf. The respective counts (forest leaves, splits, direct contradictions) are (568,40,618) and (282,13,297). The integer tail is part of every forest test. This exhausts `P7_I00019` and `P19_I00069`. ∎

**Additional complete trees.** The same exact forest theorem applied to the [7,46](Tree7x46.json.gz), [19,348](Tree19x348.json.gz), and [31,348](Tree31x348.json.gz) packets contradicts $N\le B$ on every compatible branch. Their respective (forest, split, direct) counts are (754,24,786), (1516,107,1669), and (861,53,1157). For [11,42](JointTree11x42.json.gz) the partition requires three additional price leaves: the second and third fixed primes alone suffice as valuation targets, keeping all fixed components in the mass. The first two paths fix their exponents at (16,28) and a fourth at 30 or 36, and the third fixes them at (16,46). The three window counts are 448, 448 and 736; none survives. Another 443 forest leaves, 27 splits and 491 direct cases finish the domain. All four previously singleton obligations close. ∎

The [7,90 certificate](Tree7x90.json.gz) likewise excludes that exact exponent by 454 forest leaves, 16 splits and 469 direct cases. It removes a membership in each of `P7_I00003` and `P7_I00005`; neither closes. The latter now requires only 12.

**Coverage.** The $(7,168)$ packet shortens `P7_I00005`; it does not alone close it. The [current projection](Delta.json) gives every open shard ID with all its remaining exponents. The [verifier](Verify.py) rebuilds that projection after rechecking the new arithmetic. Historical certificates and their ledgers are unchanged. From the repository root:

```
python -I -S -B -X int_max_str_digits=0 Research/FinalSprint/Verify.py
```
