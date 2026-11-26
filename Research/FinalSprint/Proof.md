# Final elimination sprint: exact-exponent certificates

Assume that \(N\le 10^{2400}=B\) is an odd perfect number. Use the canonical root order \((19,7,11,31,13,3,5,17)\); all roots before the specified root are absent. The starting point is [main at 2b53c830](https://github.com/stormwhip/PerfectNumbers/commit/2b53c830dd903b460a315df04fa3a4a410fb8357), not an earlier progress estimate.

**Theorem.** The canonical root and its exact exponent cannot be \((7,168)\).

**Proof.** Write \(A=\sigma(7^{168})\). The certificate tests primality of

```
471014884186461786359976424959315520118992312411810290816288422077055549979204503
```

and exact division into \(A\); denote this prime by \(t\). Thus \(t\mid N\). For \(c=v_t(A)\), all candidate exponents \(f=v_t(N)\) obey \(f\ge c\) and \(7^{168}(A/t^c)t^f\le B\). Enumerate up to this monotone endpoint. Euler parity, forbidden primes, overflow of a fixed valuation, abundance greater than two, and the integer size bound leave six nontrivial cases: \(2,4,6,8,10,12\). For each the [packet](Tree7x168.json.gz) specifies a finite forest. At fixed components with product \(X\), the prime-to-\(X\) part \(D\) of the product of their odd divisor sums satisfies \(XD\mid N\). A child activates only on actual divisibility; the newly charged divisor-sum parts are stripped of all fixed and forest labels, so products from distinct sources are justified by multiplicativity. Every compatible exponent is either checked or covered by the bare prime-power bound at the start of its tail. Only one node can receive an Euler discount. Applying the [exact tree theorem and verifier](../Session20261126/TreeCheck.py) gives a lower bound strictly exceeding \(B\) on each of the six leaves, independently priced by [a second integer recursion](../Session20261126/PivotCheck.py). Hence no candidate remains. This uses exact exponents throughout, not divisibility lifting. ∎

**Coverage.** This first packet shortens `P7_I00005`; it does not alone close it. The [current projection](Delta.json) gives every open shard ID with all its remaining exponents. The [verifier](Verify.py) rebuilds that projection after rechecking the new arithmetic. Historical certificates and their ledgers are unchanged. From the repository root:

```
python -I -S -B -X int_max_str_digits=0 Research/FinalSprint/Verify.py
```
