# PerfectNumbers 当前里程碑

**状态快照：2026-11-22（更新至独立验证器 V2/实验 G1）**。目标与当前完整状态见 [CurrentStatus2400.md](../Documentation/CurrentStatus2400.md)。全局状态仍为 `INCOMPLETE_FRONTIER`。

| 里程碑 | 当前状态 | 直接证据 | 下一项验收 |
| --- | --- | --- | --- |
| 前人 \(10^{1500}\) 下界 | 已发表的参考结果 | [Ochem–Rao 2012](../References/OchemRao2012.pdf) | 用作独立回归比较 |
| \(S_8\)-互素终局 LP | 旧阶段 LP 数值输出 2400.822998；最新互素类证书见上方 | [45001172416](https://github.com/stormwhip/PerfectNumbers/actions/runs/45001172416) | LP 模型涵盖性证明 + 独立导出对偶 |
| 256 个前缀区间表 | 生成成功 | [45004245214](https://github.com/stormwhip/PerfectNumbers/actions/runs/45004245214) | 独立核查系数、增益与调用条件 |
| 正式证明树版本 | V21 | [源代码](../Sources/Cpp/ProofTreeV21.cpp) · [质量检查](https://github.com/stormwhip/PerfectNumbers/actions/runs/45007403402) | 完整覆盖性与证明规则审计 |
| 根 19 指数分片 | 287 任务；164 个在 1 秒内完成，123 个超时 | [45005912683](https://github.com/stormwhip/PerfectNumbers/actions/runs/45005912683) | 长尾任务继续分片，穷尽证明 |
| 八根顺序优化 | 代理成本已分析 | [45007403299](https://github.com/stormwhip/PerfectNumbers/actions/runs/45007403299) | 比较全部八根的真实总成本 |
| V21 瓶颈剖析 | 素性测试是重要瓶颈 | [45012070442](https://github.com/stormwhip/PerfectNumbers/actions/runs/45012070442) | 优先在浅层规避昂贵运算 |
| V22 精确整除剪枝 | 数学规则可靠；性能实验负向 | [45011182741](https://github.com/stormwhip/PerfectNumbers/actions/runs/45011182741) | 仅作为理论与测试保留 |
| V23 素性测试去重 | 两个完成分片加速约 25%–30% | [45012354324](https://github.com/stormwhip/PerfectNumbers/actions/runs/45012354324) | 独立审计后考虑主线集成 |
| V24 合数乘积 GCD | 4,000 组差分通过；性能结果混合 | [45012698021](https://github.com/stormwhip/PerfectNumbers/actions/runs/45012698021) | 扩大已完成分片样本 |
| 72 小时运行框架 | 顶层分片支持重启 | [Run2400Scheduler.py](../Sources/Python/Run2400Scheduler.py) | 深层断点及全树实测 |
| 无条件 \(N>10^{2400}\) | **未完成** | [数学研究纲领](../Documentation/ResearchProblems2400.md) | 九类候选证书全部独立验收 |

历史 V1–V20 和更低目标的实验里程碑记录仍可通过[整理前版本](https://github.com/stormwhip/PerfectNumbers/blob/90100f4447f9196835951fdb7e9dcdd3ab23723f/Records/Milestones.md)访问；完整历史实验继续保存在 [ExperimentLog.md](ExperimentLog.md)。