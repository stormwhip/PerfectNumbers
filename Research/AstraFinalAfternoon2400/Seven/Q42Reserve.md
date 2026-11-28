# Exact 173 exponents 78 and 106 below Q^42

At canonical `(7,12)`, assume odd perfect \(N\le B=10^{2400}\), \(19\nmid N\), \(7^{12}\Vert N\), \(Q^{42}\Vert N\) for \(Q=16148168401\). The [packet](Forest12Q42Reserve.json.gz) excludes exact \(v_{173}=78,106\). It asserts neither the whole first-pivot fiber nor the root key.

Fix \(R=173\) and an exact \(R^h\). Let \(X\) be the fixed mass; \(c=42-v_Q(S)\), \(j=h-v_R(S)\), where \(S\) is the product of the fixed sigma blocks. The Euler prime is not among these even components and may have **any** Euler exponent \(4a+1\). Write its sigma as \((q+1)\sum_{b=0}^{2a}(q^2)^b\) and charge the square geometric atom, distinct from all ordinary prime atoms. Use the frozen [common-order-43 weights](../../FinalNight2400/SevenNext/Odd42.md) with square admissibility as in [JointEven](../../FinalNight2400/SevenNext/JointEven.md): the weight at \(Q\) is 2, the weight at \(R\) is 38. When an odd \(Q\)-order is divisible by 43, reserve 40 of the \(o-1\) base index powers for \(R\), leaving \(o-41\ge2\). At \(R\) allocate 40 for order 43, and its LTE shift is paid by the length surplus. When the orders do not share 43 the effective lengths multiply, allowing the individually allocated powers; \(R\nmid Q-1\). Order one at \(Q\) is impossible by the length limit and at \(R\) is paid by its length factor. The fixed loss kernel validates each order budget at least its corresponding weight when relevant. Thus for positive loss at depth \(b\), the entire permissible base range is strictly below \(p^b\), and there is **at most one** legal progression representative per Hensel residue; no high-weight shortcuts or omitted lifts. Squares of admissible Euler primes must be retained, including when a prime-only compositeness filter would reject the square.

For each **exact** Euler linear allocation \((i,k)\) within \([0,c]\times[0,j]\), with \(m=Q^iR^k\), \(q\equiv2m-1\pmod {4m}\), hence \(q\ge2m-1\). The exact standard price excludes any cell where
\[
 X(2m-1) Q^{2(c-i)}R^{38(j-k)}>BU.
\]
For every other cell, the verifier requires at least one stored forest at coordinate \((a,b)\) with \(a\le i,b\le k\). Because \(m_0=Q^aR^b\mid m\) is odd, \(2m-1\equiv2m_0-1\pmod{4m_0}\). The whole cell is therefore contained in the stored weaker Euler congruence and its valid exact forest inequality; no monotonicity of forest values is being presumed. The chosen forest explicitly verifies that every tracked label is incompatible with that weaker congruence, so all tracked labels are ordinary.

Reserve \(q\ge2m_0-1\) once. For each anonymous residual \(Z\), test every possible multiplicity \(u\ge0\) with \((2m_0-1)^u\le Z\); any \(Z/q^u\) must be in its required cofactor progression. If there are multiple candidates, the least positive candidate is a valid lower bound for the whole interval; if exactly one candidate fits, exact nondivisibility may reject it. No upper bound on the Euler exponent is imposed apart from the integer limit for each residual. Use the minimum of all remaining options (including \(u=0\)). All non-q occurrences are disjoint from the reserved q power, and the result is a conservative lower bound even if independent rebates relax joint occurrence of q across anonymous blocks. Both [the generic reserved forest](ReservedForest.py) and the separate recurrence inside [the verifier](VerifyQ42Reserve.py) must exceed \(B\) for each stored weaker congruence.

| \(h\) | Direct price cells | Cells covered by weaker reserved congruence | Stored forests | Minimum strict lower bound in millionths of \(B\) |
|---:|---:|---:|---:|---:|
| 78 | 2672 | 604 | 6 | 16407746 |
| 106 | 3912 | 540 | 6 | 1100327413 |

The certificate has 146 ECPP chains, SHA-256 `e272183658f5b408172f63f1c7a2f8a1060cc2fac8d73c6f7d194bcaf7c9e8ed`. Author isolated replay passed in 195.526 s:

~~~powershell
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Seven/VerifyQ42Reserve.py
~~~
