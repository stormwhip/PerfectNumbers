# PerfectNumbers 仓库目录与文件职责

**更新：2026-11-22；当前数学状态见 [CurrentStatus2400.md](CurrentStatus2400.md)。** 主线为冻结 V21，新的独立验证器与 Frontier 搜索器仍是候选系统。全量证明未完成。

## 目录结构

```text
PerfectNumbers/
├── .github/workflows/                  # GitHub 强制约定路径
├── Documentation/                      # 当前状态、数学理论、仓库维护规范
├── Records/                            # 里程碑、历史实验、验收清单
├── References/                         # 原始论文及参考资料
├── Research/
│   └── Session20261122/
│       ├── Certificates/               # 原根与替换根互素类证书（不可改变字节）
│       ├── Cpp/                        # V21 profile 和 V22–V24 历史原型
│       ├── Python/                     # 独立验证器、账本、审计器与测试
│       ├── Reports/                    # 本阶段数学/性能/集成报告
│       └── Readme.md
├── Scripts/                             # 手工运行的 WSL 脚本
├── Sources/
│   ├── Cpp/                            # V21 主线、Frontier C++、编解码与缓存
│   └── Python/                         # 正式 LP、指数清单与旧任务调度
├── Readme.md
└── Requirements.txt
```

**命名规范：** 路径名和文件主名统一采用 PascalCase（大驼峰），扩展名保持 `.cpp`、`.hpp`、`.py`、`.md`、`.yml`、`.json.gz` 等惯用小写；日期以 `SessionYYYYMMDD` 表示。GitHub 固定名称 `.github`、`workflows`、`.gitignore` 保留。历史分支不强制迁移。

## 核心文档

| 文档 | 作用 |
| --- | --- |
| [CurrentStatus2400.md](CurrentStatus2400.md) | **唯一当前状态摘要**与完整剩余任务 |
| [ProgressReport2400.md](ProgressReport2400.md) | 历史过程、对照实验和新模块进展 |
| [ResearchProblems2400.md](ResearchProblems2400.md) | 数学定义、所有待证条件及不可省略的证明义务 |
| [ValidationChecklist.md](../Records/ValidationChecklist.md) | 发布前逐项验收要求 |
| [Milestones.md](../Records/Milestones.md) | 每一阶段的证据等级及下一道门槛 |
| [ExperimentLog.md](../Records/ExperimentLog.md) | 不可篡改的历史实验记录 |
| [独立验证集成报告](../Research/Session20261122/Reports/IndependentProofIntegration2400.md) | V2 工程规格、复现命令、缺口 |

## 正式与实验程序

| 文件 | 用途 | 当前地位 |
| --- | --- | --- |
| [ProofTreeV21.cpp](../Sources/Cpp/ProofTreeV21.cpp) | V21 因子链、路障/LP 搜索 | 冻结搜索基线 |
| [ProofCoreTestsV21.cpp](../Sources/Cpp/ProofCoreTestsV21.cpp) | V21 数值回归 | 历史质量检查 |
| [BuildIndex.cpp](../Sources/Cpp/BuildIndex.cpp) | 因子表索引构造 | 生产辅助工具 |
| [PrimeCutoffCert.cpp](../Sources/Cpp/PrimeCutoffCert.cpp) | 有限素数乘积 | 生产辅助工具 |
| [ProofTreeV21Frontier.cpp](../Sources/Cpp/ProofTreeV21Frontier.cpp) | G1 复用、可切分试验搜索 | 实验性、未形成全证书 |
| [V21FrontierCodec.hpp](../Sources/Cpp/V21FrontierCodec.hpp) | 可恢复的状态编解码 V2 | 实验性 |
| [SingleFlightFactCache.hpp](../Sources/Cpp/SingleFlightFactCache.hpp) | 同键单飞共享缓存 | 独立测试，未接入搜索 |
| [IndependentVerifierV2.py](../Research/Session20261122/Python/IndependentVerifierV2.py) | 固定根独立证书检查 | 合成/篡改测试、未验完全部根 |
| [FrontierLedgerV2.py](../Research/Session20261122/Python/FrontierLedgerV2.py) | SQLite 任务、租约与分裂证据 | 故障注入测试 |
| [FrontierWorkerDriver.py](../Research/Session20261122/Python/FrontierWorkerDriver.py) | C++ 与 SQLite 调度接口 | 部分桥接 |
| [AuditRunner2400.py](../Research/Session20261122/Python/AuditRunner2400.py) | 原根 3072 项只读验收 | 真实证书尚未填满 |
| [Run2400Scheduler.py](../Sources/Python/Run2400Scheduler.py) | 旧 V21 顶层任务调度 | 保留用于复现 |
| [Run72hWSL.sh](../Scripts/Run72hWSL.sh) | 手工启停与数据准备 | 只有显式 `run` 才启动长任务 |

## 其他归档

- [研究索引](../Research/Session20261122/Readme.md)：V22–V24、路障、数值 LP、互素证书及新模块。
- `Research/Session20261122/Certificates/` 两个 `.json.gz` 为证书工件，迁移保持 Git blob SHA 原值。
- `Sources/Cpp/ProofTreeV16.cpp`、`V18`、`V19`、`V20` 以及 `Research/Session20261122/Cpp/` 下 V22–V24 是历史实现，用于精确复核不同实验。
- `.github/workflows/` 已按现有约定命名，手工大型任务不因整理而自动触发。
- `Build/`、`Run2400Results/` 与大型分解数据库不纳入源码版本库。
- 旧 `Research/2026-11-22/` 已迁移为 `Research/Session20261122/`。外部 Gemini 分支合并前须按本文件重定向路径。

## 维护规则

1. 更新当前理论状态时修改 `CurrentStatus2400.md` 和 `ProgressReport2400.md`；实验事实仅写入 `ExperimentLog.md` 并附 commit、参数和日志。
2. 成功编译、搜索器输出 `PROVEN`、独立验证器返回 `TREE_ACCEPTED` 和最终 `UNCONDITIONALLY_VERIFIED` 必须分开记录。
3. 历史报告保留当时数据和结论，上方统一增加当前状态入口。
4. 没有显式许可不运行付费 API 或启动长时间付费云资源。
