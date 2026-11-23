# PerfectNumbers

目标是证明每个奇完全数 $N>10^{2400}$，并让独立程序复核证明。

截至 2026-11-23，原根集的 **3,072** 个顶层分片中，**1,869** 个已闭合，**1,203** 个仍开放。指标容量对偶与来源素数同余新增 **18** 个已闭合分片。原根集互素类已有独立整数证书给出 `log10 N >= 4183.209493`。全局状态为 `INCOMPLETE_FRONTIER`。

- [当前状态和逐根进度](Documentation/CurrentStatus2400.md)
- [本轮推导、证书和复验说明](Research/IndicatorCapacity/Readme.md)
- [完整审计结果与开放分片清单](Research/IndicatorCapacity/Audit2400.json)
- [目录和运行入口](Documentation/RepositoryMap.md)
- [数学问题与验收条件](Documentation/ResearchProblems2400.md)

## 复验

在仓库根目录运行以下命令。Python 3.10+ 标准库足以复验证书。

```sh
mkdir -p Build
python3 Research/FermatRootValuation/IndependentCheck.py
python3 Research/IndicatorCapacity/IndicatorCapacityTests.py
python3 Research/IndicatorCapacity/AuditIndicatorCapacity2400.py --output Build/AuditSummary2400.json
cmp Research/IndicatorCapacity/Audit2400.json Build/AuditSummary2400.json
```

长时研究搜索使用 [V21](Sources/Cpp/ProofTreeV21.cpp)、[调度器](Sources/Python/Run2400Scheduler.py) 和 [Linux/WSL2 脚本](Scripts/Run72hWSL.sh)。运行产物存放在 `Build/` 或 `Run2400Results/`。工程基准与证明实验见 [实验日志](Records/ExperimentLog.md)，背景论文见 [Ochem–Rao 2012](References/OchemRao2012.pdf)。
