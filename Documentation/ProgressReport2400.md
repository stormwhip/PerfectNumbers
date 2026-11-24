# PerfectNumbers：\(10^{2400}\) 历史进展报告

**历史快照：2026-11-24（Gemini 批次新增 12 个分片，累计 2,027 / 3,072）**。最新进度见[当前状态](CurrentStatus2400.md)及[总证明](Proof2400.md)。 · **基线：V21** · **实验性前沿：V2 验证器/G1 C++** · **全局状态：`INCOMPLETE_FRONTIER`**。

> **当前结论：** 原八根互素类已独立验证 \(\log_{10}N\ge4183.209493\)，替换根 \(19\to23\) 的互素类已独立验证 \(\log_{10}N\ge3954.197016\)。两套集合的八个含根分支类仍需完成全量计算与独立核验。

## 2026-11-24 Euler 来源区间研究

把供给 Euler 素数的分圆指标中的根素因子约去，可以给同一个偶幂兼任来源和根赋值供给者的情形建立尺寸下界。533 个开放实际指数上的整数实验扩大了 76 个指数的覆盖，相对对照新增 4,190 个 Euler 赋值组合。根 3 的实际指数 1330 在最高四个正赋值上，内部来源可缩至 `c >= 2`、`c < f < 4c`。分支并集、分片验收和长时运行见[历史来源区间报告](https://github.com/stormwhip/PerfectNumbers/blob/ea08da38e38ab3309da4360ea2bb60ecb616a025/Documentation/ResearchReport2400.md)。

## Gemini 批次的合并复验

Gemini 批次经独立复验排除 51 个实际指数，净增 **12** 个顶层分片。累计闭合 **2,027 / 3,072** 项，尚余 **1,045** 项。[复验证明](../Research/TeichmullerValuation/GeminiBatchProof2400.md) · [批次审计](../Research/TeichmullerValuation/GeminiBatchAudit2400.json)

作为本轮基线，Teichmüller 提升赋值判据在根 19、7、11、31、13 分别关闭 24、32、42、21、27 个原有开放分片，净增 **146** 项，累计闭合 **2,015 / 3,072** 项，尚余 **1,057** 项。[推导与复验](../Research/TeichmullerValuation/Readme.md) · [逐项清单](../Research/TeichmullerValuation/Audit2400.json)

Claude 的 Euler 筛独立排除四个实际指数，相对 Teichmüller 基线关闭两个分片。四条排除均已由 Gemini 批次覆盖，合并后的闭合数仍为 2,027。[Claude 批次证书与复验](../Research/EulerOneSieve/Readme.md)

## 此前指标容量复验

精确复验新增排除 **74 个实际指数**，关闭 **18 个顶层分片**。根 3 排除 29 个实际指数、关闭 9 个分片，根 5 排除 45 个实际指数、关闭 9 个分片。累计闭合 **1,869 / 3,072**，剩余 **1,203**。 [数学推导与复验](../Research/IndicatorCapacity/Readme.md) · [完整清单](../Research/IndicatorCapacity/Audit2400.json)

## 此前批量复验

累计闭合 **1,851 / 3,072**，尚余 **1,221**。根 3、5 的来源判据排除 51 个实际指数，完整覆盖 40 个新顶层分片。扩大因子扫描提供另外 6 个分片证书。根 3 和根 5 的最大开放代表指数分别降至 1398、742。[推导](../Research/SupplierBatch/PerfectNumbers2400BatchReport.md) · [逐项审计](../Research/SupplierBatch/BatchAudit2400.json)

## 历史快照（1,805 项）

原根顺序下，已闭合 **1,805 / 3,072** 项，尚余 **1,267** 项。新方法排除了根 3 的 135 项、根 5 的 106 项。按规范分片 ID 与 1,629 项历史证书取并集，重叠 65 项，净增 176 项。根 3 还剩 230 项，根 5 还剩 158 项。 [推导和证书](../Research/FermatRootValuation/FermatRootValuationReport.md) · [合并审计代码](../Research/Session20261122/Python/AuditRootClass2400.py)

## 历史记录

### 2026-11-23 分圆有限剩余乘子新增三项证明叶

在原根集固定顺序下，利用 `sigma(p^(ell-1))=Phi_ell(p)` 的素因子同余限制，推出不依赖大整数分解的丰度上界，并逐一枚举全部奇数剩余乘子 `Q`。根 `(19,936)`、`(11,1150)`、`(11,1152)` 分别枚举 `705,908`、`28,471`、`2` 项，剩余数均为零。证明规则已接入 V2 独立验证器和正式审计快通道。现有 **1,396 个立即整数证明叶 + 3 个有限穷举证明叶**；候选累计闭合 `1,399/3,072`，另有 **1,673 项**待证明。最新 GitHub CI 和整个 3,072 项独立审计尚待执行，最终状态仍为 `INCOMPLETE_FRONTIER`。详细证明见 [FiniteQuotientCyclotomic2400.md](../Research/Session20261122/Reports/FiniteQuotientCyclotomic2400.md)。

### 独立验证框架的集成

以 [CurrentStatus2400.md](CurrentStatus2400.md) 为权威进度入口。原根集互素类证书已经独立核验，指数清单有 3,072 项；含根类仍未形成全部 `TREE_ACCEPTED` 的证明 DAG。原根与替换根集不能混用。

- 新增 [IndependentVerifierV2.py](../Research/Session20261122/Python/IndependentVerifierV2.py)，严格要求外部固定根、逐边重建、完整素性见证及可验证剪枝；配套合成、篡改、路障、LP 规则回归。
- 新增 [FrontierLedgerV2.py](../Research/Session20261122/Python/FrontierLedgerV2.py)、[AuditRunner2400.py](../Research/Session20261122/Python/AuditRunner2400.py) 和 [FrontierWorkerDriver.py](../Research/Session20261122/Python/FrontierWorkerDriver.py)，具备可恢复前沿、只读审计与部分 Worker 桥接。
- 新增 [ProofTreeV21Frontier.cpp](../Sources/Cpp/ProofTreeV21Frontier.cpp)、[V21FrontierCodec.hpp](../Sources/Cpp/V21FrontierCodec.hpp)、[SingleFlightFactCache.hpp](../Sources/Cpp/SingleFlightFactCache.hpp)。仍缺真实 C++ → Python 证明 DAG 桥接、全部 V21 路障/LP 语义、大素数证书、单飞缓存接入。
- 新的模块已有先前小规模测试记录，目录变更后的自动化回归仍需重新执行；完整 3,072 项和 72 小时目标均未验收。
- 完整说明：[IndependentProofIntegration2400.md](../Research/Session20261122/Reports/IndependentProofIntegration2400.md)。

以下 V21 / V22–V24 章节保留阶段实验事实，历史状态描述以本节为准。

**数学问题与验收条件详见 [ResearchProblems2400.md](ResearchProblems2400.md)。** 本文汇总对应的实际代码与实验事实。先前 V16 阶段的长篇原始报告可在 [2026-11-22 整理前快照](https://github.com/stormwhip/PerfectNumbers/blob/90100f4447f9196835951fdb7e9dcdd3ab23723f/Documentation/ProgressReport2400.md) 阅读。

## 1. 数学问题的九个互斥类

令 \(\mathcal O=\{N:\ N\text{ 为奇数},\ \sigma(N)=2N\}\)，\(S_8=\{3,5,7,11,13,17,19,31\}\)，采用外层根顺序

$$
(q_1,\ldots,q_8)=(19,7,11,31,13,3,5,17).
$$

假设 \(N\in\mathcal O\)、\(N\le10^{2400}\)。令 \(\mathcal C_i\) 表示 \(q_i\mid N\) 且所有前面的 \(q_j\nmid N\)，另令 \(\mathcal C_\infty\) 表示 \(N\) 与 \(S_8\) 每个素数都互素。要证明上述九类全空。当前数值证书仅针对 \(\mathcal C_\infty\)；另外八类由证明树负责。

## 2. 已建立的正式工程

| 环节 | 现有文件 | 实际状态 |
| --- | --- | --- |
| C++17/GMP/OpenMP 因子链 | [ProofTreeV21.cpp](../Sources/Cpp/ProofTreeV21.cpp) | 可搜索指数 2400；尚无完整证明树 |
| 256 个前缀 LP | [PrefixDualCertificates.py](../Sources/Python/PrefixDualCertificates.py) | [生成工作流 45004245214](https://github.com/stormwhip/PerfectNumbers/actions/runs/45004245214) 成功，输出 256 份表 |
| 强化 61 的因子和约束 | [IntervalCertificate61.py](../Sources/Python/IntervalCertificate61.py) | [核验 45001172416](https://github.com/stormwhip/PerfectNumbers/actions/runs/45001172416) 成功 |
| 大因子残余的安全上界 | [PrimeCutoffCert.cpp](../Sources/Cpp/PrimeCutoffCert.cpp) | 构建 \(10^8\) 素数截止乘积和确定性哈希 |
| 输入因子数据库 | [BuildIndex.cpp](../Sources/Cpp/BuildIndex.cpp) | 已建立固定版本及 SHA-256 校验 |
| 可恢复任务调度 | [Run2400Scheduler.py](../Sources/Python/Run2400Scheduler.py) | 顶层指数分片与已完成任务恢复；深层状态仍无法恢复 |
| 主线单元测试 | [ProofCoreTestsV21.cpp](../Sources/Cpp/ProofCoreTestsV21.cpp) | [CI 45007403402](https://github.com/stormwhip/PerfectNumbers/actions/runs/45007403402) 通过 |

数据库 `checkfacts.txt.gz` 的已固定 SHA-256 为

```text
ff1e84b119949ffcce57b29616d57ed5d03793ad3e4f74f1b203ad0e809f4119
```

## 3. 互素类 LP 计算

给定 \(\gcd(N,\prod_{p\in S_8}p)=1\)，增强 LP 考虑各素数指数、丰度要求 \(\sigma(N)/N=2\)、Euler 特殊素数数量、已分解的 \(\sigma(p^a)\) 强制因子及有限域外的乐观无限尾部。

终局数值输出为

$$
\log_{10}N\ge2400.822998027028
\qquad\text{（条件 LP 的区间对偶程序输出）}.
$$

这是早期程序输出。后续终局模型将诱导素数显式化，并以整数和递归素性见证独立重验对偶。原集合和替换集合的互素类均已排除目标区间中的候选。[证书、推导及复现命令](../Research/Session20261122/Reports/CertifiedTerminalAndBoundaryProfile.md)

## 4. V21：困难根的实证

[根 19 完整顶层指数清点 45005912683](https://github.com/stormwhip/PerfectNumbers/actions/runs/45005912683)：

- **287** 个指数任务；
- **164** 个在每分片 1 秒限时内返回 `PROVEN`；
- **123** 个在该限时下 `TIMEOUT`。

对这 123 项 [调整根 19 的全局位置](https://github.com/stormwhip/PerfectNumbers/actions/runs/45006916458) 时，有 73 项能在相应的 1 秒预算内完成，仍有 50 项超时。此对照改变前缀禁用条件，不能单独作为新顺序对全部八根的总体加速证据。

[八根顺序动态规划 45007403299](https://github.com/stormwhip/PerfectNumbers/actions/runs/45007403299) 对代理指标进行了全子集优化：其代理成本降幅约 0.03%–2.64%，尚无完整八根墙钟耗时的证明。短时测试中，根 19、17、31 仍不能在 30 秒内穷尽。

**72 小时目标未经过完整实测验证。** 路障乘子参考实现已在固定精度下精确找出最小可认证分界，完成 224,456 个小规模格点对照。它仍需接入真实节点的回放，以校准低成本候选乘子和复核 C++ 路障路径。[推导与复现](../Research/Session20261122/Reports/RoadblockMultiplierSearch.md)

## 4.1 原生路障对照与分支覆盖审计

- C++ 整数判界已在 Linux 实验分支跑过真实节点。会触发路障的根 19 分片 66、132、138、149 均完成三方对照，证书模式四项耗时均增加。困难分片 0、100 在 45 秒内两种模式都超时，且尚未进入路障。
- 主线已修复循环分支预算对已计入合数残余的素因子重复计价的问题。独立验证确认了实际根 19 清单的 287 项，原根集和替换根集的参考清单分别为 3,072 和 3,058 项。
- [实验数据、修复依据和覆盖核验](../Research/Session20261122/Reports/NativeRoadblockPilot.md)

## 5. 2026-11-22 性能研究 V22–V24

所有新原型均保存在 [Research/Session20261122/](../Research/Session20261122/Readme.md)，不改变正式 V21 调度脚本。

| 版本 | 数学/工程改动 | 实验结论 |
| --- | --- | --- |
| V22 | 基于 \(\operatorname{odd}(\sigma(p^a))\mid N\) 的精确整除及乘积 LCM 剪枝 | 数学规则明确且通过回归，已完成分片中增加运行耗时 |
| V23 | 对同一个 \(\sigma\) 残余复用第一次 GMP 素性测试，残余改变时重检 | 已完成的根 19 分片 35 与 130，分别降低约 30.1% 与 24.9% 的耗时 |
| V24 | 将合数残余逐项互素测试改为乘积 GCD | 4000 组随机差分验证一致；实际运行表现不稳定 |

主要证据：[V22 首轮](https://github.com/stormwhip/PerfectNumbers/actions/runs/45011182741)、[V22 延迟剪枝](https://github.com/stormwhip/PerfectNumbers/actions/runs/45011614919)、[V21 性能剖析](https://github.com/stormwhip/PerfectNumbers/actions/runs/45012070442)、[V23 对照](https://github.com/stormwhip/PerfectNumbers/actions/runs/45012354324)、[V24 对照](https://github.com/stormwhip/PerfectNumbers/actions/runs/45012698021)。

V21 剖析表明素性测试是困难分片 0、100 的主要计时热点。V23 在两项完整结束的分片中实现了有效加速。V22 与 V24 目前均不满足替换正式主线的性能证据标准。

## 6. 早期工程路线

现行工作顺序见[下一步计划](NextPlan2400.md)。以下保留原工程计划。

1. **P0 — 替换根集的前缀和搜索对照：** 为 \(19\to23\) 的候选集合生成前缀对偶，比较两套完整分区的负载与正确性。
2. **P0 — 较早层次的困难树剪枝：** 构造考虑已选指数、强制素数和 Euler 名额的条件化 LP，优先在大量素性测试以前关闭子树，必须以已完成分片墙钟耗时验收。
3. **P0 — 八根穷尽性与 roadblock：** 证明指数选项覆盖、无穷尾尺寸和丰度约束安全，完成所有顶层及必要深层任务。
4. **P1 — 独立算术与证明树验证：** 对数据库素性、分解、浮点边界和每条闭合规则导出独立证书，生成可重验的证明 DAG。
5. **P1 — 深层断点与 72 小时评估：** 在固定代码和数据版本下，进一步切分长尾任务，完成全树工作量测量，再验收实际 72 小时运行。

## 7. 证据与研究入口

- [形式化数学研究难题](ResearchProblems2400.md)
- [当前验收清单](../Records/ValidationChecklist.md)
- [研究实验归档](../Research/Session20261122/Readme.md)
- [历史实验日志](../Records/ExperimentLog.md)
- [Ochem–Rao (2012) 原始论文](../References/OchemRao2012.pdf)

**结论：** 当前研究瓶颈集中在**可独立认证的数学剪枝**与**所有困难根的可终止证明树**；V23 已降低局部计算成本，仍需通过全树证书和可靠的端到端运行把数值研究推进为无条件定理。
