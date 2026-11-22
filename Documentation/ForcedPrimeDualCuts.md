> **历史理论笔记。** 文中 V17 联合 Euler 特殊素数剪枝曾通过测试，但未证明端到端加速；V17 源代码保存在 [精简前快照](https://github.com/stormwhip/PerfectNumbers/tree/124ab21449d4afd9d017a32faa9bd27253943c70)。当前工程采用 V16 的正确区间增益。完整状态见 [ProgressReport2400](ProgressReport2400.md)。

> **当前状态**：原根集互素类已有独立整数证书；包含根素数的 3,072 个顶层分片仍未形成完整独立验收。本文为专项理论与历史实验说明，最新全量状态见 [CurrentStatus2400.md](CurrentStatus2400.md)。


# Early-State Affine LP Cuts and Forced-Prime Dual Gains

## Research question

The V12/V13 pruning implementation waited until every forced prime had been assigned an exponent. At that point the factor-chain DFS had already explored most of the branch. V14 evaluates the same affine dual bound **before** branching on the next forced prime. V15 additionally charges a lower bound for each prime known to divide the hypothetical odd perfect number but whose exponent has not yet been chosen.

The two mechanisms are independent, allowing reproducible V13/V14/V15 ablation.

## Certified-dual algebra

Consider an LP relaxation with inequality constraints \(Ax\le b(R)\), cost \(c^Tx\), and variable bounds \(0\le x_i\le1\). An admissible dual penalty vector \(\lambda\ge0\) gives, for every feasible \(x\),

\[
c^Tx\ge-\lambda^Tb(R)+\sum_i r_i x_i,
\qquad r_i=c_i+(A^T\lambda)_i.
\]

Let \(\underline r_i\) be an outward-rounded lower endpoint satisfying \(\underline r_i\le r_i\). Without further information, each bounded variable contributes at least \(\min(0,\underline r_i)\).

For a specific prime \(q\) whose occurrence has already been proved by a factor-chain divisor-sum implication, exactly one of its prime-power exponent options is selected:

\[
\sum_{i\in I_q}x_i=1,\qquad x_i\ge0.
\]

Therefore

\[
\sum_{i\in I_q}r_ix_i\ge\min_{i\in I_q}\underline r_i,
\]

and the **additive forced-prime gain** is

\[
\boxed{
g_q=
\min_{i\in I_q}\underline r_i
-
\sum_{i\in I_q}\min(0,\underline r_i)
\ge0.
}
\]

The inequality \(g_q\ge0\) follows since \(\sum_i\min(0,\underline r_i)\le\min_i\underline r_i\). Distinct primes have disjoint exponent-option groups, so gains for multiple forced primes add.

When an entire prime group is already forbidden or its exponent has been branched, V13's previously implemented variable-removal gain applies instead. A prime may contribute to *one* group adjustment only.

## Affine abundance target

The precomputed LP dual was constructed for target abundancy ratio \(R=2\), but the same dual multipliers yield a lower bound for any \(R>1\):

\[
L_F(R)\ge c_F+\lambda_F\log R.
\]

For a factor-chain state with previously branched primes \(B\), grant each known prime **its full infinite-exponent abundancy**:

\[
A_B^+=\sum_{p\in B}\log\frac{p}{p-1}.
\]

This is optimistic for every ordinary or Euler-special exponent. The unknown factors must then contribute at least

\[
\log R=\log 2-A_B^+.
\]

Any unbranched forced prime belongs to the unknown factor group, with its ordinary/special exponent still chosen by the LP. Thus the affine LP can be evaluated **before** its exponent is branched.

For the benchmark, stored prefix certificates are computed by the interval arithmetic LP implementation for the two tested masks (7 and 127). All other masks receive the trivial \(L_F(R)\ge0\) certificate, which is safe for positive log-size costs. The benchmark distinguishes this accelerated *targeted* generation from the full 256-mask production procedure.

## Limits to audit before a mathematical theorem

1. Verify the primal LP correctly relaxes all possible odd-perfect-number prime powers, including the infinite prime and exponent tails.
2. Validate that the recorded factor-chain implication really forces each unbranched \(q\) to divide \(N\), using proof-grade primality certificates and exact divisibility.
3. Validate the certified dual reduced-cost endpoints and every CSV record independently; the CSV stores already reduced affine data rather than the full multipliers.
4. Replace heuristic double-precision margin guards with exact, reproducible enclosures if a new unconditional lower bound is claimed.
5. Require the complementary LP certificate and complete exhaustive proof trees for the chosen root set and bound.

## Tests and reproducibility

- Baseline: `ProofTreeV13Optimized.cpp`.
- Earlier intermediate-state affine LP: `ProofTreeV14.cpp`.
- Forced-prime dual adjustment: `ProofTreeV15.cpp`.
- Isolated regression tests: `ProofCoreTestsV14.cpp`, `ProofCoreTestsV15.cpp`.
- Two-mask interval-dual data generator: `TargetedPrefixCertificates.py`.
- Matched benchmark: [ForcedPrimeLpBenchmark.yml](https://github.com/stormwhip/PerfectNumbers/tree/124ab21449d4afd9d017a32faa9bd27253943c70).

Full result details belong in [ExperimentLog](../Records/ExperimentLog.md).

## Matched benchmark results (2026-11-22)

The bounded workflow [44998508242](https://github.com/stormwhip/PerfectNumbers/actions/runs/44998508242) finished successfully. Mask 127 has a precomputed interval-dual lower exponent **1644.682315669432**.

| Exponent/root | V13 branches/time | V14 branches/time | V15 branches/time |
| --- | --- | --- | --- |
| 1000 / 17 | 7,709 / 6.030 s | 0 / 0.0064 s | 0 / 0.00033 s |
| 1000 / 31 | 21,408 / 15.192 s | 21,408 / 15.204 s | 21,408 / 15.236 s |
| 1500 / 17 | 187,909 / 52.102 s | 0 / 0.0052 s | 0 / 0.0059 s |
| 2201 / 17 | TIMEOUT 30 s | TIMEOUT 30 s | TIMEOUT 30 s |

All completed roots reported PROVEN and zero unresolved roadblocks, subject to the outstanding proof-grade arithmetic audit.

The p=17 early-state cut at exponents 1000 and 1500 is explained by excluding the first seven roots and then applying their LP complement bound directly. At exponent 2201, that seven-prime bound is insufficient. V15's additional forced-prime dual gains did not reduce these completed root branch counts beyond the V14 cuts.

### Research direction: prime-power-conditioned reoptimization

For a forced prime \(q\), the V15 gain uses the existing Lagrange multipliers and requires only \(\sum_{a}x_{q,a}=1\). A stronger candidate is to solve a **separate primal-dual LP under \(x_{q,a}=1\)** for selected exponent options. Its new dual can exploit required divisor-sum factors and special-prime slot restrictions before the full recursive factor chain explores that option.

Candidates should be screened numerically before generating interval-dual certificates. The experimental obligation is to show a branch-count reduction **at exponent 2300**, with the prime-power options partitioning all admissible exponents.

## V16: interval-safe forced-prime gain

The first V15 implementation computed
\[
\min_i \ell_i-\sum_i\min(0,\ell_i),
\]
where \([\ell_i,u_i]\) encloses each reduced cost. This can overestimate the gain because the baseline penalty needs an **upper** bound before it is subtracted. V15 is retained as a historical prototype; its forced-gain table is not proof-grade.

V16 uses the valid conservative lower bound
\[
G_q\;\ge\;\min_i\ell_i-\sum_i\min(0,u_i).
\]
The minimum forced option cost is bounded below by the smallest interval lower endpoint. The old box-relaxation penalty is bounded above by the sum of the negative interval upper endpoints. Their difference is therefore a certified lower bound for the improvement from imposing \(\sum_i x_{q,i}=1\).

The generator implements this with outward-rounded endpoint arithmetic in `Sources/Python/DualGainBounds.py`; `CertificateTests.py` checks endpoint combinations. V16 also rounds each accumulated gain downward in C++.

## V17 Euler-slot-coupled forced-prime dual gain

For all currently unbranched forced primes \(Q\), let \(I_q^o\) and \(I_q^s\) denote ordinary- and special-exponent LP options. If the individual reduced costs satisfy \(r_i\in[\ell_i,u_i]\), define

\[
o_q=\min_{i\in I_q^o}\ell_i,\quad
s_q=\min_{i\in I_q^s}\ell_i,\quad
B=\sum_{q\in Q}\sum_{i\in I_q}\min(0,u_i).
\]

If the Euler-special prime is not already assigned, any completion using the forced primes has total selected reduced cost at least

\[
C=\sum_{q\in Q}o_q-\max\{0,\max_{q\in Q}(o_q-s_q)\}.
\]

The inner maximum ranges only over primes with at least one special option. If a previously fixed component has already consumed the special slot, set \(C=\sum_qo_q\).

Therefore the certified additional cut over the original box-relaxation dual penalty is

\[
\boxed{G_{17}=\max(0,C-B),}
\]

with **every intermediate sum and difference directed outwards**. The formula uses the special slot jointly; it replaces the independent V16 forced gains for those same groups, avoiding double counting. The code skips forced primes without explicit LP option groups (a safe relaxation).

The main remaining audit obligations concern the LP model's completeness, interval coefficient recomputation and full-tree correctness; source-level unit tests alone are insufficient to establish a new unconditional bound.

## V17 matched benchmark outcome

[GitHub Actions 45001125412](https://github.com/stormwhip/PerfectNumbers/actions/runs/45001125412) passed all compile and regression tests and finished the diagnostic workflow.

| Target/root | V16 branches/status | V17 branches/status |
| --- | --- | --- |
| 1000 / 31 | PROVEN, 21,408 branches | PROVEN, 21,408 branches |
| 1500 / 17 | PROVEN, 0 branches | PROVEN, 0 branches |
| 2201 / 17 | TIMEOUT after 30 s | TIMEOUT after 30 s |
| 2300 / 17 | TIMEOUT after 30 s | TIMEOUT after 30 s |

At exponent 2300, 20-second progress was 294,456 visited branches / 566 LP cuts for V16, versus 268,547 visited branches / 315 cuts for V17. These partial traces do not demonstrate a wall-time improvement. Future testing should compare completed root cases with larger forced-prime groups, use exact per-subtree visit counters and consider LP reoptimization after fixing a prime-power option, rather than relying only on coupling existing dual reduced costs.
