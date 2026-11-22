# Exact lattice search for roadblock multipliers

> **进度标注（2026-11-22）**：本文记录对应阶段的数学推导、实验数据和当时的搜索状态。最新研究进度、独立验证器 V2、可恢复前沿及全量未闭合项目，统一见 [CurrentStatus2400.md](../../../Documentation/CurrentStatus2400.md)。本文历史计时和程序 `PROVEN` 均不作为 `10^2400` 完整证明。


This experiment implements Gemini's concavity-based multiplier search as a reference for the C++ integration. It determines the smallest integer boundary that can be certified at a specified dyadic precision. The experiment keeps the existing Python fixed-point scale of \(2^{80}\) and uses arbitrary-precision integers.

## Derivation and corrections

Write \(\ell_q\) for the integer lower endpoint of the scaled \(\log q\), \(h_q\) for the integer upper endpoint of the scaled abundance, and \(\Delta\) for the scaled abundance gap lower endpoint. At boundary \(b\), an ordinary prime contributes \(f_q(\mu)=\min(0,e_q\ell_q-\mu h_q)\). The objective before rounding is the minimum of the following functions.

- Use no special prime: \(F_0(\mu)=\mu\Delta+\sum_q f_q(\mu)\).
- Use an eligible finite special prime \(s\): \(F_s(\mu)=\mu\Delta+\ell_s-\mu h_s+\sum_{q\ne s}f_q(\mu)\).
- Use the generic special tail: \(F_{\rm tail}(\mu)=F_0(\mu)+\ell_{\rm tail}-\mu h_{\rm tail}\).

Remove both kinds of special alternatives when the Euler slot is already used. A common multiplier cap \(\mu_{\rm cap}=2\ell_{\rm tail}/h_{\rm tail}\) keeps the ordinary generic tail reduced cost nonnegative.

Each alternative is a sum of affine functions and minima of affine functions. Their pointwise minimum is concave and piecewise linear. Choose any active alternative and, for every \(f_q\) at equality, pick the zero branch. The resulting active affine line majorizes the objective globally. Its slope is an exact supergradient, including at a tie or fold. The generic special tail subtracts \(h_{\rm tail}\) from the slope whenever its gain is the active choice. A finite winning special prime subtracts its abundance only if its ordinary option was not included in the negative prefix.

The integer search uses \(\mu=j/D\), with \(D=2^{32}\) by default. Evaluate the unrounded numerator \(D L_b(j/D)\) and its exact slope. A positive slope excludes every strictly smaller \(j\) from improving on the current value. A negative slope excludes every strictly larger \(j\). A zero slope supplies a global maximum. The current point remains a candidate at each step. This proves exact maximization over the selected lattice. When the scaled integer budget is \(M\), a successful numerator must reach at least \((M+1)D\). Since the bound is at most \(j\Delta\), start at \(j_{\min}=\lceil(M+1)D/\Delta\rceil\) and end at \(j_{\max}=\lfloor D\mu_{\rm cap}\rfloor\).

The fixed-multiplier objective cannot decrease with \(b\) because raising the boundary removes candidates and can only increase an ordinary option's cost or remove a special alternative. Maximization over the same lattice preserves monotonicity. The outer binary search therefore returns the smallest integer \(b\in[3,P]\) with a witness on that lattice. Each fixed-boundary build uses the existing factor table. Each multiplier evaluation uses prefix sums and two crossing searches per exponent class. A negative size budget is handled separately by the caller. Absence of a lattice witness leaves the node unresolved under this rule.

The analysis uses concavity, without requiring strict concavity. A bounded heuristic search over a subset of multipliers can provide a valid witness whenever it succeeds. Its failure does not exclude a witness on the full lattice. The exact search is an offline reference and need not run at every production node.

## Reproduction

~~~bash
python -S Research/Session20261122/Python/RoadblockMultiplierSearchTests.py
~~~

The test compared 224,456 exact lattice points in 80 randomized states with the prior independent evaluator. Every fixed-boundary maximum was checked by exhaustive enumeration of the small test lattice, and the first passing boundary was checked for strict equality cases. Successful witnesses were also replayed by the fixed-multiplier event sweep.

For the existing synthetic node at \(P=300000\), scaled budget \(55\cdot2^{80}\) first passes at \(b=3\) with unscaled bound \(55.8167100711\). The absence of admissible candidates below 29 makes \(b=3\) and \(b=29\) equivalent in this example. Budget \(56\cdot2^{80}\) first passes at \(b=30\) with bound \(71.1775079036\). A reference run took about 2.8 and 1.2 seconds respectively after the shared prime table was built. Those timings include fresh per-boundary stream construction and show why this exact implementation is a diagnostic oracle.

## Next proof and performance checks

1. Use the oracle on real traced V21 roadblocks, especially in root-19 shards 0 and 100. Compare a small online multiplier portfolio with the exact minimum boundary and measure the effect on completed shards. The proof obligation is strict rechecking of each returned witness and safe handling of unresolved nodes.
2. Give both root sets equivalent prefix tables and compare whole partitions. With \(19\) before \(7\), \(\sigma(7^2)=3\cdot19\) supplies a cutoff. The replacement allows a different cutoff: with \(7\) before \(23\), \(\sigma(23^2)=7\cdot79\) excludes that branch when valid under its exponent condition. That relation alone gives no comparison of tree sizes.
3. For a fixed set of measured tasks and a fixed hardware configuration, the sum of completed runtimes and timeout cutoffs is a lower bound on total task runtime, assuming each value measures the same run configuration and includes the same phases. A timeout cutoff is also a task-level lower bound. Without an upper bound on each censored runtime, short tests alone give no finite guaranteed total or longest-task upper bound. Budget the 72-hour run using completed long-tail measurements, explicit timeout handling, and the configured concurrency.
4. For a selected root set, complete and independently verify all eight divisibility classes. The certified coprime class already closes the ninth class. State LP changes remain experimental and must preserve expanded-prime implications and disjoint residual accounting.
