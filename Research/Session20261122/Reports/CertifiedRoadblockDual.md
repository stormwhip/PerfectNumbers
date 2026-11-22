# Certified roadblock dual for the \(10^{2400}\) search

> **进度标注（2026-11-22）**：本文记录对应阶段的数学推导、实验数据和当时的搜索状态。最新研究进度、独立验证器 V2、可恢复前沿及全量未闭合项目，统一见 [CurrentStatus2400.md](../../../Documentation/CurrentStatus2400.md)。本文历史计时和程序 `PROVEN` 均不作为 `10^2400` 完整证明。


Baseline: [V21](../../../Sources/Cpp/ProofTreeV21.cpp#L712-L845). The research report [10_2400.md](https://chatgpt.com/library?file_id=libfile_569b2ac8e8c881918d81ab694cc0457e&account_id=personal) proposed replacing the rule that reserves the first eligible prime for the Euler special component. This experiment supplies an integer-arithmetic reference implementation and checks a faster formula for evaluating a candidate multiplier. Production integration and replay of reachable nodes remain open.

## Safe lower bound

Fix a proposed boundary \(b\), the prime table limit \(P\), the set \(B\) of already expanded primes, and the forbidden set \(F\). For new prime components with minimum prime at least \(b\), exclude \(F\cup B\) and extend the forbidden set by all odd primes \(r<b\) outside \(B\). Let \(\Delta\ge0\) be a certified lower bound on the remaining log-abundancy requirement.

For each finite candidate \(q\), use \(h_q=\log(q/(q-1))\) as an upper bound on its log-abundancy. Its even log-cost is \(c_{q,0}=a_0(q)\log q\), where \(a_0(q)=4\) when an effectively forbidden prime divides \(q^2+q+1\), and \(a_0(q)=2\) otherwise. Its special log-cost, if allowed, is \(c_{q,1}=\log q\). Every Euler exponent \(4u+1\) satisfies \(q+1\mid\sigma(q^{4u+1})\), so an odd forbidden divisor of \((q+1)/2\) rules out all such exponents. Special choices also require \(q\equiv1\bmod4\) and an unused Euler slot.

Set \(t=P+1\), which is a lower bound on every omitted prime. Permit arbitrary continuous even-tail abundancy at cost \(2\log(t)/h_t\) per unit. If the Euler slot is available, admit one relaxed tail special option of cost \(\log t\) and abundancy \(h_t\). Monotonicity of \(\log q\) and \(h_q\) proves that these tail options cover every actual omitted component.

For a rational \(\mu\in[0,2\log(t)/h_t]\), write \(r_{q,j}=c_{q,j}-\mu h_q\) and \(m_q=\min(0,r_{q,0})\). The special-slot penalty is
\[
\gamma=\max\!\left(0,\ \max_{q\ {\rm special\ eligible}}\{m_q-r_{q,1}\},
                    \ \mu h_t-\log t\right)
\]
when the slot is available, and \(0\) otherwise. Every finite chosen component has reduced cost at least \(m_q\) after adding the penalty to a special choice. Unchosen components contribute \(0\ge m_q\), and the tail reduced costs are nonnegative by the cap on \(\mu\) and the tail term of \(\gamma\). Summing and accounting for at most one special choice proves
\[
L(\mu)=\mu\Delta+\sum_q m_q-\gamma
\ \le\ \sum_{\rm new\ components} a\log q.
\]
A boundary is safe when its checked lower bound strictly exceeds an independently certified upper bound on the remaining log-size budget. This implication applies to any checked boundary, including a boundary proposed by an approximate search.

### Two searches per exponent stream

For a fixed exponent class \(a_0\in\{2,4\}\), sort the candidates by \(q\). The even reduced costs are increasing. Their negative portion is a prefix, so one binary search and two prefix sums yield its total.

On the eligible special subsequence of that same class, the penalty contribution is
\[
m_q-r_{q,1}
  =\min\big((a_0-1)\log q,\ \mu h_q-\log q\big).
\]
The first term increases with \(q\), and the second decreases. The maximum is attained at one of the two neighbors of the crossing \(a_0\log q=\mu h_q\). Search the special subsequence separately so that both neighbors are eligible. Each multiplier therefore takes \(O(\log n)\) comparisons and a constant number of prefix sums after constructing the two finite streams of \(n\) options for a boundary. This complexity counts integer arithmetic operations and excludes per-boundary construction.

The unrounded dual as a function of \(\mu\) is concave. It is the pointwise minimum over choosing no special component, any one eligible finite special component, or the relaxed tail special component. Each alternative is an affine term plus a sum of minima of affine terms. The prototype uses a bounded one-dimensional search and emits a short dyadic multiplier. The bound is certified for the returned multiplier independently of how close the search came to the optimum.

### Directed arithmetic

[RoadblockDual.py](../Python/RoadblockDual.py) evaluates costs using lower endpoints and abundancies using upper endpoints at scale \(2^{80}\). It range-reduces \(\log(n/d)\) to \([1,2]\), applies the positive \(\operatorname{atanh}\) series with \(z=(n-d)/(n+d)\le1/3\), and encloses the 32-term remainder by \(3z^{65}\). Integer floors and ceilings enclose every term. These endpoints preserve the stream order because each range-reduced series endpoint is monotone, including across powers of two. The tail cap uses \(2\log_{\rm lo}(t)/h_{t,\rm hi}\), and the final bound is rounded down. The prototype accepts the node gap as a lower endpoint. An integration must derive that input and the budget upper endpoint separately from certified node data.

## Reproduction and results

From the repository root:

~~~bash
python Research/Session20261122/Python/RoadblockDualTests.py
python Research/Session20261122/Python/RoadblockDualTests.py --compare-lp
~~~

The first command needs only Python. The optional comparison uses SciPy HiGHS. The tests check 200 small integer-enumerated cases, 800 exact comparisons of the prefix-sum implementation against a linear scan, and 200 comparisons against an independently formulated fractional LP. The largest difference from HiGHS was \(9.15\times10^{-11}\) in natural-log units. HiGHS is a numerical cross-check. Integer arithmetic establishes the certified inequality.

For the report's synthetic \(b=29\) example, with the V21 prime-table limit \(300000\), the finite-power target produces a certified bound of \(55.816710071\), below the feasible remaining configuration's cost \(56.240146166\). The larger target defined with infinite-power abundancies produces \(56.240146166\) to nine decimals. The former greedy rule returned approximately \(63.255079179\) for the finite-power target. The synthetic state demonstrates the issue in the relaxed selection rule. Reachability and impact in V21 require replay from real states.

A cold Python build of the finite streams for the synthetic \(P=300000\) case took about \(1.10\) seconds. Searching for a multiplier on the built streams took about \(4.1\) ms. These are single reference-run timings. The construction cost dominates and must be measured again on reachable states.

## Open work

1. Add an experimental V21 trace for reachable roadblocks with an unused Euler slot. Capture \(b\), \(B\), \(F\), the node abundance bound, the size budget, and the residual evidence needed to recompute both endpoints, including cases where the old boundary fails the new check.
2. Benchmark stream construction and boundary selection on those traces before enabling the rule in a search. The reference scans the table per boundary and checks forbidden divisibility directly. The existing C++ sigma-factor tables and exclusion marks are available for a streamed implementation. A certified tail and a directly verified final boundary should also cover fallback when a candidate multiplier is weak.
3. Once matched replay is complete, compare completed-shard wall time, roadblock width and outcomes on the existing root-19 suite. An independently certified terminal LP for the alternative \(19\to23\) root set and the complete eight-root run remain separate milestones.
