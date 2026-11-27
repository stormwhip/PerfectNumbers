# \(10^{2400}\) 证明发布验收清单

## 2026-11-28 研究分支收束

- [x] 验收 25 个新增规范精确键的分片归属和完整依赖：见[研究报告](../Research/FinalNight2400/Report.md)、[逐键复验计时](../Research/FinalNight2400/Proof.md)和[25 键独立集合重算](../Research/FinalNight2400/AuditNext/Projection25.md)。
- [x] 指定的五项历史入口均重放成功，含原始字节恢复后的两个默认 Gemini 入口：[实际回执](../Research/FinalNight2400/Audit/Baseline.md)。
- [ ] 排尽仍开放的 43 个分片与 53 个不同精确键。
- [ ] 全部历史原始输入至最终断言的一体冷重放和 72 小时验收；局部成功和本轮运行时间不得代替。

以下沿用各历史提交当时的状态，不作为对本轮结果的撤销。

## 2026-11-27 Gemini 增量验收

- [x] 原始提交算术复跑、历史回执绑定、单目标权重高次指标审阅、高次 Euler 修补、逐片投影独立重算。现行 3,004 闭合，68 开放，78 键。
- [ ] 在完整仓库重新运行[正式入口](../Research/GeminiFrontier/Verify.py)，包括历史 45/46 复验及全历史端到端重放；本轮未声称全历史通过。
- [ ] 补证两个联合定价候选；在[审阅](../Research/GeminiFrontier/Review.md)中保留开放状态。

## 2026-11-27 夜间增量验收

- 使用[夜间重放入口](../Research/Night2400/Replay.py)复验 13 个完整指数并重建投影。预期输出为 3,003 片闭合、69 片开放、79 个不同的待证键。
- [冻结晚间账本](../Research/FinalSprint/Delta.json)是投影输入，[逐片余集](../Research/Night2400/ShardToKeys.json)是本批输出。条件子域的证书留在[证明索引](../Research/Night2400/README.md)。
- 完成其余 69 个分片及全历史端到端重放后验收目标定理。

## 2026-11-26 晚间增量验收

- 以[冻结账本](../Research/Session20261126/Delta.json)为输入；用[晚间验证器](../Research/FinalSprint/Verify.py)复验 18 个完整指数的证明，再重算[晚间逐片账本](../Research/FinalSprint/Delta.json)。验收口径为新增 16 个闭片，而非 18 个闭片。
- [条件支持](../Research/FinalSprint/Support/README.md)及[低指数枢轴](../Research/FinalSprint/LowBranches/README.md)分别复验，不作为完整指数登记。
- 该批次验收后有 82 个开放分片。各日期保留当时的验收范围。

## 2026-11-25 历史证据验收

- 用 [LedgerTests.py](../Research/Midday/LedgerTests.py) 独立核验登记摘要和去重后的分片投影：2,868 闭合、204 开放。
- 用 [CheckLedger.py](../Research/Midday/CheckLedger.py) 重算午间登记包的算术及分支覆盖。原发布的隔离复验范围见 [ReleaseAudit.md](../Research/Midday/ReleaseAudit.md)。
- 用 [SupportSplit/Verify.py](../Research/SupportSplit/Verify.py) 核验冻结输入与九项条件排除。完整实际指数新增为 0。

- [x] `P3_I00193` 候选原包重放及扩大来源枚举通过。
- [ ] 修补净成本可加性、余块分配及严格对偶；复验所有叶后再登记。[专项审计](../Research/P3I00193Review/Readme.md)。

**截至 2026-11-24。** 本清单区分**运行成功**与**数学证明成立**。关联数学定义见 [形式化研究难题](../Documentation/ResearchProblems2400.md)，具体证据见 [总证明](../Documentation/Proof2400.md)。

> 当前已新增独立验证器 V2、SQLite 账本与只读 3072 项验收框架。数学验收仍未完成。权威进度见 [CurrentStatus2400.md](../Documentation/CurrentStatus2400.md)。

## 2026-11-23 根 3、5 分片

