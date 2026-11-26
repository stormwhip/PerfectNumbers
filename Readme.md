# PerfectNumbers

目标定理为：对每个奇完全数 $N$，均有 $N>10^{2400}$。

当前状态为 `INCOMPLETE_FRONTIER`，目标定理尚未证完。3,072 个规范分片中已有 **2,990 个闭合**；剩余 **82 个开放分片、92 个不同的实际指数**，其中 74 个分片只剩一个指数。11 月 26 日晚间相对[冻结基线](Research/Session20261126/Delta.json)净排除 18 个实际指数，新增闭合 16 个分片。见[当前逐片账本](Research/FinalSprint/Delta.json)和[逐根结果](Research/FinalSprint/Report.md)。

| 文档 | 内容 |
|---|---|
| [Proof2400](Documentation/Proof2400.md) | 数学推导、已证范围与证书索引 |
| [CurrentStatus2400](Documentation/CurrentStatus2400.md) | 当前逐根统计与证据等级 |
| [ResearchProblems2400](Documentation/ResearchProblems2400.md) · [NextPlan2400](Documentation/NextPlan2400.md) | 待证命题与工作顺序 |
| [RepositoryMap](Documentation/RepositoryMap.md) | 目录、依赖与复验入口 |
| [ProgressReport2400](Documentation/ProgressReport2400.md) · [ExperimentLog](Records/ExperimentLog.md) | 版本进度与实验记录 |

## 独立复验

在仓库根目录使用 Python 3.11+，保留断言。晚间[增量验证器](Research/FinalSprint/Verify.py)重放新增的完整指数证书，并将其投影到冻结的基线账本；根 3 范围筛需要支持 `unsigned __int128` 的 C++17 编译器（默认 `g++`，仅安装 Clang 时设置 `CXX=clang++`）。历史批次有单独的[依赖与复验说明](Research/Session20261126/Readme.md)。

```sh
python Sources/Python/RepositoryStructureChecks.py
python -I -S -B Sources/Python/FinalSprintLedgerChecks.py
python -I -S -B -X int_max_str_digits=0 Research/FinalSprint/Verify.py
```

前两条命令分别检查命名与链接、证书哈希与逐片投影，均不验证全部数学推理。第三条重放本批完整指数的证明并重算账本，不重放全部历史证明。[条件支持](Research/FinalSprint/Support/README.md)与[低指数枢轴](Research/FinalSprint/LowBranches/README.md)另行复验，不计作新增闭片。历史复验入口见[总证明](Documentation/Proof2400.md#历史复验命令)。V21 计时实验使用 [Linux/WSL2 脚本](Scripts/Run72hWSL.sh)。
