# PerfectNumbers — 当前证明状态与接下来的工作

**更新日期：2026-11-22**。版本参考：`7d7c1c6`（目录重构前）；正式搜索基线 **V21**。研究目标：构造可独立复核的计算证明，排除全部奇完全数 `N <= 10^2400`；并在固定硬件上测量是否能在 **72 小时**内完成。

## 1. 已有可复核结果与当前结论

- 原根集 `S={3,5,7,11,13,17,19,31}` 的互素类，独立整数验证记录给出 `log10 N >= 4183.209493`。替换根集 `S'=(S-{19})+{23}` 对应 `log10 N >= 3954.197016`；两根集的八个含根类不得交叉拼接。
- 原根集共有 **3,072 个顶层指数任务**，根 3、5、7、11、13、17、19、31 分别为 676、481、412、341、325、297、287、253 项；替换集为 3,058 项。这些是指数**覆盖任务数**，不是完成证明数。
- V21 根 19 的 287 项历史 1 秒检查结果：164 项输出程序 `PROVEN`、123 项超时。二者都不代表已获独立证书；最新全量 `VERIFIED_CLOSED` 数尚无完整验收报告。
- 已集成独立根固定证明核验器、可恢复 SQLite 前沿账本、C++ 状态编解码、实验性 G1 复用搜索器和只读全量审计运行器。**当前全局状态：`INCOMPLETE_FRONTIER`**。现有实验性求解器 `PROVEN_UNAUDITED` 不能计入定理证明。
- 新增了针对原根集的**14 项顶层直接排除证书生成规则**：整数模幂先发现先前禁止根素数整除 \(\sigma(p^d)\)，生成单个 `FORBIDDEN_FACTOR` 叶，并由 `IndependentVerifierV2` 在审计时重新核验。独立整数实验核对了 14 个整除关系；新增 Python 仓库回归尚待 CI 实际执行。其余 **3,058 项**尚无完整证明证书。\n- 目前无全量独立核验完成记录，也无在固定条件下完成 72 小时目标的实测。禁止将短窗超时样本视为总运行时间的上界。

## 2. 本轮新增基础设施

| 模块 | 文件入口 | 状态 |
| --- | --- | --- |
| 正式搜索基线 | [ProofTreeV21.cpp](../Sources/Cpp/ProofTreeV21.cpp) | 保留作对照，八根未全闭合 |
| 独立验证器 | [IndependentVerifierV2.py](../Research/Session20261122/Python/IndependentVerifierV2.py) | 合成树与防篡改测试；真实完整 DAG 未打通 |
| 全量审计器 | [AuditRunner2400.py](../Research/Session20261122/Python/AuditRunner2400.py) | 覆盖 3072/3058 项；已接入直接根矛盾的独立审计快通道 |\n| 顶层直接闭合证书 | [DirectRootClosures2400.py](../Research/Session20261122/Python/DirectRootClosures2400.py) | 原根集识别 14 项；见 [数学证明与实验](../Research/Session20261122/Reports/DirectRootClosure2400.md) |
| 原子前沿账本 | [FrontierLedgerV2.py](../Research/Session20261122/Python/FrontierLedgerV2.py) | 故障恢复/分裂存储测试 |
| C++ 前沿编解码 | [V21FrontierCodec.hpp](../Sources/Cpp/V21FrontierCodec.hpp) | V2 状态协议、旧掩码坐标、残余保序 |
| 实验性搜索器 | [ProofTreeV21Frontier.cpp](../Sources/Cpp/ProofTreeV21Frontier.cpp) | G1 初筛复用；未移植全部 V21 路障/LP |
| 并发单飞缓存 | [SingleFlightFactCache.hpp](../Sources/Cpp/SingleFlightFactCache.hpp) | 独立组件，尚未接入实际因子缓存 |
| Worker 桥接 | [FrontierWorkerDriver.py](../Research/Session20261122/Python/FrontierWorkerDriver.py) | 部分串联；未导出可接受的完整证明 DAG |

先前上传材料报告 Python 合成/故障注入和 C++ 小型测试成功；目录重构后的 CI 要重新运行这些测试。旧性能数据详见 [实验记录](../Records/ExperimentLog.md) 与 [集成报告](../Research/Session20261122/Reports/IndependentProofIntegration2400.md)。

## 3. 未完成任务（按依赖次序）

1. **P0 — 生成真正的独立证明 DAG。** 已完成顶层 `FORBIDDEN_FACTOR` 一步证书的生成与审计集成，原根集共识别 14 项。下一步 C++ 为其余直接闭合、普通分裂、封闭叶、循环分裂导出全部父边证据；账本存储与 Python 验证器逐状态一致，并对篡改、重放、中断拒绝错误闭合。
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

整理后代码仍使用原 V21 正式生产入口。目录一致性可通过 [RepositoryStructureChecks.py](../Sources/Python/RepositoryStructureChecks.py) 检查；[手工 CI 工作流](../.github/workflows/RepositoryIntegrity.yml) 可以重新跑 Python 证明/账本的合成回归、C++ 编解码和缓存测试。该 CI 只验证实现一致性，不将任何程序标签自动升级为数学证明。

### 目录整理核验（2026-11-22）

- GitHub 文件树复核：97 个已追踪文件，20 份 Markdown 文档；所有实际路径均符合 PascalCase 约定，平台保留名称 `.github/workflows` 与 `.gitignore` 不变。
- 原 `Research/2026-11-22/` 下 41 个文件已完整迁移至 `Research/Session20261122/`；31 个文件 SHA-1 未变，其余 10 个为更新 README 与历史报告状态/路径的文档。两份 `Terminal*.json.gz` 证书 blob 保持完全一致。
- 已直接读取并扫描全部 20 份当前 Markdown 的本地相对链接：**0 条失效链接**；历史已移除工作流的链接已改指历史 Git 快照。
- 加入 [RepositoryStructureChecks.py](../Sources/Python/RepositoryStructureChecks.py) 和可手工运行的 [RepositoryIntegrity.yml](../.github/workflows/RepositoryIntegrity.yml)，用于今后重复验证。工作流尚未手动触发，本记录不宣称最新代码回归已在 CI 中运行。
- 以上为文档和路径完整性验收，没有运行新的奇完全数全树搜索或增加数学下界。
