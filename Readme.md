# PerfectNumbers

目标定理为：对每个奇完全数 $N$，均有 $N>10^{2400}$。

夜间研究分支最新已验收状态为 **`INCOMPLETE_FRONTIER`**。相对 11 月 27 日主线的 3004/3072，本轮新增完整排除十九个规范精确键，现为 **3023/3072**；仍有 **49 个开放分片、59 个精确键、41 个单指数分片**。全局下界尚未证明。[本轮报告及逐根余集](Research/FinalNight2400/Proof.md) · [机器可读投影](Research/FinalNight2400/OpenFrontier.json) · [历史 Gemini 基线](Research/GeminiFrontier/Review.md)。

| 文档 | 内容 |
|---|---|
| [Proof2400](Documentation/Proof2400.md) | 数学推导、已证范围与证书索引 |
| [CurrentStatus2400](Documentation/CurrentStatus2400.md) | 当前逐根统计与证据等级 |
| [ResearchProblems2400](Documentation/ResearchProblems2400.md) · [NextPlan2400](Documentation/NextPlan2400.md) | 待证命题与工作顺序 |
| [RepositoryMap](Documentation/RepositoryMap.md) | 目录、依赖与复验入口 |
| [Milestones](Records/Milestones.md) · [ExperimentLog](Records/ExperimentLog.md) | 版本进度与实验记录 |

## 独立复验

在仓库根目录使用 Python 3.11+，保留断言。依次检查目录和链接、晚间冻结账本、夜间增量的精确算术及逐片投影。

```sh
python Sources/Python/RepositoryStructureChecks.py
python -I -S -B Sources/Python/FinalSprintLedgerChecks.py
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Replay.py
python -I -S -B -X int_max_str_digits=0 Research/GeminiFrontier/Verify.py
```

夜间命令重放历史 13 个完整指数；仅核对其投影可附加 `--projection-only`。最后一条命令重放 Gemini 已验收的算术、历史 45/46 枢轴证书、C10 条件证书及现行投影。两项候选条件证明未登记。[晚间 18 个指数的复验](Research/FinalSprint/Proof.md)及[历史复验顺序](Documentation/Proof2400.md#历史复验命令)另列。V21 长时实验使用 [Linux/WSL2 脚本](Scripts/Run72hWSL.sh)。