- [x] 独立核验根 3、5 的 241 项证明，重建顶层分片表和实际指数表。 [证明和重放命令](../Research/FermatRootValuation/FermatRootValuationReport.md)
- [x] 原根顺序下逐项合并历史证书，核对闭合 1,805 项、开放 1,267 项。 [合并审计](../Research/Session20261122/Python/AuditRootClass2400.py)
- [x] 合并并验收新增 46 份证明，累计闭合 1,851 项、开放 1,221 项。 [审计结果](../Research/SupplierBatch/BatchAudit2400.json)
- [x] 指标容量对偶新增 18 项，累计闭合 1,869 项。 [审计结果](../Research/IndicatorCapacity/Audit2400.json)

## 2026-11-24 Teichmüller 提升赋值判据

- [x] 逐项复验新增 146 个分片，累计闭合 2,015 项。 [审计结果](../Research/TeichmullerValuation/Audit2400.json)
- [ ] 完成其余 1,057 项并重放全局定理的完整证书。

## 历史验证器及验收记录（2026-11-22）

- [x] 集成外部固定根的 `IndependentVerifierV2.py`、可恢复 `FrontierLedgerV2.py` 及只读 `AuditRunner2400.py`，附合成/篡改测试源码。
- [x] 原根顺序下的 3,072 项纯整数枚举确认 14 个 `FORBIDDEN_FACTOR` 和 1,382 个 `SIGMA_DIVISOR_SIZE` 一步矛盾，共 1,396 项（45.44%）；证明规则已接入独立验证器与全量审计器。见 [DirectRootClosure2400.md](../Research/Session20261122/Reports/DirectRootClosure2400.md)。
- [x] 新增 3 个分圆有限乘子证明叶（根 19 的 d=936，根 11 的 d=1150、1152），穷举 734,381 个奇数余乘子全部排除；新证明规则与回归已写入仓库。见 [FiniteQuotientCyclotomic2400.md](../Research/Session20261122/Reports/FiniteQuotientCyclotomic2400.md)。
- [ ] 在最新 GitHub 提交实际运行 `AuditDirectRoot2400.py`，取得 1,399 个 `VERIFIED_CLOSED` 与 1,673 个 `UNSTARTED` 的可保存审计记录。
- [ ] CI 执行 `DirectRootClosuresTests.py`、`FiniteQuotientClosureTests.py`、`RootOrderDirectClosureDP.py`、`SigmaPrecheckTests.cpp` 以及已有 V2 回归，保存测试记录。
- [x] 原根集及替换根集互素类证书已有独立整数核验记录；两者分区隔离。
- [ ] 冻结 V21 搜索和实验 Frontier 输出完整可重验的证明 DAG，兼容持续分裂、路障和 LP。
- [ ] 全部 3,072 原根集顶层任务由独立验证器报告 `VERIFIED_CLOSED`，开放和未解决任务均为零；当前已找到 1,396 项直接矛盾及 3 项有限乘子整数穷举矛盾，其他 1,673 项待证明树闭合。
- [ ] 证明生成、原子提交、独立验收在固定硬件和数据下完成 72 小时端到端实测。
- [x] 目录调整后的 GitHub 文件名检查和全部 20 份 Markdown 的本地链接检查通过（0 失效链接）。
- [ ] 手动执行最新 `RepositoryIntegrity.yml` 的 Python/C++ 回归，并保存运行证据。

## A. 输入与程序可重复性

