# PerfectNumbers

目标是证明每个奇完全数 $N>10^{2400}$，并让独立程序复核证明。

截至 2026-11-24，原根集的 **3,072** 个顶层分片中，**2,192** 个已闭合，**880** 个仍开放。相对于 [4aad42d 基线](Research/GapSupply2400/Proof.md)，[晚间合并审计](Research/EveningMerge/README.md)净排除 **530** 个实际指数，关闭 **162** 个完整分片。原根集互素类已有独立整数证书给出 `log10 N >= 4183.209493`。全局状态为 `INCOMPLETE_FRONTIER`。

- [当前状态和逐根进度](Documentation/CurrentStatus2400.md)
- [项目研究报告、最新实验和下一步](Documentation/ResearchReport2400.md)
- [历史进度与工程实验](Documentation/ProgressReport2400.md)
- [已验收 Gemini 批次的推导和复验](Research/TeichmullerValuation/GeminiBatchProof2400.md)
- [Claude 的 Euler 筛证书与合并复验](Research/EulerOneSieve/Readme.md)
- [Gemini 批次审计](Research/TeichmullerValuation/GeminiBatchAudit2400.json)
- [Teichmüller 基线审计](Research/TeichmullerValuation/Audit2400.json)
- [上一轮：指标容量对偶](Research/IndicatorCapacity/Readme.md)
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
python3 Research/TeichmullerValuation/TeichmullerValuationTests.py
python3 Research/TeichmullerValuation/AuditTeichmullerValuation2400.py --output Build/AuditTeichmuller2400.json
cmp Research/TeichmullerValuation/Audit2400.json Build/AuditTeichmuller2400.json
python3 Research/TeichmullerValuation/AuditGeminiBatch2400.py --remaining Build/RemainingBeforeGapSupply2400.json
python3 Research/GapSupply2400/CheckShards.py
python3 Research/EveningMerge/VerifyFrontier.py --workers 6
```

长时研究搜索使用 [V21](Sources/Cpp/ProofTreeV21.cpp)、[调度器](Sources/Python/Run2400Scheduler.py) 和 [Linux/WSL2 脚本](Scripts/Run72hWSL.sh)。运行产物存放在 `Build/` 或 `Run2400Results/`。工程基准与证明实验见 [实验日志](Records/ExperimentLog.md)，背景论文见 [Ochem–Rao 2012](References/OchemRao2012.pdf)。
