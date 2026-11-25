# PerfectNumbers

目标是证明每个奇完全数 $N>10^{2400}$，并让独立程序复核证明。

相对 11 月 25 日 10:05 的 `main`（`6732a1a`），新增排除 **259** 个不同实际指数、闭合 **196** 个规范分片；累计 **2,862 / 3,072**，余 **210** 片、**252** 个不同实际指数，其中 **186** 片只剩一个实际指数。全局状态仍为 `INCOMPLETE_FRONTIER`。 [午间研究及复验](Research/Midday/README.md)。

- [总证明](Documentation/Proof2400.md)
- [当前状态](Documentation/CurrentStatus2400.md)及[逐片待证清单](Research/Midday/Delta.json)
- [下一步计划](Documentation/NextPlan2400.md)
- [仓库目录](Documentation/RepositoryMap.md)和[历史实验](Records/ExperimentLog.md)

## 复验

以下命令从仓库根运行，使用 Python 3.10+ 标准库。复验本轮新增证书时可单独执行最后一条。

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
python3 -B Research/NightMerge/ParallelReplay.py --workers 10 --fresh --receipts ../PerfectNumbersNightReceipts
python3 -I -S -B Research/Nov25/Ledger.py --workers 10 --check Research/Nov25/Delta.json
```

历史夜间证书的 `ParallelReplay.py` 应在干净检出中运行，回执目录放在仓库外。本轮独立清点和证书哈希核对命令见[复验说明](Research/Nov25/Closeout.md#复验范围)。

长时研究搜索使用 [V21](Sources/Cpp/ProofTreeV21.cpp)、[调度器](Sources/Python/Run2400Scheduler.py) 和 [Linux/WSL2 脚本](Scripts/Run72hWSL.sh)。运行产物存放在 `Build/` 或 `Run2400Results/`。工程基准与证明实验见 [实验日志](Records/ExperimentLog.md)，背景论文见 [Ochem–Rao 2012](References/OchemRao2012.pdf)。
