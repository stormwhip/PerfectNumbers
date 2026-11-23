> **整数复验更新（2026-11-23）**　原根集固定顺序下，合并审计已复验 **1,628 / 3,072** 个顶层分片，剩余 **1,444** 个。相对仓库 1,447 项基线，根 17 整类新增 125 项、根 5 分圆剩余乘子对偶新增 54 项，根 7、根 31 各新增 1 项。根 17 的整类下界为 `log10 N >= 2847.836220`。根 5 另有 18 项已排除 `17∤N` 分支，其 `17|N` 分支仍开放。完整规则、逐根清单与复验命令见 [RootClassValuationAudit2400](../Research/Session20261123/Reports/RootClassValuationAudit2400.md)。全局状态仍为 `INCOMPLETE_FRONTIER`。

> **2026-11-23 Gemini v5 最新研究记录：** 新报告称 3,072 个顶层任务中 **1,679 项 REPRODUCED_VERIFIED**、**1,393 项 OPEN**（较上一份 Gemini 报告净关闭 30 项）；终局互素类与根 17 整类仍报告闭合；根 5 已报告 301/481 项闭合。规则 VII 旧整除断言已被反例推翻，改为仅可用于数值尺寸下界；`P13_I00165` 尚未复现。**上传仅有研究报告和一个 C++ 因子发现工具源码，未提供所述 JSON 证书、完整 31 份 DAG 和独立验证器供本仓库复现。** 请区分 Gemini 报告中的 `REPRODUCED_VERIFIED` 与本仓库的 `EXTERNAL_REPORTED_PENDING_REPLAY`。报告归档见 [ResearchResultV5](../Research/Session20261123/Reports/ResearchResultV5.md)，逐根状态与下一步见 [GeminiProgressReviewV5](GeminiProgressReviewV5.md)。**全局定理：`INCOMPLETE_FRONTIER`；72 小时全量运行：未完成。**

> **2026-11-23 Gemini 外部报告更新：** Gemini 提交了一份新进展报告，宣称原根集的顶层任务已有 **1,649 / 3,072** 闭合、剩余 **1,423**，并称终局互素类及根 17 整类已通过证书验证。该次上传包含报告及旧交接文件，**未附新 JSON 证书、19 份 DAG、完整验证器和新开放清单**。本仓库仅记录外部报告，新增数字统一标为 `EXTERNAL_REPORTED_PENDING_REPLAY`；原文较早的 1,447 项基线与历史进展保留，详见 [Gemini 新进展与验证待办](GeminiProgressReview20261123.md)。**全局状态仍为 `INCOMPLETE_FRONTIER`。**

# PerfectNumbers — 当前证明状态与接下来的工作

**更新日期：2026-11-23**。版本参考：`7d7c1c6`（目录重构前）；正式搜索基线 **V21**。研究目标：构造可独立复核的计算证明，排除全部奇完全数 `N <= 10^2400`；并在固定硬件上测量是否能在 **72 小时**内完成。

## 1. 已有可复核结果与当前结论

- 原根集 `S={3,5,7,11,13,17,19,31}` 的互素类，独立整数验证记录给出 `log10 N >= 4183.209493`。替换根集 `S'=(S-{19})+{23}` 对应 `log10 N >= 3954.197016`；两根集的八个含根类不得交叉拼接。
- 原根集共有 **3,072 个顶层指数任务**，根 3、5、7、11、13、17、19、31 分别为 676、481、412、341、325、297、287、253 项；替换集为 3,058 项。这些是指数**覆盖任务数**，不是完成证明数。
- V21 根 19 的 287 项历史 1 秒检查结果：164 项输出程序 `PROVEN`、123 项超时。二者都不代表已获独立证书；本页首段列出本轮原根集全清单复验结果。
- 已集成独立根固定证明核验器、可恢复 SQLite 前沿账本、C++ 状态编解码、实验性 G1 复用搜索器和只读全量审计运行器。**当前全局状态：`INCOMPLETE_FRONTIER`**。现有实验性求解器 `PROVEN_UNAUDITED` 不能计入定理证明。
- 新增**两类纯整数顶层直接证明叶**：先前排除的根素数整除 `σ(p^d)` 产生 14 个 `FORBIDDEN_FACTOR` 证书；由 `p^d·odd(σ(p^d)) | N` 及尺寸超界产生 1,382 个 `SIGMA_DIVISOR_SIZE` 证书，互不重叠。独立整数枚举覆盖 **1,396 / 3,072（45.44%）** 个顶层分片；其余 **1,676 个**仍需证明树及证书。代码已接入独立验证器与全量审计器，新增仓库测试尚待 CI 运行。见 [证明与实验](../Research/Session20261122/Reports/DirectRootClosure2400.md)。
- 新增**分圆多项式素因子 + 有限乘子证书**：根 `19,d=936`、根 `11,d=1150`、根 `11,d=1152` 的剩余乘子范围分别为 `1,411,815`、`56,941`、`3`。精确整数枚举对 `705,908`、`28,471`、`2` 个奇数剩余乘子均给出矛盾。代码已接入 V2 独立证明叶验收，新增 `FINITE_QUOTIENT_CYCLOTOMIC`。**该阶段累计 1,399/3,072（45.54%），当时剩余 1,673 项**；后续分圆–Euler 乘积界见下条。参见 [理论与复现实验](../Research/Session20261122/Reports/FiniteQuotientCyclotomic2400.md)。
- 新增 **分圆–Euler 素数乘积丰度界**：无需分解 `Phi_m(p)`，利用其素因子模类、Euler 指数条件、禁用根与剩余乘子共享尺寸预算，排除 34 个顶层分片，其中 `(11,1152)` 与有限乘子证书重叠。净增加 **33 个**独立验证器可重算的整数证明叶。**该阶段候选累计 1,432/3,072（46.61%），当时剩余 1,640 项**；[严格数学证明与清单](../Research/Session20261122/Reports/CyclotomicEulerPrimorial2400.md)。已提交代码及单元测试，最新全量审计仍待执行。
- 本轮已逐项核验全清单的 3,072 项，仍有 1,444 项开放。尚无在固定条件下完成 72 小时目标的实测。

