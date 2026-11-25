# PerfectNumbers

目标定理为：对每个奇完全数 $N$，均有 $N>10^{2400}$。

当前为 `INCOMPLETE_FRONTIER`。八根互素类已排除。3,072 个含根规范分片中，2,868 个闭合，204 个开放，涉及 244 个不同实际指数。SupportSplit 新排除 9 个条件支持组合，各实际指数仍有开放组合。

根 3 五个高指数的 E0/E1/E2 已获独立整数分支证明；1162 新对偶已核验，联合丰度分配待完成。完整闭合增量为 0。见[续研证据](Research/P3I00193Review/Progress.md)。

| 文档 | 内容 |
|---|---|
| [Proof2400](Documentation/Proof2400.md) | 数学推导、已证范围与证书索引 |
| [CurrentStatus2400](Documentation/CurrentStatus2400.md) | 当前逐根统计与证据等级 |
| [ResearchProblems2400](Documentation/ResearchProblems2400.md) · [NextPlan2400](Documentation/NextPlan2400.md) | 待证命题与工作顺序 |
| [RepositoryMap](Documentation/RepositoryMap.md) | 目录、依赖与复验入口 |
| [ProgressReport2400](Documentation/ProgressReport2400.md) · [ExperimentLog](Records/ExperimentLog.md) | 版本进度与实验记录 |

## 独立复验

在仓库根目录用 Python 3.11 或更高版本运行，保留断言。

```sh
python3 Sources/Python/RepositoryStructureChecks.py
python3 -I -S -B Research/SupportSplit/Verify.py
python3 -I -S -B -X int_max_str_digits=0 Research/Midday/LedgerTests.py
python3 -I -S -B -X int_max_str_digits=0 Research/Midday/CheckLedger.py --workers 4 --check Research/Midday/Delta.json
```

四条命令分别检查仓库路径与相对链接、条件支持排除、证书摘要与分片投影、午间登记证书的算术及覆盖。完整的历史复验入口见[总证明](Documentation/Proof2400.md#历史复验命令)。V21 长时实验使用 [Linux/WSL2 脚本](Scripts/Run72hWSL.sh)。
