# PerfectNumbers

**目标：** 证明所有奇完全数 \(N\) 满足 \(N>10^{2400}\)，并输出能够由独立程序检查的有限证明证书。

**截至 2026-11-22：无条件证明尚未完成。** 原根集互素类已有独立整数证书记录支持 `log10 N >= 4183.209493`。最新的数学直接排除规则能为 **1,396/3,072 个顶层指数任务（45.44%）** 生成一步整数证明叶，其余 **1,676 项**需继续完成证明树并独立审计。实现已提交，GitHub 新回归/完整 3,072 项审计仍待执行；最终定理状态仍为 `INCOMPLETE_FRONTIER`。早期 `2400.822998027028` 是上一阶段 LP 生成器的数值输出。

## 从这里开始

- **[仓库命名、链接与证明模块的手动回归](.github/workflows/RepositoryIntegrity.yml)**：通过 `workflow_dispatch` 手动运行轻量质量检查，不会自动启动长时证明树或付费模型。

- **[最新证明状态与剩余任务](Documentation/CurrentStatus2400.md)**：当前唯一状态摘要、证明闭环、运行验收及目录迁移说明。
- **[新增顶层直接整数证明与 1,396 项清单](Research/Session20261122/Reports/DirectRootClosure2400.md)**：因子和禁止根矛盾、`odd(σ)` 整数尺寸界、独立验收与根顺序动态规划。

- **[主要数学研究难题（形式化陈述）](Documentation/ResearchProblems2400.md)**：九类候选分割、对偶证书、证明树覆盖、roadblock、状态 LP、算术正确性与 72 小时目标。
- **[当前进展报告](Documentation/ProgressReport2400.md)**：V21 阶段、实际实验、未解决的验收事项。
- **[仓库文件导览](Documentation/RepositoryMap.md)**：正式代码、研究原型、工作流与历史记录的分层说明。
- **[证明验收清单](Records/ValidationChecklist.md)**：数学与工程独立验收条件。
- **[研究实验归档](Research/Session20261122/Readme.md)**：V22–V24、性能剖析及相应的 CI 实证。

## 正式实现与当前状态

| 模块 | 入口 | 状态 |
| --- | --- | --- |
| 证明树主程序 | [ProofTreeV21.cpp](Sources/Cpp/ProofTreeV21.cpp) | 正式主线；未形成全部八根证明 |
| 因子和数据库 | [BuildIndex.cpp](Sources/Cpp/BuildIndex.cpp) | 固定数据集、索引与哈希核对 |
| 有限素数乘积 | [PrimeCutoffCert.cpp](Sources/Cpp/PrimeCutoffCert.cpp) | 截断相关残余约束 |
| 区间 LP | [IntervalCertificate61.py](Sources/Python/IntervalCertificate61.py) | 互素类数值证书生成 |
| 256 前缀证书 | [PrefixDualCertificates.py](Sources/Python/PrefixDualCertificates.py) | 生成全部 \(2^8\) 种前缀的对偶表 |
| 72 小时调度器 | [Run2400Scheduler.py](Sources/Python/Run2400Scheduler.py) | 顶层分片恢复；深层断点尚缺 |
| WSL 复现 | [Run72hWSL.sh](Scripts/Run72hWSL.sh) | 支持 selftest、prepare、run、status、verify |

V16、V18–V20 保存为复现实验的历史版本。独立验证器 V2、原子账本与 G1 实验搜索器现已集成到研究目录/实验代码。V22–V24 保存于 [独立研究归档](Research/Session20261122/Readme.md)，**未替代 V21 主程序**。

## 运行入口（Linux/WSL2）

要求 C++17、GMP、zlib、Python 3 与 GitHub CLI。仓库根目录执行：

```bash
bash Scripts/Run72hWSL.sh selftest
bash Scripts/Run72hWSL.sh prepare
bash Scripts/Run72hWSL.sh status
```

只有显式运行 `bash Scripts/Run72hWSL.sh run` 才开始长时搜索；默认上限 72 小时，默认 16 个任务、每任务 2 个线程。其余环境变量见脚本。完成所有分片后还需数学规则审计与独立证书验证。

因子表 `checkfacts.txt.gz` 固定 SHA-256：

```text
ff1e84b119949ffcce57b29616d57ed5d03793ad3e4f74f1b203ad0e809f4119
```

## 证据与历史

- [原始实验日志](Records/ExperimentLog.md)；[当前里程碑](Records/Milestones.md)。
- [Ochem–Rao (2012) 论文](References/OchemRao2012.pdf)。
- [2026-11-22 整理前主分支](https://github.com/stormwhip/PerfectNumbers/tree/90100f4447f9196835951fdb7e9dcdd3ab23723f) 与 [V22–V24 原实验分支](https://github.com/stormwhip/PerfectNumbers/tree/research/exact-sigma-size-v22)。

**证明验收原则：** `PROVEN` 是求解器输出标签；无条件 \(10^{2400}\) 下界还要求完整覆盖、对偶证书、逐叶矛盾、确定性算术和独立校验器。