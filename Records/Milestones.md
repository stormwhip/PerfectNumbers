# PerfectNumbers 当前里程碑

**更新于 2026-11-25。** 当前证明状态见 [CurrentStatus2400.md](../Documentation/CurrentStatus2400.md)。全局状态为 `INCOMPLETE_FRONTIER`。

| 里程碑 | 当前状态 | 直接证据 | 下一项验收 |
| --- | --- | --- | --- |
| 根 3 指数 1162 候选 | 新对偶及五指数的 E0/E1/E2 已复验，闭合增量 0 | [审计](../Research/P3I00193Review/Readme.md) | 完成共同素数池丰度及来源重叠计价 |
| 八根支持分割 | 复现 9 项新增条件排除，完整实际指数新增为 0 | [条件证据](../Research/SupportSplit/Readme.md) | 穷尽同一实际指数的剩余支持 |
| 午间证书并集 | 新增 202 片，累计闭合 2,868，开放 204 | [午间证书](../Research/Midday/README.md) | [剩余分片](../Research/Midday/Delta.json) |
| 两批来源与多根因子链证书 | 新增 165 项，累计闭合 2,192，开放 880 | [总证明](../Documentation/Proof2400.md)及[合并审计](../Research/EveningMerge/Audit.json) | [下一步计划](../Documentation/NextPlan2400.md) |
| Teichmüller 提升赋值判据 | 新增 146 项，累计闭合 2,015，开放 1,057 | [合并清单](../Research/TeichmullerValuation/Audit2400.json) | 继续证明开放分片 |
| 指标容量对偶 | 新增 18 项，累计闭合 1,869，开放 1,203 | [基线审计](../Research/IndicatorCapacity/Audit2400.json) | 已纳入最新合并审计 |
| 批量来源判据与扩大因子链 | 新增 46 项，累计闭合 1,851，开放 1,221 | [合并清单](../Research/SupplierBatch/BatchAudit2400.json) | 继续证明开放分片 |
| 根 3、5 的赋值和特殊素数来源证明 | 独立核验 241 项，与历史审计去重后净增 176 项。合计 1,805 项闭合，1,267 项开放 | [数学证明与核验](../Research/FermatRootValuation/FermatRootValuationReport.md) | 按合并审计清单继续求证 |
| 前人 \(10^{1500}\) 下界 | 已发表的参考结果 | [Ochem–Rao 2012](../References/OchemRao2012.pdf) | 用作独立回归比较 |
| \(S_8\)-互素终局 LP | 旧阶段 LP 数值输出 2400.822998；最新互素类证书见上方 | [45001172416](https://github.com/stormwhip/PerfectNumbers/actions/runs/45001172416) | LP 模型涵盖性证明 + 独立导出对偶 |
| 256 个前缀区间表 | 生成成功 | [45004245214](https://github.com/stormwhip/PerfectNumbers/actions/runs/45004245214) | 独立核查系数、增益与调用条件 |
| 正式证明树版本 | V21 | [源代码](../Sources/Cpp/ProofTreeV21.cpp) · [质量检查](https://github.com/stormwhip/PerfectNumbers/actions/runs/45007403402) | 完整覆盖性与证明规则审计 |
| 根 19 指数分片 | 287 任务；164 个在 1 秒内完成，123 个超时 | [45005912683](https://github.com/stormwhip/PerfectNumbers/actions/runs/45005912683) | 长尾任务继续分片，穷尽证明 |
| 八根顺序优化 | 代理成本已分析 | [45007403299](https://github.com/stormwhip/PerfectNumbers/actions/runs/45007403299) | 比较全部八根的真实总成本 |
| 顶层整数证明叶 | 数学排除规则覆盖 1,396/3,072，仍有 1,676 项 | [整数证明与实验](../Research/Session20261122/Reports/DirectRootClosure2400.md) | 执行 GitHub 新代码的独立 3,072 项审计并输出保存记录 |
| 分圆有限乘子证书 | 根 19 一项、根 11 两项完成精确整数枚举；候选总闭合 `1,399/3,072`，剩余 `1,673` | [理论与全部枚举](../Research/Session20261122/Reports/FiniteQuotientCyclotomic2400.md) | 执行最新 CI 和完整独立审计 |
| 直接闭合的根顺序优化 | 精确 256 状态 DP；全枚举 40,320 顺序对照，原根集可达到 1,397 | [RootOrderDirectClosureDP.py](../Research/Session20261122/Python/RootOrderDirectClosureDP.py) | 测量对完整证明树的真实影响；正式根顺序不变 |
| 分圆–Euler 素数乘积闭合 | 34 个数学排除，其中 33 个新增非重叠分片；累计候选 1,432/3,072，剩余 1,640 | [整数证明与分片列表](../Research/Session20261122/Reports/CyclotomicEulerPrimorial2400.md) | 执行新独立验证与全量直接证明审计 |
| 禁用根因子和指数 DP 闭合 | 新增 15 个完全非重叠整数叶；当前候选 1,447/3,072，剩余 1,625 | [严格 DP 证明与测试](../Research/Session20261122/Reports/CyclotomicExponentDP2400.md) | 运行新独立回归及 3,072 项完整审计 |
| Frontier C++ sigma 预筛 | 修复缺失头文件，精确模运算本地 36,100 次 GMP 对照通过 | [SigmaPrecheckTests.cpp](../Sources/Cpp/SigmaPrecheckTests.cpp) | 运行最新 GitHub CI、检查实验性 Frontier 可编译性 |
| V21 瓶颈剖析 | 素性测试是重要瓶颈 | [45012070442](https://github.com/stormwhip/PerfectNumbers/actions/runs/45012070442) | 优先在浅层规避昂贵运算 |
| V22 精确整除剪枝 | 数学规则可靠；性能实验负向 | [45011182741](https://github.com/stormwhip/PerfectNumbers/actions/runs/45011182741) | 仅作为理论与测试保留 |
| V23 素性测试去重 | 两个完成分片加速约 25%–30% | [45012354324](https://github.com/stormwhip/PerfectNumbers/actions/runs/45012354324) | 独立审计后考虑主线集成 |
| V24 合数乘积 GCD | 4,000 组差分通过；性能结果混合 | [45012698021](https://github.com/stormwhip/PerfectNumbers/actions/runs/45012698021) | 扩大已完成分片样本 |
| 72 小时运行框架 | 顶层分片支持重启 | [Run2400Scheduler.py](../Sources/Python/Run2400Scheduler.py) | 深层断点及全树实测 |
| 无条件 \(N>10^{2400}\) | **未完成** | [数学研究纲领](../Documentation/ResearchProblems2400.md) | 九类候选证书全部独立验收 |

历史 V1–V20 和更低目标的实验里程碑记录仍可通过[整理前版本](https://github.com/stormwhip/PerfectNumbers/blob/90100f4447f9196835951fdb7e9dcdd3ab23723f/Records/Milestones.md)访问；完整历史实验继续保存在 [ExperimentLog.md](ExperimentLog.md)。
