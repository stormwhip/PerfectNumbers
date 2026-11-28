# Complete exact t^10 first-pivot fiber at canonical (7,438)

Under the canonical odd perfect number hypothesis \(N\le10^{2400}\), \(19\nmid N\), \(7^{438}\Vert N\), and \(t^{10}\Vert N\) for \(t=572749682520506652634407616247\), the reserve packets exclude 21 exact \(v_{67}\), disjoint from the [57 unrestricted-Euler forest exclusions](Proof.md). Combined with the 72 frozen exclusions, this exhausts the 150 directly feasible even values \(2,4,\ldots,300\), closing the **entire exact first-pivot fiber \(v_t(N)=10\)**. It does not close the distinct \(t^{12}\) first fiber or the root key. No Hensel lifting or high-weight pricing is used in the new forest arithmetic.

## Why Euler has exact exponent one

This replays just the source restriction from the [frozen proof](../../FinalNight2400/Seven/Verify438.py). Write \(X=7^{438}t^{10}\), \(A=\sigma(7^{438})/t\), \(C=\sigma(t^{10})\). The recursive Lucas certificate authenticates \(t\); direct arithmetic gives \(v_t(\sigma(7^{438}))=1\), no further \(t\) from \(\sigma(t^{10})\), and \(XAC\mid N\). Any component index \(h+1\le5100<t\) by size, so its residual \(t\)-supply cannot come from an order-one length or an LTE length shift. The only possible nontrivial ordinary order is 439 (the only odd divisor of \(t-1\) in 3..5100). Since \((t-1)\equiv2\pmod4\), an Euler supplier can have order 2, 439 or 878; in the last two cases its Euler index is even and at least 878. The verifier tries all odd bases \(z\) with \(Xz^{438}\le B\) for the order-439 ordinary case and all bases \(q\equiv1\pmod4\) with \(Xq^{877}\le B\) for the nonquadratic Euler case, until the first monotone failures. Neither can supply. Thus all nine residual units come from \(q+1\) at the actual Euler prime \(q\).

Let \(m=t^9\), \(L=2m-1\), \(M=4m\). Then \(q\equiv L\pmod M\), \(q\ge L\). To exclude \(q\mid A\), test the full compatible cofactor interval: \(a=A/q\equiv A L^{-1}\pmod M\), \(1\le a\le\lfloor A/L\rfloor\). It has no candidates or just one that does not divide \(A\); the checker explicitly verifies this alternative. If \(q\mid C\), the order of \(t\) modulo \(q\) divides the odd number 11 (including order one), making \((t/q)=1\). But reciprocity with \(q\equiv1\pmod4\), \(q\equiv-1\pmod t\), and \(t\equiv3\pmod4\) gives \((t/q)=(q/t)=-1\). Thus \(q\nmid AC\), and \(XAC L^5>B\) rules out every Euler exponent ≥5. Hence \(q\Vert N\). The later forest does **not** presume \(q\) external to \(\sigma(67^h)\) or other emissions.

## Reserved ordinary forest

Under each of the twenty-one fixed prefixes, authenticate every declared prime, its root or owner status, and its membership outside the residue class of \(q\). All forest vertices are thus ordinary. Use the validated disjoint-support forest of [Proof](Proof.md), but charge the separate lower bound \(q\ge L\) in front. Prune **only** the possible already-paid factor \(q\) from each residual block (both the initial non-root portion of \(D\) and each ordinary vertex's anonymous part). If a residual integer \(Z\) contains the actual \(q\), it contains it exactly once because \(q\Vert N\) and \(Z\mid N\). Its cofactor is congruent to \(ZL^{-1}\pmod M\) and lies in \([1,\lfloor Z/L\rfloor]\). Let \(r\) be the least positive representative. If no representative is in range, or the only representative does not divide \(Z\), retain \(Z\); otherwise use \(\min(Z,r)\). This explicitly includes **all** possible cofactors; when several representatives fit, retaining the least is a lower bound, not a restriction of their possibilities. If today's relaxation independently discounts an impossible q occurrence in more than one residual, the bound merely becomes weaker. After rebate, each underlying actual residual can be taken coprime to \(q\), so charging \(L\) once cannot double bill it. Forest costs and tails use integer arithmetic only.

The [replay](VerifyReserved438.py) checks both the [first evaluator](ReservedForest.py) and a separately implemented ordinary exponent recursion based on the modular inverse and full progression interval. Both lower bounds must be strictly >B. No discovery factorizations are trusted.

~~~powershell
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Seven/VerifyReserved438.py
~~~

| Packet | Exact \(v_{67}\) | ECPP | SHA-256 | Minimum integer lower bound, millionths of \(B\) |
|---|---|---:|---|---:|
| [438d](Forest438d.json.gz) | 14,20,44,48,56,60,62,82 | 392 | `58e8aad743b97dde1b36e3600a20d4e4b6f279280d6b2f35b3786dbb42c6ca53` | 84237650 |
| [438e](Forest438e.json.gz) | 10,18,32,40,46,124 | 75 | `559d2611668771f5611ceed4931065af054d81215ebcf2da9a0899b765a4014c` | 1174141 |
| [438f](Forest438f.json.gz) | 4,6,24,80 | 264 | `c2b478fc7f053706871d056972a5012e10353d8b901c43168eb0a21e32d8d939` | 2696589 |
| [438g](Forest438g.json.gz) | 8,26 | 35 | `4bf08389280411e00057985f6d9ae74daa2a9834be8da4062aa1092c37f01c0b` | 3643823 |
| [438h](Forest438h.json.gz) | 2 | 66 | `85963c75940864d92a5c108e3e3a24bc4c68b8291dbb6172e343c47f73c59dac` | 3741154 |

## Exact full-fiber composition

Run the [integrated verifier](Full438Ten.py) with `--historical` to replay both the newly sealed packets and the actual historical arithmetic used to cover the complement. It regenerates the complete 67 exponent domain and tests exact set disjointness, not just matching counts. The four frozen groups are [33 initial](../../FinalNight2400/Seven/Verify438.py), [15 further](../../FinalNight2400/SevenNext/Verify438New.py), and [10](../../FinalNight2400/SevenNext/VerifyMixed67.py) + [14](../../FinalNight2400/SevenNext/VerifyMixed67More.py) mixed-price exclusions. These last historical prices use only weights 19/10 with sufficient exponent budgets for their documented least-representative bound; this is unrelated to the incomplete high-weight coverage withdrawn in PR #11. The three unrestricted packets add 57, and the five reserved packets add 21. First-fiber closure grants no whole-key or shard credit.

~~~powershell
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Seven/Full438Ten.py --historical
~~~