- [x] 固定 Ochem 因子表输入哈希 `ff1e84b119949ffcce57b29616d57ed5d03793ad3e4f74f1b203ad0e809f4119`。
- [x] 建立 C++ GMP 索引器与完整主线 V21；V21 核心单元测试通过（[45007403402](https://github.com/stormwhip/PerfectNumbers/actions/runs/45007403402)）。
- [x] 生成所有 256 个根前缀的 LP 对偶表，附相应输出文件哈希（[45004245214](https://github.com/stormwhip/PerfectNumbers/actions/runs/45004245214)）。
- [x] 建立顶层指数任务清单、SHA 校验和已完成分片恢复（调度器及其合成测试）。
- [ ] 每个深层证明状态都可断点保存、恢复，且恢复前后无漏项、无重复接受。
- [ ] 72 小时验收记录固定 commit、GMP 编译版本、CPU 核数、线程参数、所有输入与结果文件哈希。

## B. 数学模型与对偶证书

- [x] 增强 \(S_8\)-互素 LP 计算产生指数 \(2400.822998027028\)（**数值实验，不等同已证明的定理**）。
- [x] 关键 \(\sigma(61^{10}),\sigma(61^{12})\) 的整数分解与素性检验脚本运行通过（[45001172416](https://github.com/stormwhip/PerfectNumbers/actions/runs/45001172416)）。
- [ ] 独立证明 LP 完整包含全部可能的奇完全数普通/特殊指数情形和 \(P_{\max},a_{\mathrm{cut}}\) 外的无限尾。
- [ ] 验证所有因子和蕴含约束对实际素数指数选择成立，特别是 61 的高指数约束。
- [ ] 导出完整对偶证书（精确矩阵系数、乘子、界约束、负 reduced costs、严格区间数值）；独立验证 \(\mathrm{LB}>2400\log10\)。
- [ ] 对 256 个前缀和状态增益证书独立检查区间方向、重复扣除与 Euler 特殊素数名额。

## C. 因子链证明的完备性和正确性

- [ ] 形式化证明 V21 的每种顶层/内部分支指数覆盖引理（包含 \(p=3,7\)、特殊奇指数与非精确指数）。
- [ ] 形式化证明各根的前缀互斥与九类完整覆盖。
- [ ] 证明 roadblock 的分数背包放松和无限素数尾下界，以及确定上界 \(b\) 的单调性。
- [ ] 证明合数残余的最小素因子界、丰度上界、尺寸计数及重叠处理全部安全。
- [ ] 将所有决定分支生死的浮点阈值更换为严格区间/有理数比较，或附显式认证余量。
- [ ] 数据库里每个当作素数使用的因子都提供确定性素性证书；分解过程需经整数乘法复核。
- [ ] 对八根 \((19,7,11,31,13,3,5,17)\) 的全部指数分片完成搜索，且无 unresolved / timeout / 失败 roadblock。
- [ ] 输出每个闭合叶节点对应的可独立验证的矛盾证据。

## D. 独立验证与最终发布

- [ ] 开发与搜索器相互独立的短小证书验证器，覆盖全部 LP 对偶证书、根/指数覆盖以及每条叶结点推理。
- [ ] 在第二环境重验完整数据、任务划分及全部已闭合叶节点，完成证书 DAG 的哈希/覆盖性审计。
- [ ] 由完整八根证书与互素 LP 证书推出 \(\forall N\in\mathcal O,\ N>10^{2400}\)。
- [ ] 在目标硬件上验证总运行墙钟时间 \(\le72\) 小时，包括可重启任务的全部输出和证明校验。

## E. 已完成的性能研究（不计入证明验收）

- [x] 根 19 的 287 个顶层指数任务普查：164 个 1 秒内完成、123 个超时（[45005912683](https://github.com/stormwhip/PerfectNumbers/actions/runs/45005912683)）。
- [x] V21 函数计时定位 GMP 素性测试开销（[45012070442](https://github.com/stormwhip/PerfectNumbers/actions/runs/45012070442)）。
- [x] V22 精确整除剪枝：数学规则与实现测试通过，完成分片未体现运行时优势。
- [x] V23 去除重复素性测试：两个已完成分片相对 V21 运行时间减少约 25%–30%（[45012354324](https://github.com/stormwhip/PerfectNumbers/actions/runs/45012354324)）。
- [x] V24 乘积 GCD：4,000 组随机差分一致，时间改善尚不稳定（[45012698021](https://github.com/stormwhip/PerfectNumbers/actions/runs/45012698021)）。

原 V16 时期的历史审计记录保留于 [旧提交](https://github.com/stormwhip/PerfectNumbers/blob/90100f4447f9196835951fdb7e9dcdd3ab23723f/Records/ValidationChecklist.md)。

## 根 3 续研验收

- [x] 五指数的 E0/E1/E2 独立整数证明、42 叶保守重算、5829 个来源素数检查。
- [x] 34972 余块与 $A$ 的 gcd 及候选 Euler 素数下界检查。
- [x] 新对偶 1441 列的精确有理数检验及恶意篡改回归。
- [ ] 完成未激活森林节点丰度、大余块与来源重叠、全部叶的联合严格下界。

[证书、结果与复验命令](../Research/P3I00193Review/Progress.md)。
