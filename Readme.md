# PerfectNumbers

目标定理为：对每个奇完全数 $N$，均有 $N>10^{2400}$。

当前状态为 `INCOMPLETE_FRONTIER`。3,072 个规范分片中已有 **2,974 个闭合**，剩余 **98 个分片、110 个不同的实际指数**，其中 89 个分片只剩一个指数。本批净排除 134 个实际指数，新增闭合 106 个分片。见[增量账本](Research/Session20261126/Delta.json)和[复验说明](Research/Session20261126/Readme.md)。

| 文档 | 内容 |
|---|---|
| [Proof2400](Documentation/Proof2400.md) | 数学推导、已证范围与证书索引 |
| [CurrentStatus2400](Documentation/CurrentStatus2400.md) | 当前逐根统计与证据等级 |
| [ResearchProblems2400](Documentation/ResearchProblems2400.md) · [NextPlan2400](Documentation/NextPlan2400.md) | 待证命题与工作顺序 |
| [RepositoryMap](Documentation/RepositoryMap.md) | 目录、依赖与复验入口 |
| [ProgressReport2400](Documentation/ProgressReport2400.md) · [ExperimentLog](Records/ExperimentLog.md) | 版本进度与实验记录 |

## 独立复验

在仓库根目录使用 Python 3.11+，保留断言。完整增量复验需要支持 `unsigned __int128` 的 C++17 编译器及 `python-flint==0.9.0`。依赖设置见[复验说明](Research/Session20261126/Readme.md)。

```sh
python Sources/Python/RepositoryStructureChecks.py
python -I -S -B Research/Session20261126/CheckFrontier.py
python -I -S -B -X int_max_str_digits=0 Research/Session20261126/Replay.py
```

三条命令依次检查仓库与链接、核对开放前沿表、重放本批证明并重新计算分片账本。历史复验入口见[总证明](Documentation/Proof2400.md#历史复验命令)。V21 计时实验使用 [Linux/WSL2 脚本](Scripts/Run72hWSL.sh)。
