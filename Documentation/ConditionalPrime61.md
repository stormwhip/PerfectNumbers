> **最新研究结论（2026-11-22）**：补充精确的 sigma(61^10)、sigma(61^12) 因子蕴含后，对与八素数 S8 全部互素、**未附加 61|N 条件**的 LP 模型，已得到 2400.822998027028 的区间对偶计算下界。输入整数分解已单独核验。详见 [证明里程碑](../Records/Milestones.md) 和 [实验记录](https://github.com/stormwhip/PerfectNumbers/actions/runs/45001172416)。

> **当前状态**：原根集互素类已有独立整数证书；包含根素数的 3,072 个顶层分片仍未形成完整独立验收。本文为专项理论与历史实验说明，最新全量状态见 [CurrentStatus2400.md](CurrentStatus2400.md)。


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

## Numerical results and new eight-prime conclusion

Run [45001172416](https://github.com/stormwhip/PerfectNumbers/actions/runs/45001172416) independently verifies the exact integer products and primality of the six stated `sigma(61^a)` factorizations. The LP script additionally includes factorization implications for exponents 10 and 12, formerly excluded by the global `p^a<10^14` factorization heuristic.

| Conditional model | Interval dual exponent lower bound |
| --- | ---: |
| **No 61 hypothesis**, only all S8 primes excluded | **2400.822998027028** |
| 61 exactly to exponent 6 | 2425.846325041447 |
| 61 exactly to exponent 10 | 2465.876803180284 |
| 61 exactly to exponent 12 | 2511.641527478704 |
| 61 exponent >=16 (even) | 2400.822993303349 |
| 61 exponent >=10 (even) | 2400.822993303349 |

The unconditional-on-61 *complementary LP* result is stronger than the previously known `2390.111014` eight-prime bound; the original extra root 61 is thus **not necessary for the terminal LP at exponent 2400**, pending independent proof audit. The containing-prime factor-chain trees for all eight members of S8 are still incomplete.
