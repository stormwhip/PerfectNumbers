# PerfectNumbers

项目目标是证明每个奇完全数 $N>10^{2400}$，并由独立程序复验。

目前闭合 **2,868 / 3,072** 个规范分片，余 **204** 片、**244** 个实际指数，其中 **181** 片只剩一个指数。PR #5 排除 **267** 个实际指数，新增闭合 **202** 片。全局状态为 INCOMPLETE_FRONTIER。

- [总证明](Documentation/Proof2400.md) · [逐根状态](Documentation/CurrentStatus2400.md) · [下一步](Documentation/NextPlan2400.md)
- [证书与复验](Research/Midday/README.md) · [逐片待证清单](Research/Midday/Delta.json)
- [仓库目录](Documentation/RepositoryMap.md) · [实验日志](Records/ExperimentLog.md)

## 复验

从仓库根目录使用 Python 3.11 标准库执行。

~~~sh
python -I -S -B -X int_max_str_digits=0 Research/Midday/LedgerTests.py
python -I -S -B -X int_max_str_digits=0 Research/Midday/CheckLedger.py --workers 4 --check Research/Midday/Delta.json
~~~

第一条独立核对证书哈希及分片清点，第二条逐包重算本轮证明。此前各批见[历史复验命令](Documentation/Proof2400.md#历史复验命令)。长时搜索使用 [V21](Sources/Cpp/ProofTreeV21.cpp) 和 [Linux/WSL2 脚本](Scripts/Run72hWSL.sh)。
