# Conditional prime-61 linear programs for target 10^2400

Assume an odd perfect number is coprime to
\(S_8=\{3,5,7,11,13,17,19,31\}\) and divisible by \(61\).

Because \(61\equiv-1\pmod{31}\), every odd exponent \(e\) forces
\(31\mid\sigma(61^e)\), contradicting \(31\nmid N\).
The possibilities \(e=2,4,8\) are excluded by exact divisibilities:

- \(\sigma(61^2)=3\cdot13\cdot97\),
- \(\sigma(61^4)=5\cdot131\cdot21491\),
- \(\sigma(61^8)\) is divisible by \(3\cdot13\cdot19\).

It follows that the exhaustive cases for \(e=\nu_{61}(N)\) are
\(e=6\) and even \(e\ge10\).

The stand-alone primal/dual pilot
`IntervalCertificate61.py` adds one inequality

\[
-\sum_{a\in A}x_{61,a}\le-1
\]

to the baseline LP. The model already includes
\(\sum_a x_{61,a}\le1\), so this forces exactly one allowed exponent
group. For \(A=\{6\}\), it fixes \(61^6\parallel N\). For
\(A=\{10,12,14,\text{ordinary tail }\ge16\}\), it forces
\(\nu_{61}(N)\ge10\). A new nonnegative dual multiplier contributes
to the reduced costs and to the certified objective; the certificate
generator verifies these changes with interval arithmetic.

The original LP's \(\sigma(61^6)=52379047267\) factor implication is
retained for the exact-6 case. The program deliberately relaxes unknown
factors in the tail rather than pretending to have a complete factorization.

A conditional certificate does **not** imply the unconditional \(10^{2400}\)
bound: the eight excluded-prime root branches must all be proved, and the LP
model must undergo a proof-grade independent audit.
