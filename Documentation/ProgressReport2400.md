# PerfectNumbers：\(10^{2400}\) 当前进展报告

**更新日期：2026-11-22** · **主分支基线：V21** · **研究分支：V22–V24** · **研究目标：给出可独立验证的无条件 \(N>10^{2400}\) 证明**。

> **当前结论：** 八个指定素因子全部缺失时的增强 LP 输出下界指数 \(2400.822998027028\)；八个含根素数的证明树尚未全部完成；独立的全域 LP、因子链与精确算术审计仍未通过。完整定理未完成。

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

它超过目标指数 \(2400\)，但需要**独立证明每个真实候选必映射到 LP 的可行解**、再将求解器对偶向量导出为可复核的有理或向外舍入区间证书。上述数值尚不能单独宣称为已完成的数学定理。

## 4. V21：困难根的实证

[根 19 完整顶层指数清点 45005912683](https://github.com/stormwhip/PerfectNumbers/actions/runs/45005912683)：

- **287** 个指数任务；
- **164** 个在每分片 1 秒限时内返回 `PROVEN`；
- **123** 个在该限时下 `TIMEOUT`。

对这 123 项 [调整根 19 的全局位置](https://github.com/stormwhip/PerfectNumbers/actions/runs/45006916458) 时，有 73 项能在相应的 1 秒预算内完成，仍有 50 项超时。此对照改变前缀禁用条件，不能单独作为新顺序对全部八根的总体加速证据。

[八根顺序动态规划 45007403299](https://github.com/stormwhip/PerfectNumbers/actions/runs/45007403299) 对代理指标进行了全子集优化：其代理成本降幅约 0.03%–2.64%，尚无完整八根墙钟耗时的证明。短时测试中，根 19、17、31 仍不能在 30 秒内穷尽。

**72 小时目标未经过完整实测验证。**

## 5. 2026-11-22 性能研究 V22–V24

所有新原型均保存在 [Research/2026-11-22/](../Research/2026-11-22/README.md)，不改变正式 V21 调度脚本。

| 版本 | 数学/工程改动 | 实验结论 |
| --- | --- | --- |
| V22 | 基于 \(\operatorname{odd}(\sigma(p^a))\mid N\) 的精确整除及乘积 LCM 剪枝 | 数学规则明确且通过回归，已完成分片中增加运行耗时 |
| V23 | 对同一个 \(\sigma\) 残余复用第一次 GMP 素性测试，残余改变时重检 | 已完成的根 19 分片 35 与 130，分别降低约 30.1% 与 24.9% 的耗时 |
| V24 | 将合数残余逐项互素测试改为乘积 GCD | 4000 组随机差分验证一致；实际运行表现不稳定 |

主要证据：[V22 首轮](https://github.com/stormwhip/PerfectNumbers/actions/runs/45011182741)、[V22 延迟剪枝](https://github.com/stormwhip/PerfectNumbers/actions/runs/45011614919)、[V21 性能剖析](https://github.com/stormwhip/PerfectNumbers/actions/runs/45012070442)、[V23 对照](https://github.com/stormwhip/PerfectNumbers/actions/runs/45012354324)、[V24 对照](https://github.com/stormwhip/PerfectNumbers/actions/runs/45012698021)。

V21 剖析表明素性测试是困难分片 0、100 的主要计时热点。V23 在两项完整结束的分片中实现了有效加速。V22 与 V24 目前均不满足替换正式主线的性能证据标准。

## 6. 下一阶段研究优先级

1. **P0 — LP 正确性与独立证书：** 完成无限尾部、特殊指数、\(\sigma(61^{10}),\sigma(61^{12})\) 蕴含模型的涵盖证明；导出可独立校验的区间/有理对偶见证。
2. **P0 — 较早层次的困难树剪枝：** 构造考虑已选指数、强制素数和 Euler 名额的条件化 LP，优先在大量素性测试以前关闭子树，必须以已完成分片墙钟耗时验收。
3. **P0 — 八根穷尽性与 roadblock：** 证明指数选项覆盖、无穷尾尺寸和丰度约束安全，完成所有顶层及必要深层任务。
4. **P1 — 独立算术与证明树验证：** 对数据库素性、分解、浮点边界和每条闭合规则导出独立证书，生成可重验的证明 DAG。
5. **P1 — 深层断点与 72 小时评估：** 在固定代码和数据版本下，进一步切分长尾任务，完成全树工作量测量，再验收实际 72 小时运行。

## 7. 证据与研究入口

- [形式化数学研究难题](ResearchProblems2400.md)
- [当前验收清单](../Records/ValidationChecklist.md)
- [研究实验归档](../Research/2026-11-22/README.md)
- [历史实验日志](../Records/ExperimentLog.md)
- [Ochem–Rao (2012) 原始论文](../References/OchemRao2012.pdf)

**结论：** 当前研究瓶颈集中在**可独立认证的数学剪枝**与**所有困难根的可终止证明树**；V23 已降低局部计算成本，仍需通过全树证书和可靠的端到端运行把数值研究推进为无条件定理。