## 2. 本轮新增基础设施

| 模块 | 文件入口 | 状态 |
| --- | --- | --- |
| 正式搜索基线 | [ProofTreeV21.cpp](../Sources/Cpp/ProofTreeV21.cpp) | 保留作对照，八根未全闭合 |
| 独立验证器 | [IndependentVerifierV2.py](../Research/Session20261122/Python/IndependentVerifierV2.py) | 合成树与防篡改测试；真实完整 DAG 未打通 |
| 全量审计器 | [AuditRunner2400.py](../Research/Session20261122/Python/AuditRunner2400.py) | 覆盖 3072/3058 项；已接入两类直接整数证书快通道 |
| 顶层直接闭合证书 | [DirectRootClosures2400.py](../Research/Session20261122/Python/DirectRootClosures2400.py) | 基础两类整数叶 1,396 项；另有两类新规则；见 [数学证明与实验](../Research/Session20261122/Reports/DirectRootClosure2400.md) |
| 禁用根指数 DP 整数证书 | [CyclotomicExponentDPClosure2400.py](../Research/Session20261122/Python/CyclotomicExponentDPClosure2400.py) | 15 个新增整数叶；独立验证器已接入，待新完整 CI 审计 |
| 分圆–Euler 素数乘积证书 | [CyclotomicPrimorialClosure2400.py](../Research/Session20261122/Python/CyclotomicPrimorialClosure2400.py) | 33 个新增非重叠整数叶；独立验证器已接入，待新完整 CI 审计 |
| 分圆有限乘子证明 | [FiniteQuotientClosure2400.py](../Research/Session20261122/Python/FiniteQuotientClosure2400.py) | 3 项完整整数穷举，独立验证器已接入；最新 CI 待执行 |
| 精确根顺序优化 | [RootOrderDirectClosureDP.py](../Research/Session20261122/Python/RootOrderDirectClosureDP.py) | 精确 DP + 40,320 个根排列交叉检查；正式根顺序保持不变 |
| 全量直接证书审计 | [AuditDirectRoot2400.py](../Research/Session20261122/Python/AuditDirectRoot2400.py) | 以缺失账本为输入检查 1,447 项；新增回归尚待运行 |
| 原子前沿账本 | [FrontierLedgerV2.py](../Research/Session20261122/Python/FrontierLedgerV2.py) | 故障恢复/分裂存储测试 |
| C++ 前沿编解码 | [V21FrontierCodec.hpp](../Sources/Cpp/V21FrontierCodec.hpp) | V2 状态协议、旧掩码坐标、残余保序 |
| 实验性搜索器 | [ProofTreeV21Frontier.cpp](../Sources/Cpp/ProofTreeV21Frontier.cpp) | G1 初筛复用；未移植全部 V21 路障/LP |
| 并发单飞缓存 | [SingleFlightFactCache.hpp](../Sources/Cpp/SingleFlightFactCache.hpp) | 独立组件，尚未接入实际因子缓存 |
| Worker 桥接 | [FrontierWorkerDriver.py](../Research/Session20261122/Python/FrontierWorkerDriver.py) | 部分串联；未导出可接受的完整证明 DAG |

先前上传材料报告 Python 合成/故障注入和 C++ 小型测试成功；目录重构后的 CI 要重新运行这些测试。旧性能数据详见 [实验记录](../Records/ExperimentLog.md) 与 [集成报告](../Research/Session20261122/Reports/IndependentProofIntegration2400.md)。

## 3. 未完成任务（按依赖次序）

