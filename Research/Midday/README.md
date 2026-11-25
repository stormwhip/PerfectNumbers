# 午间证明证书与复验

[总证明](../../Documentation/Proof2400.md#5-11-月-25-日午间证明)汇总推导和覆盖范围。[当前状态](../../Documentation/CurrentStatus2400.md)提供逐根统计。

- [Registry.json](Registry.json) 绑定 255 个证书及其 SHA-256。
- [Delta.json](Delta.json) 记录新增实际指数、闭合分片及每个待证分片的剩余指数。
- [ReleaseAudit.md](ReleaseAudit.md) 记录冻结快照、隔离复验和计数规则。
- [ExperimentNotes.md](ExperimentNotes.md) 记录发现过程及未能签发的实验。

从干净检出使用 Python 3.11 标准库执行，保持断言启用。

~~~sh
python -I -S -B -X int_max_str_digits=0 Research/Midday/CheckLedger.py --workers 4 --check Research/Midday/Delta.json
python -I -S -B -X int_max_str_digits=0 Research/Midday/LedgerTests.py
python -I -S -B Research/MiddayFive/Replay.py --audit
~~~
