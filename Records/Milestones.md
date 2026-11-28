# 完全数证明里程碑

[当前状态](../Documentation/CurrentStatus2400.md)给出逐根统计和待证集合。[总证明](../Documentation/Proof2400.md)汇总数学推导，[实验日志](ExperimentLog.md)记录运行参数与结果。

## 分片证明时间线

| 批次 | 闭合 / 3,072 | 开放 | 冻结证据 |
|---|---:|---:|---|
| 根 3、5 赋值与来源 | 1,805 | 1,267 | [复验报告](../Research/FermatRootValuation/FermatRootValuationReport.md) |
| 批量来源与扩大因子链 | 1,851 | 1,221 | [审计](../Research/SupplierBatch/BatchAudit2400.json) |
| 指标容量 | 1,869 | 1,203 | [审计](../Research/IndicatorCapacity/Audit2400.json) |
| Teichmüller 提升 | 2,015 | 1,057 | [审计](../Research/TeichmullerValuation/Audit2400.json) |
| Gemini 批次并集 | 2,027 | 1,045 | [审计](../Research/TeichmullerValuation/GeminiBatchAudit2400.json) |
| 来源间隙与多根因子链并集 | 2,192 | 880 | [审计](../Research/EveningMerge/Audit.json) |
| 夜间并集 | 2,646 | 426 | [审计](../Research/NightMerge/Audit.json) |
| 11 月 25 日上午 | 2,666 | 406 | [账本](../Research/Nov25/Delta.json) |
| 11 月 25 日午间 | 2,868 | 204 | [账本](../Research/Midday/Delta.json) |
| 11 月 25 日 SupportSplit | 2,868 | 204 | [九项条件排除](../Research/SupportSplit/Readme.md) |
| 11 月 25 日 P3_I00193 | 2,868 | 204 | [候选重放及净成本缺口](../Research/P3I00193Review/Readme.md) |
| 11 月 26 日晚间前（冻结基线） | 2,974 | 98 | [账本](../Research/Session20261126/Delta.json) · [验收](../Research/Session20261126/Validation.md) |
| 11 月 26 日晚间 | 2,990 | 82 | [逐片账本](../Research/FinalSprint/Delta.json) · [证明与复验](../Research/FinalSprint/Proof.md) |
| 11 月 27 日夜间 | 3,003 | 69 | [增量账本](../Research/Night2400/Delta.json) · [证书索引](../Research/Night2400/README.md) |
| 11 月 27 日 Gemini 增量 | 3,004 | 68 | [账本](../Research/GeminiFrontier/Delta.json) · [审阅](../Research/GeminiFrontier/Review.md) |
| **11 月 28 日 PR #10 研究分支** | **3,029** | **43** | [逐片余集](../Research/FinalNight2400/OpenFrontier.json) · [逐键回执](../Research/FinalNight2400/Proof.md) |

| 11 月 28 日 PR #12 | 3,031 | 41 | [逐片余集](../Research/AstraFinalAfternoon2400/OpenFrontier.json) |
| 11 月 28 日 PR #13、#14 理论研究 | 3,031 | 41 | [独立审阅](../Research/JointConservation2400/MergeReview.md)；零新增闭片 |

11 月 26 日晚间前排除 134 个不同的 $(p,e)$ 并新增闭合 106 片，晚间批次分别再增 18 和 16。11 月 27 日夜间批次又排除 13 个不同的 $(p,e)$，各清空一个单指数分片。Gemini 后续增量排除 $(13,508)$，新增闭合 1 片。该冻结基线有 68 个开放分片、78 个不同的 $(p,e)$、60 个单指数片。PR #10 新增 25 个完整精确键，独立投影复算后余 43 片、53 键、35 个单指数片。剩余分片构成 $N>10^{2400}$ 的待证情形。

对与原八根全部互素的情形，已认证的下界为 $\log_{10}N\ge4183.209493$。将根 19 替换为 23 后，相应互素类的下界为 $\log_{10}N\ge3954.197016$。这两项均为指定根集的互素类结果。

历史工程细节和性能试验见[早期完整报告](https://github.com/stormwhip/PerfectNumbers/blob/9d74c34dda8908a19542b855c78ef2feb8844b66/Documentation/ProgressReport2400.md)。

## 数学证书与程序验证

| 里程碑 | 当前状态 | 直接证据 | 下一项验收 |
| --- | --- | --- | --- |
| 根 3 指数 970、990 | 两项全域证明均已登记 | [970](../Research/FinalSprint/Full970.md) · [990](../Research/FinalSprint/Proof990.md) | 根 3 剩余 6、12、856 |
| 根 3 指数 1,108、1,162 | 两项全域证书均已登记 | [1,108](../Research/Session20261126/Joint1108/Readme.md) · [1,162](../Research/Session20261126/Joint/README.md) | 保留历史回归 |
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

历史 V1–V20 和更低目标的实验里程碑记录仍可通过[整理前版本](https://github.com/stormwhip/PerfectNumbers/blob/90100f4447f9196835951fdb7e9dcdd3ab23723f/Records/Milestones.md)访问；完整历史实验继续保存在 [ExperimentLog.md](ExperimentLog.md)。

11 月 27 日后续增量补齐 $(19,58)$ 的 $T^{10}$ 子域；C10 历史开放路径 11→10，仍为 3,004 闭片、68 开片、78 键。
