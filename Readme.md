# PerfectNumbers

目标是证明每个奇完全数 $N>10^{2400}$，并让独立程序复核证明。

截至北京时间 2026-11-25，此研究分支有 **2,574 / 3,072** 个规范分片闭合，余 **498** 个。夜间相对 `3b50576` 净增 382 个完整分片、949 个实际指数。原八根互素类保持 `log10 N >= 4183.209493`；四根互素类已有独立重放的 `log10 N >= 2411.108934`。全局状态为 `INCOMPLETE_FRONTIER`。

- [总证明](Documentation/Proof2400.md)
- [当前状态](Documentation/CurrentStatus2400.md)及[逐片待证清单](Research/NightMerge/Audit.json)
- [下一步计划](Documentation/NextPlan2400.md)
- [仓库目录](Documentation/RepositoryMap.md)和[历史实验](Records/ExperimentLog.md)

## 复验

单独复验此次合并的新增证书可直接运行下面代码块的最后一条命令。其它命令复验互素类和历史基线。运行环境为仓库根目录及 Python 3.10+ 标准库。

```sh
mkdir -p Build
python3 -S Research/Session20261122/Python/TerminalCertificate.py verify Research/Session20261122/Certificates/TerminalOriginal.json.gz
python3 Research/FermatRootValuation/IndependentCheck.py
python3 Research/IndicatorCapacity/IndicatorCapacityTests.py
python3 Research/IndicatorCapacity/AuditIndicatorCapacity2400.py --output Build/AuditSummary2400.json
cmp Research/IndicatorCapacity/Audit2400.json Build/AuditSummary2400.json
python3 Research/TeichmullerValuation/TeichmullerValuationTests.py
python3 Research/TeichmullerValuation/AuditTeichmullerValuation2400.py --output Build/AuditTeichmuller2400.json
cmp Research/TeichmullerValuation/Audit2400.json Build/AuditTeichmuller2400.json
python3 Research/TeichmullerValuation/AuditGeminiBatch2400.py --remaining Build/RemainingBeforeGapSupply2400.json
python3 Research/EveningMerge/VerifyFrontier.py --workers 6
python3 -B Research/NightMerge/Checkpoint.py
```

长时研究搜索使用 [V21](Sources/Cpp/ProofTreeV21.cpp)、[调度器](Sources/Python/Run2400Scheduler.py) 和 [Linux/WSL2 脚本](Scripts/Run72hWSL.sh)。运行产物存放在 `Build/` 或 `Run2400Results/`。工程基准与证明实验见 [实验日志](Records/ExperimentLog.md)，背景论文见 [Ochem–Rao 2012](References/OchemRao2012.pdf)。
