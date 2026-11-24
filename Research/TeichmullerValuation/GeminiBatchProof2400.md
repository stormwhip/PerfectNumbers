# Gemini batch replay, 2026-11-24

The independent verifier confirms 51 exclusions under the existing root-order assumptions and bound \(B=10^{2400}\). The exclusions close 12 of the previously open shards. The checked-in audit lists the exact root/exponent pairs and shard IDs. The existing [Teichmüller audit](Audit2400.json) is the input manifest. The [batch audit](GeminiBatchAudit2400.json) records the 12 additions. Pass `--remaining PATH` to write the resulting frontier.

```sh
python3 Research/TeichmullerValuation/AuditGeminiBatch2400.py
```

## Valuation bounds

Write \(N=p^e q^a M^2\) with Euler prime \(q\), and \(A=\sigma(p^e)\). Set \(s=v_p(\sigma(q^a))\), so the primes of \(M\) supply precisely \(e-s\) units. Use the baseline Teichmüller pricing with slope \(\kappa\) and include only deficit levels at most \(e-s\) when \(s\) is fixed. The surplus calculation minimizes \(r^f/p^{\kappa v_p(\sigma(r^f))}\) over even \(f\) at or above the required valuation. At each LTE level \(j\) it uses the least admissible exponent; beyond the first level with \(op^j\) above the minimum exponent, the ratio grows by the baseline LTE increment bound.

For \(a\ge5\), the Euler factor pays \(p^{5s}/D_5\). Order one gives \(a\ge 2p^s-1\) when \(s>0\). Order two gives \(q\ge 2p^t-1\) for \(t=v_p(q+1)\), and \(a\ge 2p^j-1\) if \(j=v_p((a+1)/2)>0\). For order at least three, the minimal legal exponent is at least five. A prime \(q<p^t\) is exactly the least positive Teichmüller lift and is checked for a possible deficit. Each extra LTE level is paid by \(5^{6(p^j-1)}\ge p^{5j}\), using \(7\le p\le31\). Since \(\kappa\le4\), the final lower bound can drop the factor \(p^{(5-\kappa)s}\).

Deleting a deficit requires either a verified forbidden divisor at the only deficient exponent or a distinct surplus prime forced by that exponent. Each sponsor is reserved once and is distinct from every deficit prime and every factor used for an additional valuation surplus. In an Euler-one branch a sponsor congruent to 1 modulo 4 is used only when it cannot be Euler. If the emitter could equal a sponsor, the corresponding deficit is restored. Known factors of \(A\) are verified by deterministic 64-bit Miller–Rabin and exact valuation.

## Euler exponent one

For \(s=0\), use \(q\ge5\). For \(s>0\), walk \(q=(4k+2)p^s-1\), skipping only certified composites and candidates with the wrong \(p\)-adic valuation. At each retained lower bound, the valuation price gives an upper bound on \(q\). For \(q\mid A\), every relevant cyclotomic factor is checked by exact division within the CRT progression. If \(q>h\) and \(q\mid\Phi_h(p)\), its order is \(h\); the companion factor is also \(1\pmod{2h}\) when \(\gcd(\Phi_h(p),h)=1\). An unfinished progression is treated as open. No additional quadratic-nonresidue multiplier is used.

If \(q\nmid A\), at least one non-Euler prime \(r^f\parallel M^2\) supplies \(q\mid\sigma(r^f)\). Write \(b=v_p(\sigma(r^f))\). Then \(r^f>2p^b q/3\). When \(r\nmid A\), multiply the valuation bound for the other primes by the size bound using \(A\) and \(r^f\), with weights \(1\) and \(\kappa-1\), to cancel \(b\). In the size bound, each known odd valuation of \(A\) can be rounded up to the next even valuation since \(q\nmid A\).

For \(r^c\parallel A\), write \(f=c+g\), \(P=p^{e+1}\), \(Y=p^s\), \(U=(P-1)/r^c\) and \(w=\sigma(r^f)/q\). Then
\[
D=U(w(r-1)-1)-r^{g+1},\qquad qD=(P-1-q)r^{g+1}-U(q+1).
\]
Reduction modulo \(Y\) gives \(Y\mid D\). The integer \(D\) is odd, since \(U\) is even and \(r\) is odd, so \(D\ne0\). The two signs imply \(r^{g+1}>Y\) or \(r^{g+1}>Yq/P\), respectively. Combine these inequalities with \(r^c\mid A\) and \(N\ge p^e q A_g r^g\), where \(A_g\) rounds up the known odd valuations of primes other than \(r\). The resulting interval bounds \(c\) and \(r\), and \(\sigma(r^f)/q\) then bounds \(p^b\). If the interval still permits a case at the enumeration limit, the verifier leaves the exponent open. The bounds use the lower endpoint for \(q\) throughout and therefore apply to all larger eligible \(q\).

The replay replaces the submission's quadratic-nonresidue bonus and its case-specific emitter bounds. The former needs a disjointness argument when other surplus factors are already priced. The latter are replaced by the two signs of \(D\) and a finite interval check. In particular, divisibility of \(f+1\) by 5 or 11 is necessary for positive valuation at \(p=11\); the residue class of \(r\) still matters.
