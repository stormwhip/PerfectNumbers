# 奇完全数 \(10^{2400}\) 下界项目进展报告

**日期：2026 年 11 月 22 日 · 项目：PerfectNumbers · 主目标：无条件证明每个奇完全数 \(N>10^{2400}\)**

> 当前状态：已有超过 \(10^{2400}\) 的**指定八素数互素条件 LP 数值下界**，尚无完整的八根因子链证明。所有新下界均须通过模型、数值和计算证书的独立核验后才能作为数学定理。精简前仓库原始快照：[124ab214](https://github.com/stormwhip/PerfectNumbers/tree/124ab21449d4afd9d017a32faa9bd27253943c70)。

## 1. 研究问题、目标与摘要

奇完全数（odd perfect number, OPN）是假设存在的奇整数 \(N\)，满足正因子和 \(\sigma(N)=2N\)。其存在性仍是开放问题。本项目只研究一个明确目标：排除所有满足 \(N\le10^{2400}\) 的奇完全数，生成可由第三方核验的证明树与线性规划（LP）证书。

Euler 的结构定理给出 \(N=\pi^{4a+1}m^2\)，其中 \(\pi\equiv1\pmod4\)，且 \(\gcd(\pi,m)=1\)。因子链搜索利用
\[
p^e\parallel N\quad\Longrightarrow\quad \sigma(p^e)\mid 2N
\]
传播必须出现的素因子，并在过丰度、大小超界、禁用素数出现或指数条件冲突时关闭分支。

采用以下八素数集合：
\[
S_8=\{3,5,7,11,13,17,19,31\}.
\]
完整证明拆为两个逻辑上互补的部分：（A）依次排除每个至少含有一个 \(S_8\) 中素数的候选；（B）给出 \(\gcd(N,\prod_{p\in S_8}p)=1\) 时的严格下界。当前 B 已产生数值输出，A 尚未完成。

## 2. 前人的工作与文献状态

| 年份 | 作者 | 已有研究结论 | 本项目直接用途 |
| --- | --- | --- | --- |
| 1991 | Brent、Cohen、te Riele | 证明 \(N>10^{300}\)，采用大型因子链证明树与整数分解 | 计算证明树的先导方法 [1] |
| 2007 | Nielsen | 任意奇完全数至少有 9 个不同素因子 | 附加结构条件 [3] |
| 2012 | Ochem、Rao | 在 *Mathematics of Computation* 正式发表 \(N>10^{1500}\)，同时给出 \(\Omega(N)\ge101\) 及最大素数幂组件 \(>10^{62}\) | 直接基准与技术路线 [2] |
| 2012 | Nielsen 等 | 因子链筛法与奇完全数结构限制 | 潜在附加剪枝 [4] |
| 2015 | Nielsen | \(\omega(N)\ge10\) | 后续 LP/因子数量约束的候选 [5] |
| 截至本报告日期 | Ochem 官方项目页 | 报告后续计算下界 \(N>10^{2200}\)，并提供 t2300 合数列表、roadblock 和 checkfacts 因子数据库 | 当前公开计算基准及大规模输入 [6] |
| 2026 | Ochem、Zelinsky | 针对“恰有一个偶指数大于 2”的特殊 OPN 类给出强限制 | 专题旁证，不直接推出一般下界 [7] |

**文献地位区分：** \(10^{1500}\) 有正式发表的原始论文；\(10^{2200}\) 是 Ochem 官方网页公布的后续计算进展；本项目的 \(10^{2400}\) 条件 LP 输出为尚待完全审计的程序结果。任何一层均不代替后一层的独立证明责任。

## 3. 已完成工作与实验证据

### 3.1 原始因子链、工程与根集合优化

建立了 C++17 / GMP 因子链求解器和因子索引构建器，使用输入压缩包的固定 SHA-256：

ff1e84b119949ffcce57b29616d57ed5d03793ad3e4f74f1b203ad0e809f4119

历史 V4 记录：指数 1000 对应 749,961 个分支、51.59 秒；指数 1500 对应 33,137,706 个分支、1054.08 秒。这些是旧环境的历史实验，并非当前新版本的证明级认证。

V1–V17 的主要研究包括 OpenMP 任务调度、因子与合数残余处理、路障（roadblock）、\(p\)-进估值传播、最优根顺序、状态级 LP 对偶剪枝和欧拉特殊素数名额耦合。部分改进在低指数有效，另一些在完整算例上未表现出加速，均保留在 [ExperimentLog](../Records/ExperimentLog.md)。

对八根的所有 \(8\cdot2^7=1024\) 条有向子集状态转移，在指数 500 下已进行穷尽成本测量；按分支数优化的顺序为
\[
19,\ 7,\ 11,\ 31,\ 13,\ 3,\ 5,\ 17,
\]
对应 40,733 分支。[8] 这与目前求解器的顺序一致，尚无针对指数 2400 的顺序最优性证明。

V14–V16 将固定对偶 LP 检查前移到 DFS 中间状态，在指数 1500 的最后根 17 上将 187,909 个原有搜索分支化为一次 LP 剪枝。[9] 指数 2201 / 2300 的困难根在短时限测试中仍超时。V15 曾存在强制素数增益的区间端点方向错误，V16 修正为保守区间下界。V17 的特殊素数联合剪枝完成测试，但在可终止的对照算例中无新增分支减少，因此精简后主线保留 V16。[10]

### 3.2 本项目目前最重要的结果：八素数终局 LP 跨过 2400

在线性规划中表示可行素数幂、丰度、Euler 特殊素数唯一性、因子和蕴含关系和无限尾部的保守松弛。对于 \(\gcd(N,\prod_{p\in S_8}p)=1\)，比较两种模型：

| LP 版本 | 区间对偶程序输出的 \(\log_{10}N\) 下界 | 相对目标 2400 |
| --- | ---: | ---: |
| 初始八素数模型 | 2390.111014293284 | -9.888986 |
| 补入 61 的高指数因子和约束 | **2400.822998027028** | **+0.822998** |

两条关键的新约束来自精确分解：
\[
\sigma(61^{10})=199\cdot859\cdot4242586390571,
\]
\[
\sigma(61^{12})=187123\cdot14421466756460791.
\]

程序 [Prime61FactorChecks.py](../Sources/Python/Prime61FactorChecks.py) 已对这些等式、多个 \(61^e\) 的因子和等式以及所列素因子的素性进行独立检查；[运行 45001172416](https://github.com/stormwhip/PerfectNumbers/actions/runs/45001172416) 通过。

61 的额外条件化 LP 数值结果（均额外假定与 \(S_8\) 互素）：

| 61 的指数条件 | 区间对偶程序下界指数 |
| --- | ---: |
| \(61^6\parallel N\) | 2425.846325041447 |
| \(61^{10}\parallel N\) | 2465.876803180284 |
| \(61^{12}\parallel N\) | 2511.641527478704 |
| \(\nu_{61}(N)\ge16\)，偶指数 | 2400.822993303349 |

若 \(61\mid N\)，奇指数会强制 \(31\mid N\)；指数 \(2,4,8,14\) 可由 \(\sigma(61^e)\) 含指定禁用素因子排除，故上述四类覆盖所有剩余指数。

**最关键的进展是“未另外假定 \(61\mid N\)”的总终局 LP 输出 2400.822998。** 因而当前目标不再要求额外增加第九个根素数。需要特别核查的仍是模型安全性、区间对偶是否独立有效，以及这仅约 0.823 的余量能否在严格验算中保留。[11]

## 4. 尚未解决的核心问题与验收条件

| 优先级 | 待完成内容 | 必须达到的验收标准 |
| --- | --- | --- |
| P0 | **LP 模型数学正确性审计** | 所有普通/特殊指数选项、有限及无限尾部、每条因子和蕴含在 OPN 全部可能情形下安全 |
| P0 | **独立 LP 对偶证书** | 导出每一约束的有理/区间乘子及完整残差，用第二套验证器独立重算，并证明下界严格大于 2400 |
| P0 | **全部八个根分支完成** | 按固定顺序逐根排除，全部返回已完成且没有 unresolved roadblock；记录每条终结分支对应的严格矛盾 |
| P1 | 证明树算术正确性 | 对可能影响剪枝的浮点比较采用经过认证的舍入；明确指数分支完备性、素性、数据库分解、残余互素/重叠及 ALPHA 约束 |
| P1 | 可恢复的任务分片 | 精确记录搜索状态、每个子任务前缀、代码提交、因子数据库哈希、已处理和未处理任务；可中断恢复并去重验算 |
| P1 | \(10^{2400}\) 分支成本剖析 | 在相同硬件和数据条件下形成可终止或有固定预算的分层测试，优先定位困难根与重型 roadblock |
| P2 | 更强的条件化 LP / 分支优化 | 对完整可终止算例证明分支数和端到端耗时实际下降；保留失败实验数据 |
| P3 | 定理与公开可复核材料 | 明确问题分区、形式化推理、证书输入、源代码版本、数据库校验值、运行日志与独立审计 |

程序打印 PROVEN 只说明当前实现认为已关闭搜索分支；完全数定理需要额外通过以上审计。

## 5. 下一步实施计划

**阶段 A — 先认证增强 LP：** 建立完整约束清单，特查 \(\sigma(61^{10}),\sigma(61^{12})\) 的指数变量及高指数尾部，输出可由独立程序计算的对偶乘子与向外舍入界。把“2400.822998”提升为可检查的正式不等式。

**阶段 B — 让搜索持续可恢复：** 将当前 DFS 按精确根前缀和指数状态分片；使用持久任务清单、断点恢复、稳定状态哈希和错误退出检测。保留本地 32 线程长时间任务与 GitHub Actions 小规模测试的边界；未经手动选择，CI 只运行轻量测试。

**阶段 C — 完成 \(10^{2400}\) 八根证明：** 基于固定顺序逐根完成，每个任务归档可核验的终结证据。优先改进高成本路障和条件 LP，最后与阶段 A 的无根终局证明合并。

**时间估算：** 历史 V4 的指数 1000/1500 数据不能直接预测新搜索树在 2400 的总时间。现有 2201/2300 限时记录尚无完整高指数根结束，因此应先测实际分支成本，再决定长期运算安排。

## 6. 精简后的代码与证据入口

| 功能 | 当前正式文件 |
| --- | --- |
| 因子数据库索引 | [BuildIndex.cpp](../Sources/Cpp/BuildIndex.cpp) |
| 八根主求解器 | [ProofTreeV16.cpp](../Sources/Cpp/ProofTreeV16.cpp) |
| 求解器核心回归 | [ProofCoreTestsV16.cpp](../Sources/Cpp/ProofCoreTestsV16.cpp) |
| 增强 LP 主体 | [IntervalCertificate61.py](../Sources/Python/IntervalCertificate61.py) |
| 全部 256 个前缀对偶证书 | [PrefixDualCertificates.py](../Sources/Python/PrefixDualCertificates.py) |
| 61 条件化测试 | [ConditionalPrime61.py](../Sources/Python/ConditionalPrime61.py) |
| 整数分解核验 | [Prime61FactorChecks.py](../Sources/Python/Prime61FactorChecks.py) |
| 证明审计清单 | [ValidationChecklist.md](../Records/ValidationChecklist.md) |
| 历史完整实验 | [ExperimentLog.md](../Records/ExperimentLog.md) |

为了聚焦当前目标，旧证明树 V1–V15/V17、重复的版本化测试、过时的 benchmark、旧理论候选与临时文档已从主分支清理；均可通过 [精简前提交 124ab214](https://github.com/stormwhip/PerfectNumbers/tree/124ab21449d4afd9d017a32faa9bd27253943c70) 恢复。

## 7. 参考文献

[1] R. P. Brent, G. L. Cohen, H. J. J. te Riele, *Improved techniques for lower bounds for odd perfect numbers*, Math. Comp. 57 (1991), 857–868. [作者原始摘要与文献](https://maths-people.anu.edu.au/brent/pd/rpb116a.pdf)。

[2] P. Ochem, M. Rao, *Odd perfect numbers are greater than \(10^{1500}\)*, Math. Comp. 81 (2012), 1869–1877. [DOI](https://doi.org/10.1090/S0025-5718-2012-02563-4)；[仓库内 PDF](../References/OchemRao2012.pdf)。

[3] P. P. Nielsen, *Odd perfect numbers have at least nine distinct prime factors*, Math. Comp. 76 (2007), 2109–2126. [arXiv](https://arxiv.org/abs/math/0602485)。

[4] P. P. Nielsen 等，*Sieve methods for odd perfect numbers* (2012). [论文](https://mathdept.byu.edu/~pace/OPNSieves_web.pdf)。

[5] P. P. Nielsen, *Odd perfect numbers, Diophantine equations, and upper bounds*, Math. Comp. 84 (2015), 2549–2567. [AMS 原文](https://www.ams.org/journals/mcom/2015-84-295/S0025-5718-2015-02941-X/S0025-5718-2015-02941-X.pdf)。

[6] P. Ochem, [Odd perfect numbers — 官方项目网页](https://www.lirmm.fr/~ochem/opn/)，2026-11-22 核对。

[7] P. Ochem, J. Zelinsky, *On odd perfect numbers with exactly one even exponent greater than 2*, 2026，预印本 [arXiv:2607.19746](https://arxiv.org/abs/2607.19746)。

[8] [根顺序全部 1024 转移测试](https://github.com/stormwhip/PerfectNumbers/actions/runs/44996427816)；
[9] [V13–V15 状态剪枝测试](https://github.com/stormwhip/PerfectNumbers/actions/runs/44998508242)；
[10] [V16/V17 对照](https://github.com/stormwhip/PerfectNumbers/actions/runs/45001125412)；
[11] [61 因子分解与增强 LP 重复实验](https://github.com/stormwhip/PerfectNumbers/actions/runs/45001172416)。

---

**项目结论：** 无条件 \(N>10^{2400}\) 仍未完成。强条件 LP 下界已超过目标，当前最有价值的工作是**证明级 LP 证书 + 全部八根可恢复穷尽搜索**。