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
- Matched benchmark: [ForcedPrimeLpBenchmark.yml](../.github/workflows/ForcedPrimeLpBenchmark.yml).

Full result details belong in [ExperimentLog](../Records/ExperimentLog.md).