1. **P0 — 生成真正的独立证明 DAG。** 全清单审计接受了 1,628 项。下一步 C++ 为其余 1,444 项中的直接闭合、普通分裂、封闭叶、循环分裂导出全部父边证据；账本存储与 Python 验证器逐状态一致，并对篡改、重放、中断拒绝错误闭合。
2. **P0 — 补齐冻结 V21 的搜索规则。** 将路障、循环新素数枚举、延迟残余强化与全部 256 前缀/状态 LP 的数学语义转移到新搜索器，并独立证明每类剪枝可靠。先比较根 19 的分片 130、35，再比较 66、132、138、149，最后测困难 0、100。
3. **P0 — 大素数的确定性素性证书与精确算术。** GMP probable-prime 仅用于探索，必须输出可独立检查的素性见证；校验来源分离赋值、Euler 指数、残余最小素因子下界和区间取整方向。
4. **P1 — 提高困难分片吞吐。** 把单飞缓存接入 `get_sigma_fact`，固定键 `(p,d+1)` 与线程读写生命期；测算完整分片耗时、任务切分代价及关键路径。
5. **P1 — 全量 3,072 项独立验收。** 统一根集、清单和哈希，输出 `VERIFIED_CLOSED` 全量统计；未核验的 `PROVEN`、超时、开放前沿、证书缺项一律视为未完成。
6. **P2 — 72 小时实机验收。** 固定机器、GMP/编译器版本、数据库指纹、证书规则，实测 `T_prep+T_search+T_verify`；报告每项任务、最长链与调度开销。

### 定理验收标准

固定 `B=10^2400`，先独立核验原根集的互素终结证书，再对 3,072 项逐根回放证明 DAG。所有叶与分裂均由确定性数学规则验证、所有真实强制素数均有确定性证书，且总开放前沿、失败证书、未覆盖分支均为零，才可输出 `UNCONDITIONALLY_VERIFIED`。

## 4. 文档职责与迁移说明

- 本文为唯一**当前状态入口**；[ProgressReport2400.md](ProgressReport2400.md) 保留完整阶段细节；[RepositoryMap.md](RepositoryMap.md) 列出最新代码与文件夹。
- [ResearchProblems2400.md](ResearchProblems2400.md) 是形式化数学难题，部分旧数值实验属于历史阶段。
- [Milestones.md](../Records/Milestones.md) 为阶段任务表；[ValidationChecklist.md](../Records/ValidationChecklist.md) 是发布门槛；[ExperimentLog.md](../Records/ExperimentLog.md) 是历史运行记录。
- 旧研究目录 `Research/2026-11-22/` 在本次整理中统一为 `Research/Session20261122/`；原 `README.md` 统一为 `Readme.md`。GitHub 必需的 `.github/workflows/`、`.gitignore` 采用平台固定命名。
- 目录整理仅改变路径与文档链接；没有执行新一轮 72 小时大规模实验，没有新增完全证明。

## 5. 仓库维护与质量回归

整理后代码仍使用原 V21 正式生产入口。实验性 V21 Frontier 已修复旧路径引用的缺失 `SigmaPrecheck.hpp`，并增加精确 GMP 差分回归；本地同等实现通过 36,100 组对照，GitHub 最新 CI 尚待执行。目录一致性可通过 [RepositoryStructureChecks.py](../Sources/Python/RepositoryStructureChecks.py) 检查；[手工 CI 工作流](../.github/workflows/RepositoryIntegrity.yml) 可以重新跑 Python 证明/账本的合成回归、C++ 编解码和缓存测试。该 CI 只验证实现一致性，不将任何程序标签自动升级为数学证明。

### 目录整理核验（2026-11-22）

- GitHub 文件树复核：97 个已追踪文件，20 份 Markdown 文档；所有实际路径均符合 PascalCase 约定，平台保留名称 `.github/workflows` 与 `.gitignore` 不变。
- 原 `Research/2026-11-22/` 下 41 个文件已完整迁移至 `Research/Session20261122/`；31 个文件 SHA-1 未变，其余 10 个为更新 README 与历史报告状态/路径的文档。两份 `Terminal*.json.gz` 证书 blob 保持完全一致。
- 已直接读取并扫描全部 20 份当前 Markdown 的本地相对链接：**0 条失效链接**；历史已移除工作流的链接已改指历史 Git 快照。
- 加入 [RepositoryStructureChecks.py](../Sources/Python/RepositoryStructureChecks.py) 和可手工运行的 [RepositoryIntegrity.yml](../.github/workflows/RepositoryIntegrity.yml)，用于今后重复验证。工作流尚未手动触发，本记录不宣称最新代码回归已在 CI 中运行。
- 上述目录整理数字为历史快照。其后新增了直接整数证明叶、独立审计入口和 C++ 回归；当前总文件数与 Markdown 数已改变。本轮没有运行八根完整证明树，也没有建立新的无条件奇完全数下界。
