# PerfectNumbers 仓库导览与文件归属

**整理日期：2026-11-22。** 当前主线为 V21；研究 V22–V24 归档存放于 `Research/2026-11-22/`。本次整理保持正式求解器及现有 GitHub Actions 工作流的原始路径，避免破坏可复现调用。

## 1. 项目入口

| 文件 | 用途 | 维护状态 |
| --- | --- | --- |
| [Readme.md](../Readme.md) | 目标、当前结论、复现入口 | 当前 |
| [ResearchProblems2400.md](ResearchProblems2400.md) | **数学上严格定义待解决问题与证明条件** | 当前研究纲领 |
| [ProgressReport2400.md](ProgressReport2400.md) | 当前已实现和实测结果 | 当前 |
| [ValidationChecklist.md](../Records/ValidationChecklist.md) | 证明发布前验收条件 | 当前 |
| [Milestones.md](../Records/Milestones.md) | 阶段里程碑与证据链接 | 当前 |
| [ExperimentLog.md](../Records/ExperimentLog.md) | 全部历史实验，保留未经精简的原始记录 | 历史日志 |

旧版 V16 阶段进展和里程碑可通过 [原主分支快照](https://github.com/stormwhip/PerfectNumbers/tree/90100f4447f9196835951fdb7e9dcdd3ab23723f) 核对。

## 2. 生产主线：Sources/Cpp

| 文件 | 说明 |
| --- | --- |
| [ProofTreeV21.cpp](../Sources/Cpp/ProofTreeV21.cpp) | 当前正式的八根搜索树与状态剪枝 |
| [ProofCoreTestsV21.cpp](../Sources/Cpp/ProofCoreTestsV21.cpp) | 主要的数值/指数覆盖回归测试 |
| [BuildIndex.cpp](../Sources/Cpp/BuildIndex.cpp) | 压缩因子表转固定内存映射索引 |
| [PrimeCutoffCert.cpp](../Sources/Cpp/PrimeCutoffCert.cpp) | 构造经校验的有限素数乘积 |

V16、V18、V19、V20 的 `ProofTree*.cpp` 和 `ProofCoreTests*.cpp` 保留以复现历次算法差异，不再作为最新计算入口。

## 3. LP、证明脚本与调度：Sources/Python / Scripts

| 文件 | 说明 |
| --- | --- |
| [IntervalCertificate61.py](../Sources/Python/IntervalCertificate61.py) | 含特殊素数、无限尾和 sigma(61) 约束的增强 LP |
| [PrefixDualCertificates.py](../Sources/Python/PrefixDualCertificates.py) | 256 个前缀对偶/增益表 |
| [Targeted2400Certificates.py](../Sources/Python/Targeted2400Certificates.py) | 精简前缀证书生成与对照 |
| [ConditionalPrime61.py](../Sources/Python/ConditionalPrime61.py) | 61 指数条件化实验 |
| [Prime61FactorChecks.py](../Sources/Python/Prime61FactorChecks.py) | sigma(61) 等式与素性核验 |
| [DualGainBounds.py](../Sources/Python/DualGainBounds.py) | 区间安全的强制素数增益 |
| [RootExclusionDP2400.py](../Sources/Python/RootExclusionDP2400.py) | 八根顺序的组合代理成本分析 |
| [Run2400Scheduler.py](../Sources/Python/Run2400Scheduler.py) | 顶层指数任务清单、运行状态与输入哈希 |
| [Run2400SchedulerTests.py](../Sources/Python/Run2400SchedulerTests.py) | 调度器回归测试 |
| [CertificateTests.py](../Sources/Python/CertificateTests.py) | 证书相关单元测试 |
| [Run72hWSL.sh](../Scripts/Run72hWSL.sh) | 手动准备、运行及校验入口 |

`Legacy15PrefixProbe.py` 是历史 15 根比较脚本，保留供复现实验。

## 4. 实验原型：Research/2026-11-22

研究目录中包含 V21 函数级剖析器、V22 精确整除剪枝、V23 缓存残余素性结果、V24 乘积 GCD，以及它们的测试代码和实验报告。

- [研究目录索引](../Research/2026-11-22/README.md)。
- [V22 数学与负向耗时实验](../Research/2026-11-22/Reports/ExactSigmaDivisibilityV22.md)。
- [V23 正向性能实验](../Research/2026-11-22/Reports/V23PrimalityPerformance.md)。
- [V24 等价性/混合收益实验](../Research/2026-11-22/Reports/V24CompositePerformance.md)。

保留原始 [research/exact-sigma-size-v22](https://github.com/stormwhip/PerfectNumbers/tree/research/exact-sigma-size-v22) 分支及该分支上的 GitHub Actions 工作流，便于重现当时的运行环境。主线尚未合并 V23 的运行时优化；V23 对数学证明的完整审计仍待完成。

## 5. .github/workflows 分类

**质量与数学证书：** `QualityChecks.yml`、`Full2400PrefixCertificates.yml`、`Conditional61Lp.yml`。

**当前证明树与剩余算术测试：** `FactorChain2400.yml`、`CertifiedCutoff2400Benchmark.yml`、`Residual2400Benchmark.yml`、`PrimeCutoffPilot.yml`。

**诊断及历史方案比较：** `Shard2400Census.yml`、`Root19HardShardOrdering.yml`、`RootOrder2400Pilot.yml`、`RootExclusionDP2400.yml`、`Legacy15PrefixPilot.yml`。

V22–V24 和 V21 profiler 的短时实验工作流仍位于上述研究分支。这些历史任务与当前正式的 72 小时程序相互独立。

## 6. 数学资料、历史证据与生成物

- [OchemRao2012.pdf](../References/OchemRao2012.pdf)：前人原始论文。
- [ForcedPrimeDualCuts.md](ForcedPrimeDualCuts.md)：V14–V17 状态 LP 推导与旧实验。
- [ConditionalPrime61.md](ConditionalPrime61.md)：61 的条件化 LP 问题。
- `Records/ExperimentLog.md`：带工作流编号的正反实验。
- `Build/`、`Run2400Results/`、原始大型数据及编译输出：本地或 GitHub Actions 工件，不纳入小型源代码目录；按 `Scripts/Run72hWSL.sh` 中的 SHA-256 和固定输入生成。

## 7. 维护原则

1. **一个生产入口：** 证明树以 V21 为准。新的优化先进入研究分支，完成独立回归与完整分片耗时对照后再集成。
2. **完整证据链：** 数学论证、代码版本、数据 SHA-256、运行参数、终结证书及独立校验结果逐项关联。
3. **历史可追溯：** 保留已有实验和原始 Git 快照；更新当前状态时不把未经证明的数值标记为无条件定理。
4. **无需付费 API：** 本项目使用本地 C++、GMP、Python 与 GitHub Actions，长期计算应由明确的 `run` 动作启动。