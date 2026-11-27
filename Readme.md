# PerfectNumbers

目标定理为：对每个奇完全数 $N$，均有 $N>10^{2400}$。

当前状态为 `INCOMPLETE_FRONTIER`。3,072 个规范分片中已有 **3,003 个闭合**，余 **69 个开放分片、79 个不同的 $(p,e)$**，其中 61 个分片只剩一个指数。11 月 27 日批次排除 13 个完整指数，新增闭合 13 片。$N>10^{2400}$ 仍待证明。[逐片余集](Research/Night2400/ShardToKeys.json) · [证明与复验](Research/Night2400/README.md)。

| 文档 | 内容 |
|---|---|
| [Proof2400](Documentation/Proof2400.md) | 数学推导、已证范围与证书索引 |
| [CurrentStatus2400](Documentation/CurrentStatus2400.md) | 当前逐根统计与证据等级 |
| [ResearchProblems2400](Documentation/ResearchProblems2400.md) · [NextPlan2400](Documentation/NextPlan2400.md) | 待证命题与工作顺序 |
| [RepositoryMap](Documentation/RepositoryMap.md) | 目录、依赖与复验入口 |
| [ProgressReport2400](Documentation/ProgressReport2400.md) · [ExperimentLog](Records/ExperimentLog.md) | 版本进度与实验记录 |

## 独立复验

在仓库根目录使用 Python 3.11+，保留断言。依次检查目录和链接、晚间冻结账本、夜间增量的精确算术及逐片投影。

```sh
python Sources/Python/RepositoryStructureChecks.py
python -I -S -B Sources/Python/FinalSprintLedgerChecks.py
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Replay.py
```

最后一条命令重放 13 个完整指数的证书并重算现行账本。仅核对投影时可附加 `--projection-only`。[晚间 18 个指数的复验](Research/FinalSprint/Proof.md)及[历史复验顺序](Documentation/Proof2400.md#历史复验命令)另列。V21 长时实验使用 [Linux/WSL2 脚本](Scripts/Run72hWSL.sh)。
